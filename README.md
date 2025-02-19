# なでしこ3 マニュアルプロジェクト

日本語プログラミング言語「なでしこ3」のマニュアルを作成するプロジェクトです。
GitHubを通じてマニュアル作成に参加できます。マニュアルはテキストベースのWikiとなっており誰でもマニュアル作成に参加できます。

- [なでしこ3マニュアル(Wiki)](https://nadesi.com/v3/doc/)

マニュアル製作のために、konawiki3を利用しています。

- [Konawiki3](https://github.com/kujirahand/konawiki3)
- [なでしこ3](https://nadesi.com/doc3/)

以下のURLでマニュアルへの貢献度が確認できます。

- [GitHub > 貢献度グラフ](https://github.com/kujirahand/nadesiko3doc/graphs/contributors)

## プロジェクトの開始方法

マニュアルプロジェクトに参加するには、このリポジトリを直接編集して、プルリクエストを送信してください。
Konawiki3は、本プロジェクトのために大幅に改良された専用のWikiです。

Gitをインストールした後、ターミナルで下記のコマンドを実行してください。

```sh
# マニュアル作成ツールのkonawiki3を取得
git clone git@github.com:kujirahand/konawiki3.git
# なでしこ3のマニュアルを取得
git clone git@github.com:kujirahand/nadesiko3doc.git
# (必要に応じて)なでしこ3のリポジトリ
git clone git@github.com:kujirahand/nadesiko3.git
```

上記コマンドを実行すると、次のようなファイル構造となります。

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

PHP8以降をインストールしてパスを通しておいてください。下記のパッケージが必要です。

- `php-mbstring`
- `php-pdo-sqlite`

以下のコマンドを実行するとPHPのWebサーバーが起動します。

```sh
cd nadesiko3doc
php -S localhost:8888
```

Webブラウザを開いて「localhost:8888」にアクセスします。
管理者のメールアドレスとパスワードの指定画面が出ますので任意のものを指定してください。
この設定は、Konawiki3を使うためのもので、リポジトリには反映されるものではりません。
すると、FrontPageにアクセスするように言われますので、リンクをクリックします。

### Konawiki3の設定を変更しよう

続いて、Konawikiの設定画面が出ます。下記の設定を行って[Save]ボタンを押します。
なでしこ３のマニュアルに近い設定になります。

- 項目 `Header/Footer > allpage_header` へ `#nako3doc` と記述。
- 項目 `Options > plugin_disallow` から `html,htmlshow` を削除。

### nako3docの設定

プラグイン #nako3doc は、Wikiになでしこの命令を自動挿入するプラグインです。
`data/nako3commands.db` を参照します。
このファイルは、なでしこのバージョンアップにより自動的に更新されるため、このファイルを編集しないでください。

## マニュアルを編集しよう

### 命令名とファイル名の関係

なでしこ3の命令は「{プラグイン名}/{命令名}.txt」という名前で管理します。

例えば、システム命令の「足す」であれば送り仮名を省略した以下の形式でファイル名を記述します。

```
data/plugin_system/足.txt
```

### プルリクエストの送信

マニュアルの修正を行った後、修正点をコミットして`git push`します。
その後、GitHubのページにアクセスして、プルリクエストを送信してください。

