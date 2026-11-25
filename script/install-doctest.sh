#!/bin/sh
set -eu

cd "$(dirname "$0")"
runtime_dir="$(pwd)/.runtime"
export PATH="$PATH:$runtime_dir/bin:$runtime_dir/lnako/bin"

if [ ! -x node_modules/.bin/cnako3 ] || [ ! -f node_modules/nadesiko3/batch/doctest.nako3 ]; then
    npm ci
fi

skip() {
    case ",${DOCTEST_SKIP:-}," in
        *",$1,"*) return 0 ;;
        *) return 1 ;;
    esac
}

if { ! skip gonako && ! command -v gonako >/dev/null 2>&1; } ||
   { ! skip lnako && ! command -v lnako >/dev/null 2>&1; }; then
    case "$(uname -s)-$(uname -m)" in
        Darwin-arm64) gonako_platform=darwin-arm64; lnako_platform=macos-arm64 ;;
        Linux-x86_64) gonako_platform=linux-amd64; lnako_platform=linux-x64 ;;
        *) echo '自動インストール非対応の環境です。gonako と lnako を PATH に用意してください。' >&2; exit 1 ;;
    esac
    mkdir -p "$runtime_dir"
    tmp_dir=$(mktemp -d "${TMPDIR:-/tmp}/nadesiko-doctest.XXXXXX")
    trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

    if ! skip gonako && ! command -v gonako >/dev/null 2>&1; then
        echo 'gonako 3.8.13 をインストールします'
        curl -fL "https://github.com/kujirahand/nadesiko3go/releases/download/3.8.13/gonako-3.8.13-${gonako_platform}.zip" -o "$tmp_dir/gonako.zip"
        unzip -q "$tmp_dir/gonako.zip" -d "$tmp_dir/gonako"
        mkdir -p "$runtime_dir/bin"
        install -m 755 "$tmp_dir/gonako/gonako" "$runtime_dir/bin/gonako"
    fi
    if ! skip lnako && ! command -v lnako >/dev/null 2>&1; then
        echo 'lnako 0.2.4 をインストールします'
        curl -fL "https://github.com/soramikan/lnako/releases/download/v0.2.4/lnako-0.2.4-${lnako_platform}.tar.gz" -o "$tmp_dir/lnako.tar.gz"
        mkdir -p "$tmp_dir/lnako"
        tar -xzf "$tmp_dir/lnako.tar.gz" -C "$tmp_dir/lnako"
        lnako_bin=$(find "$tmp_dir/lnako" -type f -path '*/bin/lnako' -print | head -n 1)
        [ -n "$lnako_bin" ] || { echo 'lnako がアーカイブ内に見つかりません' >&2; exit 1; }
        mkdir -p "$runtime_dir/lnako"
        cp -R "$(dirname "$(dirname "$lnako_bin")")/." "$runtime_dir/lnako/"
    fi
fi
