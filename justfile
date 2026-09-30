# なでしこ3マニュアルプロジェクト用justfile

# デフォルトコマンド
default:
    @just --list

# PHPの開発サーバーを起動
server:
    php -S localhost:8888

# コマンド一覧をDBに変換
cmd2db:
    cd script && cnako3 cmd2db.nako3

# 解説がない命令を一覧表示
enum-blank:
    cd script && cnako3 enum_blank_command.nako3

# 全スクリプトを実行（cmd2db + enum-blank）
build: cmd2db enum-blank

# メタ情報を更新
update-meta:
    php script/update-meta.php

# npmの依存関係をインストール
install-deps:
    cd script && npm install

# 開発環境をセットアップ
setup: install-deps
    @echo "セットアップが完了しました"

# ヘルプを表示
help:
    @echo "なでしこ3マニュアルプロジェクト"
    @echo ""
    @echo "利用可能なコマンド:"
    @echo "  just server       - PHP開発サーバーを起動 (localhost:8888)"
    @echo "  just cmd2db       - コマンド一覧をDBに変換"
    @echo "  just enum-blank   - 解説がない命令を一覧表示"
    @echo "  just build        - 全スクリプトを実行 (cmd2db + enum-blank)"
    @echo "  just update-meta  - メタ情報を更新"
    @echo "  just install-deps - npmの依存関係をインストール"
    @echo "  just setup        - 開発環境をセットアップ"
    @echo "  just help         - このヘルプを表示"
