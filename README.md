# Overview
[LINE API Use Caseサイト](https://lineapiusecase.com/ja/top.html)で提供している[テーブルオーダー](https://lineapiusecase.com/ja/usecase/tableorder.html)のデモアプリケーションソースコードとなります。    
今回紹介している手順を参考にすると、LINE APIを活用したテーブルオーダーアプリケーションを開発することが可能です。    
テーブルオーダーアプリケーションを利用すると、LINEアプリ上で飲食店のメニューを表示し、注文～決済を行うことが出来ます。そのため、店舗で注文用に独自のハードウェアを持つ必要が無くなります。   
さらに、決済後にLIFFアプリで取得したユーザーIDを利用し、LINEで販促メッセージを送信することも出来ます。

なお、このページで紹介しているソースコードの環境はAWSを利用しています。  
※ ドキュメントなどの文言は日本語対応となっています。  
※ This document is written in only Japanese for now. We’ll translate it later as soon as possible.

# Libraries
## Node.js

フロントエンド側の開発で使用する Node.js をローカル開発環境にインストールしてください。
※ v10.13 以上 最新の LTS バージョンのインストールをおすすめします。なお、Cloud9にはすでにNode.jsのバージョン10.24.1がインストール済みです。

```
node -v
v10.24.1 
```
↑ このように表示されたら、インストール済みです。

【Node.jsダウンロードサイト】  
https://nodejs.org/ja/download/

## Python

Pythonのバージョン3.8以上がインストール済みでない場合、インストールしてください。  
2021-04-28時点では、Pythonは3.7.9がインストールされているため、3.8を以下のコマンドでインストールしてください。

```
git clone https://github.com/jaws-ug-kanazawa/line-api-use-case-table-order.git
cd line-api-use-case-table-order/tools/
sh install_python3.8.sh
```

コマンドプロンプト、又はターミナルにて以下のコマンドを入力し、インストール済みか確認できます。
```
python --version
Python 3.8.5
```

```
pip --version
pip 9.0.3 from /usr/lib/python3.8/site-packages (python 3.8)
```
↑ このように表示されたら、インストール済みです。

Cloud9以外の環境で開発する場合においてPythonがインストール済みでない場合、バックエンド側の開発で使用するPython（3.8以上）をローカル開発環境にインストールしてください。

【Pythonインストール参考サイト】  
Windows: https://www.python.jp/install/windows/install.html  
Mac: https://www.python.jp/install/macos/index.html

## AWS SAM
本アプリケーションのデプロイには、AWS サーバーレスアプリケーションモデル(AWS SAM)を利用します。
[AWS公式ドキュメント](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html
)を参考に、AWS アカウントの登録と設定、AWS SAM CLI と Docker のインストールを行ってください。  
※ SAM CLIの推奨バージョンは1.15.0以上  
※ Docker のインストールもローカルテストの有無に関わらず必要です。

## ディスク容量の拡張

Cloud9の初期EBSサイズは10GiBです。SAMを利用する際に10GBを超える容量のサイズが必要となるため、以下の方法にてEBSボリュームサイズを20GBに変更してください。

```
cd line-api-use-case-table-order/tools/
sh resize.sh 20
```

df -Hのコマンドを実行し、/dev/xvda1が20GiB(22GB)になっていることを確認してください。
```
Filesystem      Size  Used Avail Use% Mounted on
devtmpfs        497M     0  497M   0% /dev
tmpfs           516M     0  516M   0% /dev/shm
tmpfs           516M  566k  515M   1% /run
tmpfs           516M     0  516M   0% /sys/fs/cgroup
/dev/xvda1       22G   12G   11G  52% /
tmpfs           104M     0  104M   0% /run/user/1000
tmpfs           104M     0  104M   0% /run/user/0
```

### 公式ドキュメントの参考箇所
公式ドキュメントの以下の項目を完了させ、次の手順に進んでください。なお、既に導入済みのものは適宜飛ばして下さい。  
※本資料は 2020 年 12 月に作成しているため、最新の公式ドキュメントの内容と齟齬がある可能性があります。

1. [AWS SAM CLI のインストール](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
1. [AWS 認証情報の設定](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-getting-started-set-up-credentials.html)
1. [（任意）チュートリアル: Hello World アプリケーションの導入](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html)

# Getting Started / Tutorial
こちらの手順では、アプリケーション開発に必要な「LINEチャネル作成、バックエンド・フロントエンドの構築、テストデータ投入、動作確認」について説明します。
以下リンク先の手順を参考にし、本番環境（AWS）とローカル環境の構築を行ってください。

### [LINE チャネルの作成](./docs/liff-channel-create.md)
### [バックエンドの構築](./docs/back-end-construction.md)
### [本番（AWS）フロントエンド環境構築](./docs/front-end-construction.md)
### [ローカルフロントエンド環境構築](./docs/front-end-development-environment.md)
***
### [テストデータ投入](./docs/test-data-charge.md)
***
### [動作確認](./docs/validation.md)
***
# License
TableOrderの全てのファイルは、条件なしで自由にご利用いただけます。
自由にdownload&cloneをして、LINE APIを活用した素敵なアプリケーションの開発を始めてください！

See [LICENSE](LICENSE) for more detail.(English)

# How to contribute

First of all, thank you so much for taking your time to contribute! LINE API Use Case Hair Salon is not very different from any other open source projects. It will be fantastic if you help us by doing any of the following:

- File an issue in [the issue tracker](https://github.com/line/line-api-use-case-table-order/issues) to report bugs and propose new features and improvements.
- Ask a question using [the issue tracker](https://github.com/line/line-api-use-case-table-order/issues).
- Contribute your work by sending [a pull request](https://github.com/line/line-api-use-case-table-order/pulls).

When you are sending a pull request, you'll be considered as being aware of and accepting the followings.
- Grant [the same license](LICENSE) to the contribution
- Represent the contribution is your own creation
- Not expected to provide support for your contribution
