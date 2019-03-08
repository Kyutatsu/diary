# diary
Web開発の練習を目的として作成したWebアプリケーションです。
## 機能概要
絵日記をイメージしたアプリケーションです。まず画像をアップロード、もしくはブラウザ上で作成し登録します。登録した画像を元に、絵日記を作成、掲示板に投稿、また連携すれば直接twitterに投稿することができます。


## 構成
基本的にDjangoの一般的な構成(自動生成される構成)のままで作成しています。

- diary: 絵日記を作成するための機能です。
- drawing: 画像のアップロード、もしくはブラウザ上で簡単なお絵かきをするための機能です。
- Tweetdiary: drawingで作成した画像をクリック一つでtwitterに呟きます。
- board: drawingで作成した画像やコメントを投稿できる掲示板です。本アプリを利用しているユーザー間で交流できます。
- author: プロフィール情報および、サインアップに関係する機能をまとめています。
下の画像は本アプリケーションのheader部分です(pcなど大きめの表示の場合).画像に書き込んであるとおりにコードと画面が基本的には対応しています。tweetdiary機能は、drawing(イラスト)の詳細から利用可能です(後述)

![fig1](https://github.com/Kyutatsu/diary/blob/pictures/fig1.png)

またhtmlファイルは、各appフォルダにあるtemplatesにまとめてあります。baseのディレクトリのtemplatesディレクトリには全てのhtmlファイルの継承元になるbase.htmlと、ログイン/ログアウト用のtemplateを配置しています。



## 実装した機能の抜粋とコードへの参照
特に参考にしていただけると思う箇所への参照をピックアップさせていただきました。


### Django
基本的な機能を一通り実装できます。公式ドキュメントを参照しながら、実装したい機能を持ったクラスを探して利用することができます。
**board**フォルダを見ていただけるとわかりやすいです(link)。
- CRUD
  - diary, drawing,authorで実装しています。Diary(link)がわかりやすいです。
- Pagination
  - Board(リンク)では,直接Paginationオブジェクトをviewで扱っています。対応するテンプレートはboard/template/board/topic_list.htmlです。
- 認証機能
  - ログイン,ログアウトはDjangoの提供するViewを利用しています(django.contrib.auth.urlsをurlにincludeしています)。Templateは/template/registrationに作成しました。
  - サインアップはauthor/views.py(line68)に実装しています。[この動画](https://www.youtube.com/watch?v=aCotgGyS2gc&list=PLf5QDVUBPTbyt4rCfIMQPh_IsCWoDW0jF&index=4&t=65s)を参考にしながら作成しました。
- テスト
  - diary/tests.pyのみです。手が回っておらず、不十分です。今後しっかりと書いていきたいです。
- API(Twitter API)との連携: twitterへの画像投稿(ツイート)機能
  - tweetdiary/views.pyに実装しています。Drawingのdetail viewからツイッターに画像投稿が可能です。Twitter APIとのやりとりにrequests_oauthlibを利用しています。Drawing appで作成した画像は透過png形式でtwitter投稿には不適ですので、PILを利用して透過部分を白色に変換してからツイートしています。取得したアクセスキーはセッションに保存し、なんどもログインすることを防いでいます。

![fig2](https://github.com/Kyutatsu/diary/blob/pictures/fig2.png)
![fig3](https://github.com/Kyutatsu/diary/blob/pictures/fig3.png)
