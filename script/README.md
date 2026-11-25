# DocTest

Node.js 22 以降、npm、curl、tar、unzip を用意し、リポジトリのルートで `just doctest` を実行します。`just install` だけを実行して依存関係を準備することもできます。実行時には常に npm の最新版の cnako3 と、GitHub の最新リリースの gonako と lnako を取得します。gonako と lnako は `script/.runtime/` にインストールされ、PATH 上のコマンドより優先されます。自動インストールは macOS arm64 と Linux x86_64 に対応します。

`DOCTEST_SKIP=gonako,lnako just doctest` のように指定すると、対象のインストールとテストを省略できます。個別の npm コマンドを実行する場合、ローカルにインストールされたランタイムは `script/.runtime/bin` と `script/.runtime/lnako/bin` を PATH に追加してください。

- [cnako3 のインストール](https://nadesi.com/v3/doc/index.php?FAQ%2F%E3%81%AA%E3%81%A7%E3%81%97%E3%81%933%E3%82%92%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%81%97%E3%81%A6%E4%BD%BF%E3%81%86%E3%81%AB%E3%81%AF%EF%BC%9F&show)
- [gonako のインストール](https://nadesi.com/v3/doc/index.php?gonako&show)
- [lnako のインストール](https://nadesi.com/v3/doc/index.php?lnako&show)

`{{{#nako3` ブロック内の `### 表示結果: ...` と続く `### ...` 行を期待値として照合します。`GO表示結果` は gonako、`lnako表示結果` は lnako、`表示結果` は cnako3 で実行します。

| コマンド | 対象 |
| --- | --- |
| `npm run doctest:all` | `data/` 以下を再帰的に探索し、ラベルごとに実行 |
| `npm run doctest:gonako` | `data/gonako` の `GO表示結果` |
| `npm run doctest:lnako` | `data/lnako_lowlevel` と `data/lnako_node` の `lnako表示結果` |
| `npm run doctest:cnako3` | `plugin_system` を除く `data/plugin_*` の `表示結果` |
| `npm run doctest:system` | `data/plugin_system` と `data/文法` の `表示結果` |

各ランナーの結果を表示し、いずれかが失敗するか必要な実行ファイルが見つからない場合は終了コードが非ゼロになります。意図的に省略する場合は、例えば `DOCTEST_SKIP=gonako,lnako npm run doctest:all` とします。省略はサマリーに表示され、失敗には数えません。DocTest はサンプルを実際に実行します。
