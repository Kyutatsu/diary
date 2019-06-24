# diary
Web開発の練習として作成したWebアプリケーションです。[こちら](https://qtatsu.com)からぜひお試しください。
<iframe src="https://github.com/Kyutatsu/diary/blob/pictures/diary.mp4"></iframe>
## 機能概要
絵日記をイメージしたアプリケーションです。まずブラウザ上でお絵かきした画像を登録します(fileをuploadでもOK)。画像を元に絵日記を作成、掲示板に投稿、また連携すればclick一つでtwitterに投稿することができます。

## 機能紹介動画
3分程度です
![movie](https://github.com/Kyutatsu/diary/blob/pictures/diary.gif)

## 使用技術の一覧
- サーバーサイド
  - Python3
  - Django
- クライアントサイド
  - JavaScript
  - Bootstrap
- インフラ: もう一つのアプリ(imagesFromTwitter)をサブドメインで公開してます。
  - Linux(CentOS7)
  - Apache
  - mod_wsgi
    - Daemon modeで使用してます。
  - MySQL
- その他(デプロイ, バージョン管理, 開発)
  - VPS(独自ドメインを取得し、さくらのVPSを借りて公開しています)
  - SSL(Let's Encrypt)
  - Git
  - Vim
  - Vagrant, VirtualBox: デプロイの練習に使用した。

## ファイルの構成
基本的にDjangoの一般的な構成(自動生成される構成)のままで作成しています。

- diary: 絵日記を作成するための機能です。
- drawing: 画像のアップロード、もしくはブラウザ上で簡単なお絵かきをするための機能です。
- Tweetdiary: drawingで作成した画像をクリック一つで**twitter**に呟きます。
- board: drawingで作成した画像やコメントを投稿できる掲示板です。ユーザー間で交流できます。
- author: プロフィール情報および、サインアップに関係する機能をまとめています。

## 実装した機能の詳細とコードへの参照
特に参考にしていただけると思う箇所への参照をピックアップさせていただきました。

### Django
**基本的な機能を一通り実装できます。** 公式ドキュメントを参照しながら、実装したい機能を持ったクラスを探して利用することができます。
**board**フォルダを見ていただけるとわかりやすいです=>[diary/board](https://github.com/Kyutatsu/diary/tree/be96e7c9993b44946cded4c4811f5392d9326333/board)。
- CRUD
  - diary, drawing,authorで実装しています。[diaryのview](https://github.com/Kyutatsu/diary/blob/be96e7c9993b44946cded4c4811f5392d9326333/diary/views.py)がわかりやすいです。
- Pagination
  - diary,drawing,boardで使用しています。[board:line35](https://github.com/Kyutatsu/diary/blob/be96e7c9993b44946cded4c4811f5392d9326333/board/views.py#L35)では,直接Paginationオブジェクトをviewで扱っています。テンプレート[board/template/board/topic_list.htmlのこの箇所](https://github.com/Kyutatsu/diary/blob/be96e7c9993b44946cded4c4811f5392d9326333/board/templates/board/topic_list.html#L36)が対応します。
- 認証機能
  - ログイン,ログアウトはDjangoの提供するViewを利用しています(django.contrib.auth.urlsをurlにincludeしています)。Templateは/template/registrationに作成しました。
  - サインアップはauthor/views.py(line68)に実装しています。[この動画](https://www.youtube.com/watch?v=aCotgGyS2gc&list=PLf5QDVUBPTbyt4rCfIMQPh_IsCWoDW0jF&index=4&t=65s)を参考にしながら作成しました。
- 単体テスト
  - [diary/tests.py](https://github.com/Kyutatsu/diary/blob/be96e7c9993b44946cded4c4811f5392d9326333/diary/tests.py)のみです。手が回っておらず、不十分です。今後しっかりと書いていきたいです。
- Twitter APIとの連携: twitterへの画像投稿(ツイート)機能
  - t[weetdiary/views.py](https://github.com/Kyutatsu/diary/blob/be96e7c9993b44946cded4c4811f5392d9326333/tweetdiary/views.py)に実装しています。イラストの詳細ページ(イラスト一覧 > 閲覧 > twitterに投稿)からツイッターに画像投稿が可能です(下の画像参照)。Twitter APIとのやりとりにrequests_oauthlibを利用しています。取得したアクセスキーはセッションに保存し、複数回ログインする手間を防いでいます。


### JavaScript
基本的な要素の取得やeventListenerによる変更以外に、canvas要素やスマートホンのタッチイベントなどを利用しました。
- canvas要素を利用したブラウザ上でのお絵かき機能
  - [drawing/static/drawing/drawing.js](https://github.com/Kyutatsu/diary/blob/be96e7c9993b44946cded4c4811f5392d9326333/drawing/static/drawing/drawing.js)に実装しています。PCでもスマートホンでも利用可能です。画像をアップロードし、それを元に加筆することもできます(イラストを描くページで“CLICKして選ぶ”を押すか、ドラッグ&ドロップで画像をcanvasに落とせます)。Base64形式で[canvasからデータを取り出し](https://github.com/Kyutatsu/diary/blob/be96e7c9993b44946cded4c4811f5392d9326333/drawing/static/drawing/drawing.js#L85)、[drawing/views.py: line61](https://github.com/Kyutatsu/diary/blob/be96e7c9993b44946cded4c4811f5392d9326333/drawing/views.py#L61)で、デコードし、ファイルオブジェクトに変換して保存しています。
- 画像選択
  - [diary/static/diary/pictures.js](https://github.com/Kyutatsu/diary/blob/be96e7c9993b44946cded4c4811f5392d9326333/diary/static/diary/pictures.js)など。これまで描いた画像から、diaryに使用する画像を選択します。ページ内で、擬似的にPaginationのように画像が表示されるようにしています。

### Bootstrap
すべてのテンプレートにおいてBootstrapを利用し、レスポンシブ対応にしています。

### 作成時に注意した点
また機能ごとにアプリケーションをなるべく分け、一つのアプリケーションには一つの仕事をさせることを意識しました。うまくできたとは言えませんが、反省を活かして次はもっと独立した設計にできると思います。

### 反省点
設計が不十分であり、冗長な部分が多くできてしまいました。
また、各modelに不要なfieldが存在します。
そのため全体的に効率が悪く他者から読みづらいコードになってしまったと思います。論理的に正しく、無駄のない読みやすい構造を目指そうと反省しています。
