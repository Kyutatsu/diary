import json
import os
import tempfile
import uuid

from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
from PIL import Image

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from drawing.models import DrawingModel
from diarySite.settings import MEDIA_ROOT


APIKEY = os.environ.get('ApiKey', False)
APISECRETKEY = os.environ.get('ApiSecretKey', False)
oauth_callback = "https://qtatsu.com/tweetdiary/get_token/"
# oauth_callback = "http://127.0.0.1:8000/tweetdiary/get_token/"


def post_drawing(request, pk):
    """sessionのaccess_tokenに値があれば使ってツイートし、そうでなければ取得する """
    access_token = request.session.get('access_token', None)
    if access_token:
        # 200返せなかったら、そこでaccess_token取り直せばいいか。
        twitter = OAuth1Session(
                APIKEY,
                APISECRETKEY,
                access_token['oauth_token'],
                access_token['oauth_token_secret'],
        )
        drawing = get_object_or_404(DrawingModel, id=pk)
        drawing_path = MEDIA_ROOT[:-7] + drawing.drawing.url
#         with open(drawing_path, 'rb') as file:
#             file_data = file.read()
# twitterのviewerは背景黒だったので、透過背景を白に変換しておくことにする。
        im = Image.open(drawing_path)
        im_white_background = Image.new("RGB", im.size, (255, 255, 255))
        im_white_background.paste(im, mask=im.split()[3])
        # 擬似的にPILでfileを保存せずにImageオブジェクト>bytesに変換するため
        # temp directoryを作り、そこに保存することにした。
        with tempfile.TemporaryDirectory() as tmpdirname:
            path_name = tmpdirname + '/im_png.png'
            im_white_background.save(path_name)
            with open(path_name, 'rb') as im_png:
                params_for_file_upload = {
                        'user_id': access_token['user_id'],
                        'media': im_png,
                }
                response_for_file_upload = twitter.post(
                        'https://upload.twitter.com/1.1/media/upload.json',
                        files=params_for_file_upload,
                )
        if response_for_file_upload.status_code == 200:
            uploaded_file = json.loads(response_for_file_upload.text)
        else:
            return HttpResponse('ファイルアップロードできてない')
        # タイトルを取得する
        title = drawing.title[:140]

        params = {
                'user_id': access_token['user_id'],
                'status': title,
                'media_ids': uploaded_file['media_id_string'],
        }
        twitter.post(
                'https://api.twitter.com/1.1/statuses/update.json',
                params=params,
        )
        return HttpResponseRedirect(reverse('tweetdiary:select_url'))

    else:
        request.session['upload_file_pk'] = str(pk)  # loginしてない初回,pk保存
        tweet = OAuth1Session(APIKEY, APISECRETKEY)
        response = tweet.post(
                url="https://api.twitter.com/oauth/request_token",
                params={
                    'oauth_callback': oauth_callback
                },
        )
        if response.status_code == 200:  # type: int
            request_token = dict(parse_qsl(response.content.decode('utf-8')))
            auth_url = "https://api.twitter.com/oauth/authenticate"
            auth_endpoint = f"{auth_url}?oauth_token={request_token['oauth_token']}"
            return HttpResponseRedirect(auth_endpoint)
        else:
            return HttpResponse('投稿できません')


def get_access_token(request):
    """authenticateのendpointへリダイレクト後call_backしてくる場所.

    画面としては存在せず、urlのoauth_tokenとverifierの値をもらうためのviewとして使う.
    これをtwitterのdeveloperページに登録してある.
    """
    result_url = request.get_full_path()
    context = result_url.split('?')[1]
    keys = dict(parse_qsl(context, encoding='utf-8'))
    oauth_token = keys.get('oauth_token', None)
    oauth_verifier = keys.get('oauth_verifier', None)
    tweet = OAuth1Session(APIKEY, APISECRETKEY, oauth_token, oauth_verifier)
    response = tweet.post(
            'https://api.twitter.com/oauth/access_token',
            params={
                'oauth_verifier': oauth_verifier
            },
    )
    if response.status_code == 200:
        access_token = dict(parse_qsl(response.content.decode('utf-8')))
        request.session['access_token'] = access_token
        pk = uuid.UUID(request.session.get('upload_file_pk'))
        return HttpResponseRedirect(
                reverse('tweetdiary:tweet_drawing', args=[pk])
        )
    else:
        return HttpResponse('access_token取得ができません')


def select_url(request):
    return render(
            request,
            'tweetdiary/select_url.html',
    )
