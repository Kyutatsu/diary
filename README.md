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
2.	JavaScript
基本的な要素の取得や変更以外に、canvas要素やスマートホンのタッチイベントなどを利用できます。
・	canvas要素を利用したブラウザ上でのお絵かき機能
➢	drawing/static/drawing/drawing.jsに実装しています。PCでもスマートホンでも利用可能です。画像をアップロードし、それを元に加筆することもできます(“CLICKして選ぶ”を押すか、ドラッグ&ドロップで画像をcanvasに落とせます)。Base64形式でcanvasからデータを取り出し、drawing/views.pyのline41で、デコードし、ファイルオブジェクトに変換して保存しています。
・	画像選択
➢	diary/static/diary/pictures.jsなど。これまで描いた画像から、diaryに使用する画像を選択します。ページ内で、擬似的にPaginationのように画像が表示されるようにしています。

3.	Bootstrap
・	すべてのテンプレートにおいてBootstrapを利用し、レスポンシブ対応にしています。


[作成時に注意したところ]
・機能ごとにアプリケーションをなるべく細かく分け、「一つのアプリケーションには一つの仕事をさせる」ことを目指しました。個々のアプリケーションが再利用可能となるよう、意識を払いました。結局、満足のいく出来ではありませんでしたが、反省を活かして次はもっと独立した設計にできると思います。

[反省点]
設計が不十分であり、冗長な部分が多くできてしまいました。例えば、author appはDjangoのUserオブジェクトに対して生年月日などの情報を付加するだけの機能を与えるつもりで作成しましたが、author/models.pyで定義したAuthorオブジェクトをdrawingやdiaryで利用してしまいました。絵や日記を個人に結びつけるためにAuthorを使用していますが、この目的からはUserオブジェクトで十分でした。修正予定です。
また、各modelに不要なfieldが存在します。Drawingモデルのdrawing_base64フィールドは不要であり、データベースを圧迫するだけのものとなっています。修正予定です。
全体的にこのようなミスにより、効率が悪く他者から読みづらいコードになってしまったと思います。論理的に正しく、無駄のない読みやすい構造を目指そうと反省しています。

