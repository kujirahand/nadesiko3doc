#!/bin/sh
set -eu

cd "$(dirname "$0")"
runtime_dir="$(pwd)/.runtime"
export PATH="$runtime_dir/bin:$runtime_dir/lnako/bin:$PATH"

npm install --no-save --package-lock=false nadesiko3@latest

skip() {
    case ",${DOCTEST_SKIP:-}," in
        *",$1,"*) return 0 ;;
        *) return 1 ;;
    esac
}

if ! skip gonako || ! skip lnako; then
    case "$(uname -s)-$(uname -m)" in
        Darwin-arm64) gonako_platform=darwin-arm64; lnako_platform=macos-arm64 ;;
        Linux-x86_64) gonako_platform=linux-amd64; lnako_platform=linux-x64 ;;
        *) echo '自動インストール非対応の環境です。gonako と lnako を PATH に用意してください。' >&2; exit 1 ;;
    esac
    mkdir -p "$runtime_dir"
    tmp_dir=$(mktemp -d "${TMPDIR:-/tmp}/nadesiko-doctest.XXXXXX")
    trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

    if ! skip gonako; then
        echo 'gonako の最新リリースをインストールします'
        curl -fsSL https://api.github.com/repos/kujirahand/nadesiko3go/releases/latest -o "$tmp_dir/gonako-release.json"
        gonako_url=$(node -e 'const r = require(process.argv[1]); const name = `gonako-${r.tag_name.replace(/^v/, "")}-${process.argv[2]}.zip`; const a = r.assets.find(a => a.name === name); if (!a) { console.error(`リリースに ${name} がありません`); process.exit(1); } console.log(a.browser_download_url)' "$tmp_dir/gonako-release.json" "$gonako_platform")
        curl -fL "$gonako_url" -o "$tmp_dir/gonako.zip"
        unzip -q "$tmp_dir/gonako.zip" -d "$tmp_dir/gonako"
        mkdir -p "$runtime_dir/bin"
        install -m 755 "$tmp_dir/gonako/gonako" "$runtime_dir/bin/gonako"
    fi
    if ! skip lnako; then
        echo 'lnako の最新リリースをインストールします'
        curl -fsSL https://api.github.com/repos/soramikan/lnako/releases/latest -o "$tmp_dir/lnako-release.json"
        lnako_url=$(node -e 'const r = require(process.argv[1]); const name = `lnako-${r.tag_name.replace(/^v/, "")}-${process.argv[2]}.tar.gz`; const a = r.assets.find(a => a.name === name); if (!a) { console.error(`リリースに ${name} がありません`); process.exit(1); } console.log(a.browser_download_url)' "$tmp_dir/lnako-release.json" "$lnako_platform")
        curl -fL "$lnako_url" -o "$tmp_dir/lnako.tar.gz"
        mkdir -p "$tmp_dir/lnako"
        tar -xzf "$tmp_dir/lnako.tar.gz" -C "$tmp_dir/lnako"
        lnako_bin=$(find "$tmp_dir/lnako" -type f -path '*/bin/lnako' -print | head -n 1)
        [ -n "$lnako_bin" ] || { echo 'lnako がアーカイブ内に見つかりません' >&2; exit 1; }
        mkdir -p "$runtime_dir/lnako"
        cp -R "$(dirname "$(dirname "$lnako_bin")")/." "$runtime_dir/lnako/"
    fi
fi
