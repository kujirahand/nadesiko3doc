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

また、[just](https://github.com/casey/just)をインストールすることをお勧めします。justを使うことで、各種操作を簡単に行えます。

#### justを使ったサーバー起動

以下のコマンドを実行するとPHPのWebサーバーが起動します。

```sh
just server
```

#### 直接PHPを実行する場合

以下のコマンドでもPHPのWebサーバーが起動します。

```sh
cd nadesiko3doc
php -S localhost:8888
```

Webブラウザを開いて「localhost:8888」にアクセスします。
管理者のメールアドレスとパスワードの指定画面が出ますので任意のものを指定してください。
この設定は、Konawiki3を使うためのもので、リポジトリには反映されるものではありません。
すると、FrontPageにアクセスするように言われますので、リンクをクリックします。

### justコマンドの使い方

このプロジェクトでは、[just](https://github.com/casey/just)を使って各種操作を簡単に行えます。
justをインストールした後、以下のコマンドが利用できます。

```sh
# 利用可能なコマンド一覧を表示
just

# PHPの開発サーバーを起動
just server

# コマンド一覧をDBに変換
just cmd2db

# 解説がない命令を一覧表示
just enum-blank

# 全スクリプトを実行（cmd2db + enum-blank）
just build

# メタ情報を更新
just update-meta

# npmの依存関係をインストール
just install-deps

# 開発環境をセットアップ
just setup
```

### Konawiki3の設定を変更しよう

続いて、Konawikiの設定画面が出ます。下記の設定を行って[Save]ボタンを押します。
なでしこ３のマニュアルに近い設定になります。

- 項目 `Header/Footer > allpage_header` へ `#nako3doc` と記述。
- 項目 `Options > plugin_disallow` から `html,htmlshow` を削除。

### nako3docの設定

プラグイン #nako3doc は、Wikiになでしこの命令を自動挿入するプラグインです。
`data/nako3commands.db` を参照します。
このファイルは、なでしこのバージョンアップにより自動的に更新されるため、このファイルを編集しないでください。

### Konawiki3用プラグインに関する補足

このWiki専用のプラグインは、Konawiki3本体(`konawiki3/kona3engine/plugins/`)には入れず、このリポジトリの `data/.plugins/` に置く「ローカルプラグイン」として管理しています。そのため、プラグインの修正もマニュアルと同じくこのリポジトリへのプルリクエストで行います。

`data/.plugins/` には次のファイルがあります。

| ファイル | 役割 |
|---|---|
| `nako3doc.inc.php` | 本体です。命令ページへの命令情報(カテゴリ/環境/種類/引数/説明)の自動挿入と、機能順の命令一覧の生成を行います。プラグインアクションによる命令検索(`index.php?<ページ>&plugin&name=nako3doc&q=<命令名>`)も持ちます。 |
| `nako3doc2kana.inc.php` | カナ順・ヨミ順の命令一覧を生成します。 |
| `nako3doc_utils.php` | プラグイン本体ではなく、上記2つから共通で使う部品です。ページ名や引数に応じて、参照する命令一覧DB(`nako3commands.db` / `gonako-commands.db` / `lnako-commands.db`)を切り替えます。 |

主な使い方は次のとおりです。

| 書式 | 動作 |
|---|---|
| `#nako3doc` | 引数なしで使います。全ページ共通ヘッダー(`allpage_header`)に設定しておくと、表示中のページが命令ページであれば、その命令の情報表を自動で表示します。 |
| `#nako3doc(list-func,<ランタイム>)` | 機能順の命令一覧を表示します。`data/wnako.txt` や `data/gonako.txt` など、各ランタイムの一覧ページで使います。 |
| `#nako3doc(plugins)` | プラグイン一覧を表示します。`data/プラグイン一覧.txt` で使います。 |
| `#nako3doc2kana(kana,<ランタイム>)` | カナ順の命令一覧を表示します。`yomi` を指定するとヨミ順になります。従来の `#nako3doc(list-kana)` / `#nako3doc(list-yomi)` も互換のため利用できます。 |

Konawiki3のローカルプラグイン共通のルールとして、次の点も覚えておいてください。

- ファイル名は「プラグイン名.inc.php」で、実行関数は `kona3plugins_<プラグイン名>_execute($args)` です。必要に応じて `_init()` や、URLから呼ばれる `_action()` も定義できます。
- プラグインの検索順序は、標準プラグイン(`kona3engine/plugins/`)が先で、ローカルプラグイン(`data/.plugins/`)はその次です。同名のプラグインがある場合は標準プラグインが優先されるため、ローカルプラグインで標準プラグインを上書きすることはできません。
- 設定の `plugin_disallow` に名前を書くと、標準・ローカルを問わずそのプラグインが無効になります(前節の設定で `html,htmlshow` を許可しているのはこのためです)。`plugin_alias` で別名を付けることもできます。
- インストール済みプラグインの一覧は `index.php?FrontPage&plugin&name=pluginlist` で確認でき、標準プラグインとローカルプラグインの両方が表示されます。各ファイルの先頭コメントの1行目が説明として使われます。
- ローカルプラグインはPHPコードとして実行されます。信頼できるファイルだけを置き、利用者の入力を出力に含めるときは `htmlspecialchars` でエスケープしてください。
- `data/.plugins/` はこのリポジトリで編集してよい対象です。一方、`konawiki3/`・`private/`・`cache/`・`attach/` と、自動生成される `data/.meta/` は編集しません(詳しくは `data/AGENTS.md` を参照してください)。

## マニュアルを編集しよう

### 命令名とファイル名の関係

なでしこ3の命令は「{プラグイン名}/{命令名}.txt」という名前で管理します。

例えば、システム命令の「足す」であれば送り仮名を省略した以下の形式でファイル名を記述します。

```
data/plugin_system/足.txt
```

### ランタイムごとのディレクトリルール

なでしこ3には複数のランタイムがあり、命令マニュアルをどのディレクトリに置くかはランタイムごとに異なります。ページ名は、`data/` からの相対パスから拡張子 `.txt` を除いたものになります。新しい命令のマニュアルを追加するときは、対象ランタイムのルールに従って配置してください。

| ランタイム | 命令ファイルの置き場所 | 命令一覧DB |
|---|---|---|
| なでしこ3(wnako / cnako / enako / phpnako) | `data/plugin_*/`・`data/nadesiko3-*/`(プラグインごとのディレクトリ) | `data/nako3commands.db` |
| gonako(なでしこ3 Go版) | `data/gonako/`(全命令を1つのディレクトリに配置) | `data/gonako-commands.db` |
| lnako(なでしこ3 高速ネイティブ版) | `data/lnako/`・`data/lnako_node/`・`data/lnako_lowlevel/` | `data/lnako-commands.db` |

#### なでしこ3(wnako / cnako / enako / phpnako)

- 命令ファイルは `data/{プラグイン名}/{命令名}.txt` とし、プラグインごとにディレクトリを分けます(`plugin_system` や `plugin_browser` などの `plugin_*` と、`nadesiko3-sqlite3` や `nadesiko3-music` などの `nadesiko3-*` があります)。
- プラグインの概要ページは、原則として `data/{プラグイン名}.txt` に置きます。
- どのランタイムで使える命令かは、ディレクトリではなくDBのプラグイン情報(`nakotype`)で区別します。各ランタイムの一覧ページ(`data/wnako.txt`・`data/cnako.txt`・`data/enako.txt`・`data/phpnako.txt`)が `#nako3doc(list-func,<ランタイム>)` で絞り込んで表示します。
- 命令一覧DB `data/nako3commands.db` は、`script/cmd2db.nako3` が なでしこ3 の `batch/command.txt` から生成します。直接編集しないでください。

#### gonako(なでしこ3 Go版)

- 命令ファイルは `data/gonako/{命令名}.txt` とし、プラグインごとに分けず、全命令を1つのディレクトリに平置きします。DB上でもプラグイン名は `gonako` で統一されます。
- 一覧ページは `data/gonako.txt`(機能順)と `data/gonako-カナ順.txt`(カナ順)です。
- なでしこ3と共通の命令の多くは、中身が `#include(plugin_*/<命令名>)` とだけ書かれた別名(エイリアス)ファイルです。別名ファイルは変更せず、説明を直すときは参照先の `plugin_*` 側のファイルを編集してください。gonako固有の命令は、`data/gonako/` に直接マニュアルを書きます。

#### lnako(なでしこ3 高速ネイティブ版)

- 命令ファイルは、役割ごとに次の3つのディレクトリに分けます。
  - `data/lnako/` --- 基本命令(`plugin_system`・`plugin_math` などと互換)
  - `data/lnako_node/` --- PC・コンソール向け命令(`plugin_node` 互換)
  - `data/lnako_lowlevel/` --- lnako独自の低レイヤーAPI命令
- 一覧ページは `data/lnako.txt`(機能順)と `data/lnako-カナ順.txt`(カナ順)で、`lnako_node`・`lnako_lowlevel` の概要ページもそれぞれ用意されています。
- これら3つのディレクトリのファイルと命令一覧DB `data/lnako-commands.db` は、`script/generate_lnako_docs.py` で生成します。生成対象のファイルを直接編集しないでください。
- 生成後のファイルを見ると、`data/lnako/` のファイルは現状すべて `#include(...)` の別名ファイルになっており、説明の実体は参照先の `plugin_*` 側にあります。`lnako_node` は別名ファイルと実体のファイルが混在し、`lnako_lowlevel` は `#include` ではない lnako固有の内容になっています。

#### ランタイム共通のページ

チュートリアル(`data/チュートリアル/`)や文法(`data/文法/`)、FAQ(`data/FAQ/`)などのページは、特定のランタイム専用ではなく共通のページとして `data/` 直下に置きます。

なお、いずれのランタイムでも、ファイルの文字コードはUTF-8、改行コードはLFに統一し、ファイル名の末尾に空白を入れないでください(詳しくは `data/AGENTS.md` を参照してください)。

### プルリクエストの送信

マニュアルの修正を行った後、修正点をコミットして`git push`します。
その後、GitHubのページにアクセスして、プルリクエストを送信してください。

