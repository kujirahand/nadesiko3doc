# なでしこ3 マニュアルプロジェクト

日本語プログラミング言語「なでしこ3」のマニュアルを作成するプロジェクトです。GitHubでマニュアル作成に参加できます。

- [なでしこ3](https://nadesi.com/doc3/)
- [なでしこ3マニュアル](https://nadesi.com/v3/doc/)

## プロジェクトの開始方法

マニュアルは基本的にテキストファイルですが、Konawiki3を利用することでWiki上で気軽にマニュアルの作成ができます。

```
# マニュアル作成ツールのkonawiki3を取得
git clone git@github.com:kujirahand/konawiki3.git
# なでしこ3のマニュアルを取得
git clone git@github.com:kujirahand/nadesiko3doc.git
# (必要に応じて)なでしこ3のリポジトリ
git clone git@github.com:kujirahand/nadesiko3
```

なお、これによって以下のようなファイル構造となります。

```
+
| - <konawiki3>
| - <nadesiko3>
| - <nadesiko3doc>
|   | - index.php
|   | - konawiki3.ini.php
```

nadesiko3doc/index.php から konawiki3/kona3engine を参照してWikiを動かすことができます。

### ツールの開始

PHP7をインストールしてパスを通しておいてください。以下のコマンドを実行するとPHPのWebサーバーが起動します。

```
cd nadesiko3doc
php -S localhost:8888
```

そして、Webブラウザで「localhost:8888」にアクセスし、ユーザー名「nako3」、パスワード「nako3」でログインして作業できます。


### 命令名とファイル名の関係

なでしこ3の命令は「{プラグイン名}/{命令名}__解説.txt」という名前で管理します。

例えば、システム命令の「足す」であれば送り仮名を省略した以下の形式でファイル名を記述します。

```
data/plugin_system/足__解説.txt
```

なでしこのソースコードから自動生成できる基本的なデータは次の形式で書き出されます。そのため「{プラグイン名}/{命令名}.txt」というファイルは編集しても上書きされてしまうので注意してください。

```
# 編集してはいけないファイル
data/plugin_system/足.txt
```





