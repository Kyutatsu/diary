from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.urls import reverse

from django.core.paginator import Paginator

from .models import Article
from .forms import ArticleForm
from author.models import Author
from drawing.models import DrawingModel


class IndexView(LoginRequiredMixin, generic.ListView):
    '''作成した日記の一覧を表示する'''
    template_name = 'diary/index.html'
    context_object_name = 'diaries'
    paginate_by = 3
    model = Article

    def get_queryset(self):
        try:
            author = Author.objects.get(user=self.request.user)
        except Exception:
            return []
        return Article.objects.filter(author=author).order_by('-created_date')


# 修正予定: object毎のpermission
class IndividualView(LoginRequiredMixin, generic.View):
    template_name = 'diary/individual.html'

    def get(self, request, pk):
        try:
            author = Author.objects.get(user=self.request.user)
        except Exception:
            return HttpResponse('まだ日記を書いてません')
        article = Article.objects.get(pk=pk)
        if article.author == author:
            return render(
                    request,
                    self.template_name,
                    {
                        'article': article,
                    }
            )
        else:
            return HttpResponseForbidden()


@login_required
def make_diary(request):
    '''あたらしい日記を作成する'''
    author = get_object_or_404(Author, user=request.user)
    drawings = DrawingModel.objects.filter(author=author)
    drawings = drawings.order_by('-created_date')
    drawings_url_list = []
    for drawing in drawings:
        drawings_url_list.append(drawing.drawing.url)
    num_four = list(range(1, len(drawings_url_list) // 4 + 2))
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            author = Author.objects.get(user=request.user)
            # ログイン中のuser-objをセット
            author.article_set.add(article)
            article.picture = request.POST.get('select_img', None)
            article.save()

            return HttpResponseRedirect(reverse('diary:index'))
    else:
        form = ArticleForm()
    return render(request, 'diary/make_diary.html', {
        'form': form,
        'drawings_url_list': drawings_url_list,
        'num_four': num_four,
        })


def update_diary(request, pk):
    '''日記を編集する'''
    diary = get_object_or_404(Article, pk=pk)
    author = get_object_or_404(Author, user=request.user)
    drawings = DrawingModel.objects.filter(author=author)
    drawings_url_list = []
    for drawing in drawings:
        drawings_url_list.append(drawing.drawing.url)
    num_four = list(range(1, len(drawings_url_list) // 4 + 2))  # 絵一覧のリンク数
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=diary)
        if form.is_valid():
            article = form.save()
            article.picture = request.POST.get('select_img', None)
            article.save()
            return redirect('diary:individual', pk=diary.pk)
    else:
        form = ArticleForm(instance=diary)
    return render(
            request,
            'diary/update_diary.html',
            {
                'form': form, 'PK': pk,  # pkここで渡した
                'drawings_url_list': drawings_url_list,
                'now_picture': diary.picture,
                'num_four': num_four,
            }
    )


@login_required
def delete_diary(request, pk):
    """日記の削除
    
    確認ダイアログで削除を選んだのちここに飛ばす。
    """
    diary = get_object_or_404(Article, pk=pk)
    diary.delete()
    return redirect('diary:index')
