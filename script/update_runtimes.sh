#!/usr/bin/env bash
# update_runtimes.sh --- なでしこ3の各ランタイムを最新リリースに揃えるスクリプト
#
# 対象ランタイム (DocTestの実行に使うCLI版):
#   cnako3  ... kujirahand/nadesiko3   (npmパッケージ nadesiko3 で配布)
#   gonako  ... kujirahand/nadesiko3go (GitHub ReleasesのZIPで配布)
#   lnako   ... soramikan/lnako        (GitHub Releasesのアーカイブで配布)
#
# 動作:
#   1. 各リポジトリの GitHub Releases (latest) のタグを取得する
#   2. ローカルにインストール済みのバージョンと比較する
#   3. 最新でない場合 (または未インストールの場合) は再インストールする
#   既に最新なら何もしない (冪等)。--check を付けると確認だけで終わる。
#
# 使い方:
#   script/update_runtimes.sh                 # 全ランタイムを確認し、必要なら更新
#   script/update_runtimes.sh --check         # バージョン確認のみ (更新しない)
#   script/update_runtimes.sh cnako3 lnako    # 対象を絞る
#   script/update_runtimes.sh --force gonako  # 最新でも再インストールする
#
# 環境変数:
#   BIN_DIR            gonako/lnako のリンクを置く場所 (既定: $HOME/.local/bin)
#   LNAKO_VARIANT      lnako の配布形態: standard (既定) / full (LLVM同梱)
#   CNAKO3_CMD / GONAKO_CMD / LNAKO_CMD
#                      バージョン確認に使うコマンドのパスを上書きする
#                      (開発用チェックアウトなど、配布物でないものを指す場合は
#                       その旨が分かるよう、更新対象から外れる点に注意)
#
# 注意:
#   - macOS / Linux 専用です (Windows は各ランタイムの公式手順を使ってください)。
#   - gonako-gui (GUI版) は対象外です。公式インストーラーか Homebrew で更新してください。
#   - Homebrew でインストールした gonako / lnako がある場合、PATH の優先順位に
#     よっては、そちらが使われ続けます。混在させず、どちらかに統一してください。
#   - lnako の AOT ビルド用ツールチェーン (LLVM) は別管理です。
#     `lnako toolchain install` / `lnako toolchain update` で更新してください。

set -uo pipefail

BIN_DIR="${BIN_DIR:-$HOME/.local/bin}"
LNAKO_VARIANT="${LNAKO_VARIANT:-standard}"

CHECK_ONLY=0
FORCE=0
TARGETS=()

usage() {
  sed -n '2,40p' "$0" | sed 's/^# \{0,1\}//'
}

for arg in "$@"; do
  case "$arg" in
    --check) CHECK_ONLY=1 ;;
    --force) FORCE=1 ;;
    -h|--help) usage; exit 0 ;;
    cnako3|gonako|lnako) TARGETS+=("$arg") ;;
    *) echo "エラー: 不明な引数です: $arg" >&2; exit 2 ;;
  esac
done
if [ "${#TARGETS[@]}" -eq 0 ]; then
  TARGETS=(cnako3 gonako lnako)
fi

OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
ARCH="$(uname -m)"
case "$OS" in
  darwin|linux) ;;
  *) echo "エラー: 未対応のOSです ($OS)。Windowsでは公式手順を使ってください。" >&2; exit 2 ;;
esac

FAILED=0

# GitHub Releases の最新タグを取得する (そのまま返す)
# 注意: タグの書式はリポジトリごとに違う (nadesiko3/nadesiko3go は "3.8.12"、
# lnako は "v0.2.5")。ダウンロードURLにはタグをそのまま使い、
# バージョン比較のときだけ先頭の v を取り除くこと。
latest_tag() {
  local repo="$1" tag=""
  tag="$(curl -fsSL "https://api.github.com/repos/${repo}/releases/latest" 2>/dev/null \
    | grep '"tag_name":' | head -n 1 | sed -E 's/.*"([^"]+)".*/\1/' || true)"
  if [ -z "$tag" ] && command -v gh >/dev/null 2>&1; then
    tag="$(gh release view --repo "$repo" --json tagName --jq .tagName 2>/dev/null || true)"
  fi
  echo "$tag"
}

# タグから先頭の v を取り除いたバージョン番号を返す
tag_version() {
  echo "${1#v}"
}

# コマンドの場所を表示する (なければ空)
find_cmd() {
  local override="$1" name="$2"
  if [ -n "$override" ]; then echo "$override"; return; fi
  command -v "$name" 2>/dev/null || true
}

# ---------------------------------------------------------------- cnako3
check_cnako3() {
  local latest; latest="$(tag_version "$1")"
  local cmd; cmd="$(find_cmd "${CNAKO3_CMD:-}" cnako3)"
  local local_ver=""
  if [ -n "$cmd" ]; then
    # 出力例: v3.8.12
    local_ver="$("$cmd" --version 2>/dev/null | tr -d 'v' | head -n 1 | tr -d '[:space:]')"
  fi
  echo "[cnako3] ローカル: ${local_ver:-(未インストール)} / 最新: ${latest}  (コマンド: ${cmd:-なし})"
  if [ "$local_ver" = "$latest" ] && [ "$FORCE" -eq 0 ]; then
    echo "[cnako3] 最新です。何もしません。"
    return 0
  fi
  if [ "$CHECK_ONLY" -eq 1 ]; then
    echo "[cnako3] 更新が必要です (--check のため実行しません)"
    return 0
  fi
  if ! command -v npm >/dev/null 2>&1; then
    echo "[cnako3] エラー: npm が見つかりません。先に Node.js (v22以上) をインストールしてください。" >&2
    return 1
  fi
  echo "[cnako3] npm install -g nadesiko3@${latest} を実行します..."
  if npm install -g "nadesiko3@${latest}"; then
    local new_cmd; new_cmd="$(find_cmd "${CNAKO3_CMD:-}" cnako3)"
    echo "[cnako3] 更新後のバージョン: $("$new_cmd" --version 2>/dev/null)"
  else
    echo "[cnako3] エラー: npm install に失敗しました。" >&2
    return 1
  fi
}

# ---------------------------------------------------------------- gonako
install_gonako() {
  local tag="$1" ver; ver="$(tag_version "$tag")"
  local gos goarch zip url tmpdir
  gos="$OS"
  case "$ARCH" in
    x86_64|amd64) goarch="amd64" ;;
    arm64|aarch64) goarch="arm64" ;;
    *) echo "[gonako] エラー: 未対応のCPUです ($ARCH)" >&2; return 1 ;;
  esac
  zip="gonako-${ver}-${gos}-${goarch}.zip"
  url="https://github.com/kujirahand/nadesiko3go/releases/download/${tag}/${zip}"
  tmpdir="$(mktemp -d)"
  echo "[gonako] ${url} をダウンロードします..."
  if ! curl -fSL "$url" -o "$tmpdir/$zip"; then
    echo "[gonako] エラー: ダウンロードに失敗しました。" >&2
    rm -rf "$tmpdir"; return 1
  fi
  unzip -q -o "$tmpdir/$zip" -d "$tmpdir/out"
  mkdir -p "$BIN_DIR"
  # ZIPの直下に gonako バイナリが入っている
  if [ -f "$tmpdir/out/gonako" ]; then
    install -m 755 "$tmpdir/out/gonako" "$BIN_DIR/gonako"
  else
    echo "[gonako] エラー: ZIP内に gonako バイナリが見つかりません。" >&2
    rm -rf "$tmpdir"; return 1
  fi
  rm -rf "$tmpdir"
  echo "[gonako] $BIN_DIR/gonako にインストールしました。"
}

check_gonako() {
  local tag="$1" latest; latest="$(tag_version "$tag")"
  local cmd; cmd="$(find_cmd "${GONAKO_CMD:-}" gonako)"
  local local_ver=""
  if [ -n "$cmd" ]; then
    # 出力例: gonako v3.8.12 (linux/amd64)
    local_ver="$("$cmd" version 2>/dev/null | sed -E 's/^gonako v([0-9.]+).*/\1/' | head -n 1)"
  fi
  echo "[gonako] ローカル: ${local_ver:-(未インストール)} / 最新: ${latest}  (コマンド: ${cmd:-なし})"
  if [ "$local_ver" = "$latest" ] && [ "$FORCE" -eq 0 ]; then
    echo "[gonako] 最新です。何もしません。"
    return 0
  fi
  if [ "$CHECK_ONLY" -eq 1 ]; then
    echo "[gonako] 更新が必要です (--check のため実行しません)"
    return 0
  fi
  install_gonako "$tag" || return 1
  echo "[gonako] 更新後のバージョン: $("$BIN_DIR/gonako" version 2>/dev/null)"
  if [ -n "$cmd" ] && [ "$cmd" != "$BIN_DIR/gonako" ]; then
    echo "[gonako] 注意: 既存の gonako は $cmd にあります。PATH の優先順位によっては古い方が使われます。"
  fi
}

# ---------------------------------------------------------------- lnako
install_lnako() {
  local tag="$1" ver; ver="$(tag_version "$tag")"
  local platform archive url tmpdir dest_root dest
  case "$OS/$ARCH" in
    darwin/arm64|darwin/aarch64) platform="macos-arm64" ;;
    linux/x86_64|linux/amd64) platform="linux-x64" ;;
    *) echo "[lnako] エラー: 配布アーカイブのない環境です ($OS/$ARCH)。Homebrew かソースビルドを使ってください。" >&2; return 1 ;;
  esac
  archive="lnako-${ver}-${platform}"
  if [ "$LNAKO_VARIANT" = "full" ]; then
    archive="${archive}-full"
  fi
  url="https://github.com/soramikan/lnako/releases/download/${tag}/${archive}.tar.gz"
  tmpdir="$(mktemp -d)"
  echo "[lnako] ${url} をダウンロードします..."
  if ! curl -fSL "$url" -o "$tmpdir/${archive}.tar.gz"; then
    echo "[lnako] エラー: ダウンロードに失敗しました。" >&2
    rm -rf "$tmpdir"; return 1
  fi
  # .sha256 が配布されているので照合する (取得できた場合のみ)
  if curl -fsSL "$url.sha256" -o "$tmpdir/${archive}.tar.gz.sha256" 2>/dev/null; then
    if command -v sha256sum >/dev/null 2>&1; then
      (cd "$tmpdir" && sha256sum -c "${archive}.tar.gz.sha256") || {
        echo "[lnako] エラー: SHA-256 が一致しません。中止します。" >&2
        rm -rf "$tmpdir"; return 1; }
    elif command -v shasum >/dev/null 2>&1; then
      (cd "$tmpdir" && shasum -a 256 -c "${archive}.tar.gz.sha256") || {
        echo "[lnako] エラー: SHA-256 が一致しません。中止します。" >&2
        rm -rf "$tmpdir"; return 1; }
    fi
    echo "[lnako] SHA-256 を確認しました。"
  fi
  tar -xzf "$tmpdir/${archive}.tar.gz" -C "$tmpdir"
  dest_root="${LNAKO_INSTALL_DIR:-$HOME/.local/opt}"
  dest="$dest_root/$archive"
  mkdir -p "$dest_root" "$BIN_DIR"
  rm -rf "$dest"
  # アーカイブ直下のフォルダ (bin/ lib/ など) の構造を保ったまま配置する。
  # bin/lnako 単体だけを取り出してはいけない。
  mv "$tmpdir/$archive" "$dest"
  ln -sf "$dest/bin/lnako" "$BIN_DIR/lnako"
  rm -rf "$tmpdir"
  echo "[lnako] $dest に配置し、$BIN_DIR/lnako からリンクしました。"
}

check_lnako() {
  local tag="$1" latest; latest="$(tag_version "$tag")"
  local cmd; cmd="$(find_cmd "${LNAKO_CMD:-}" lnako)"
  local local_ver=""
  if [ -n "$cmd" ]; then
    # 出力例: lnako 0.2.5
    local_ver="$("$cmd" --version 2>/dev/null | sed -E 's/^lnako ([0-9.]+).*/\1/' | head -n 1)"
  fi
  echo "[lnako] ローカル: ${local_ver:-(未インストール)} / 最新: ${latest}  (コマンド: ${cmd:-なし})"
  if [ "$local_ver" = "$latest" ] && [ "$FORCE" -eq 0 ]; then
    echo "[lnako] 最新です。何もしません。"
    return 0
  fi
  if [ "$CHECK_ONLY" -eq 1 ]; then
    echo "[lnako] 更新が必要です (--check のため実行しません)"
    return 0
  fi
  install_lnako "$tag" || return 1
  echo "[lnako] 更新後のバージョン: $("$BIN_DIR/lnako" --version 2>/dev/null)"
  if [ -n "$cmd" ]; then
    local resolved; resolved="$(command -v lnako 2>/dev/null || true)"
    if [ "$resolved" != "$BIN_DIR/lnako" ]; then
      echo "[lnako] 注意: PATH 上の lnako は $resolved です。$BIN_DIR が PATH の先にあるか確認してください。"
    fi
  fi
}

# ---------------------------------------------------------------- main
echo "== なでしこ3 ランタイム更新チェック (OS: $OS / ARCH: $ARCH) =="
echo "   BIN_DIR: $BIN_DIR"
case ":$PATH:" in
  *":$BIN_DIR:"*) ;;
  *) echo "   注意: BIN_DIR が PATH に含まれていません。シェルの設定に追加してください。" ;;
esac

for target in "${TARGETS[@]}"; do
  case "$target" in
    cnako3)
      latest="$(latest_tag kujirahand/nadesiko3)"
      if [ -z "$latest" ]; then echo "[cnako3] エラー: 最新版を取得できませんでした。" >&2; FAILED=1; continue; fi
      check_cnako3 "$latest" || FAILED=1
      ;;
    gonako)
      latest="$(latest_tag kujirahand/nadesiko3go)"
      if [ -z "$latest" ]; then echo "[gonako] エラー: 最新版を取得できませんでした。" >&2; FAILED=1; continue; fi
      check_gonako "$latest" || FAILED=1
      ;;
    lnako)
      latest="$(latest_tag soramikan/lnako)"
      if [ -z "$latest" ]; then echo "[lnako] エラー: 最新版を取得できませんでした。" >&2; FAILED=1; continue; fi
      check_lnako "$latest" || FAILED=1
      ;;
  esac
done

if [ "$FAILED" -ne 0 ]; then
  echo "== 一部のランタイムで問題がありました ==" >&2
  exit 1
fi
echo "== 完了 =="
