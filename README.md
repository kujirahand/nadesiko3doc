# なでしこ3 マニュアルプロジェクト

日本語プログラミング言語「なでしこ3」のマニュアルを作成するプロジェクトです。GitHubでマニュアル作成に参加できます。

- [なでしこ3](https://nadesi.com/doc3/)

## プロジェクトの開始方法

マニュアルは基本的にテキストファイルですが、Konawiki3を利用することでWiki上で気軽にマニュアルの作成ができます。

```
# マニュアル作成ツールのkonawiki3を取得
git clone git@github.com:kujirahand/konawiki3.git

# konawiki3のwikiデータが格納されているディレクトリに移動
cd konawiki3/data

# なでしこ3のマニュアルを取得
git clone git@github.com:kujirahand/nadesiko3doc.git
```

### ツールの開始

PHP7をインストールしてパスを通しておいてください。

```
cd konawiki3
php -S localhost:8888
```

Webブラウザで「localhost:8888」にアクセスし、ユーザー名「nako3」、パスワード「nako3」でログインして作業できます。








