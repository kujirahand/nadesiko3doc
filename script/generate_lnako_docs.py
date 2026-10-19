#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lnako (なでしこ3 高速ネイティブ版) のマニュアルページおよび data/lnako-commands.db を生成するスクリプト
- data/lnako/*.txt (392件)
- data/lnako_node/*.txt (107件)
- data/lnako_lowlevel/*.txt (63件)
- data/lnako.txt, data/lnako-カナ順.txt, data/lnako_node.txt, data/lnako_lowlevel.txt
- data/lnako-commands.db (SQLite)
"""
import os
import sqlite3

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
NAKO3_DB_PATH = os.path.join(DATA_DIR, 'nako3commands.db')
LNAKO_DB_PATH = os.path.join(DATA_DIR, 'lnako-commands.db')

LNAKO_STD = [['plugin_system', 'システム定数', 'ナデシコバージョン'],
 ['plugin_system', 'システム定数', 'ナデシコ言語バージョン'],
 ['plugin_system', 'システム定数', 'ナデシコエンジン'],
 ['plugin_system', 'システム定数', 'ナデシコ種類'],
 ['plugin_system', 'システム定数', 'はい'],
 ['plugin_system', 'システム定数', 'いいえ'],
 ['plugin_system', 'システム定数', '真'],
 ['plugin_system', 'システム定数', '偽'],
 ['plugin_system', 'システム定数', '永遠'],
 ['plugin_system', 'システム定数', 'オン'],
 ['plugin_system', 'システム定数', 'オフ'],
 ['plugin_system', 'システム定数', '改行'],
 ['plugin_system', 'システム定数', 'タブ'],
 ['plugin_system', 'システム定数', 'カッコ'],
 ['plugin_system', 'システム定数', 'カッコ閉'],
 ['plugin_system', 'システム定数', '波カッコ'],
 ['plugin_system', 'システム定数', '波カッコ閉'],
 ['plugin_system', 'システム定数', 'OK'],
 ['plugin_system', 'システム定数', 'NG'],
 ['plugin_system', 'システム定数', 'キャンセル'],
 ['plugin_system', 'システム定数', 'TRUE'],
 ['plugin_system', 'システム定数', 'FALSE'],
 ['plugin_system', 'システム定数', 'true'],
 ['plugin_system', 'システム定数', 'false'],
 ['plugin_system', 'システム定数', 'PI'],
 ['plugin_system', 'システム定数', '空'],
 ['plugin_system', 'システム定数', 'NULL'],
 ['plugin_system', 'システム定数', 'undefined'],
 ['plugin_system', 'システム定数', '未定義'],
 ['plugin_system', 'システム定数', 'エラーメッセージ'],
 ['plugin_system', 'システム定数', '対象'],
 ['plugin_system', 'システム定数', '対象キー'],
 ['plugin_system', 'システム定数', '回数'],
 ['plugin_system', 'システム定数', 'CR'],
 ['plugin_system', 'システム定数', 'LF'],
 ['plugin_system', 'システム定数', '非数'],
 ['plugin_system', 'システム定数', '無限大'],
 ['plugin_system', 'システム定数', '戻値無'],
 ['plugin_system', 'システム定数', '戻値有'],
 ['plugin_system', 'システム定数', '空配列'],
 ['plugin_system', 'システム定数', '空辞書'],
 ['plugin_system', 'システム定数', '空ハッシュ'],
 ['plugin_system', 'システム定数', '空オブジェクト'],
 ['plugin_system', 'システム定数', '真偽判定'],
 ['plugin_system', '敬語', 'ください'],
 ['plugin_system', '敬語', 'お願'],
 ['plugin_system', '敬語', 'です'],
 ['plugin_system', '敬語', '拝啓'],
 ['plugin_system', '敬語', '敬具'],
 ['plugin_system', '敬語', '礼節レベル取得'],
 ['plugin_system', '特殊命令', 'JS実行'],
 ['plugin_system', '特殊命令', 'JSオブジェクト取得'],
 ['plugin_system', '特殊命令', 'JS関数実行'],
 ['plugin_system', '特殊命令', 'ASYNC'],
 ['plugin_system', '特殊命令', 'AWAIT実行'],
 ['plugin_system', '特殊命令', 'JSメソッド実行'],
 ['plugin_system', '特殊命令', 'ナデシコ'],
 ['plugin_system', '特殊命令', 'ナデシコ続'],
 ['plugin_system', '特殊命令', '実行'],
 ['plugin_system', '特殊命令', '実行時間計測'],
 ['plugin_system', '特殊命令', '終'],
 ['plugin_system', 'デバッグ支援', 'デバッグ表示'],
 ['plugin_system', 'デバッグ支援', 'ハテナ関数設定'],
 ['plugin_system', 'デバッグ支援', 'ハテナ関数実行'],
 ['plugin_system', 'デバッグ支援', 'エラー発生'],
 ['plugin_system', 'デバッグ支援', '__DEBUG'],
 ['plugin_system', 'デバッグ支援', '__DEBUG強制待機'],
 ['plugin_system', 'デバッグ支援', '__DEBUGブレイクポイント一覧'],
 ['plugin_system', 'デバッグ支援', '__DEBUG待機フラグ'],
 ['plugin_system', 'デバッグ支援', '__DEBUG_BP_WAIT'],
 ['plugin_system', 'デバッグ支援', 'グローバル関数一覧取得'],
 ['plugin_system', 'デバッグ支援', 'システム関数一覧取得'],
 ['plugin_system', 'デバッグ支援', 'システム関数存在'],
 ['plugin_system', 'デバッグ支援', 'プラグイン一覧取得'],
 ['plugin_system', 'デバッグ支援', 'モジュール一覧取得'],
 ['plugin_system', 'デバッグ支援', '助詞一覧取得'],
 ['plugin_system', 'デバッグ支援', '予約語一覧取得'],
 ['plugin_system', 'プラグイン管理', 'プラグイン名'],
 ['plugin_system', 'プラグイン管理', 'プラグイン名設定'],
 ['plugin_system', 'プラグイン管理', '名前空間'],
 ['plugin_system', 'プラグイン管理', '名前空間設定'],
 ['plugin_system', 'プラグイン管理', '名前空間ポップ'],
 ['plugin_system', '四則演算', '足'],
 ['plugin_system', '四則演算', '合計'],
 ['plugin_system', '四則演算', '引'],
 ['plugin_system', '四則演算', '掛'],
 ['plugin_system', '四則演算', '倍'],
 ['plugin_system', '四則演算', '割'],
 ['plugin_system', '四則演算', '割余'],
 ['plugin_system', '四則演算', '偶数'],
 ['plugin_system', '四則演算', '奇数'],
 ['plugin_system', '四則演算', '二乗'],
 ['plugin_system', '四則演算', 'べき乗'],
 ['plugin_system', '四則演算', '以上'],
 ['plugin_system', '四則演算', '以下'],
 ['plugin_system', '四則演算', '未満'],
 ['plugin_system', '四則演算', '超'],
 ['plugin_system', '四則演算', '等'],
 ['plugin_system', '四則演算', '等無'],
 ['plugin_system', '四則演算', '一致'],
 ['plugin_system', '四則演算', '不一致'],
 ['plugin_system', '四則演算', '範囲内'],
 ['plugin_system', '四則演算', '範囲'],
 ['plugin_system', '四則演算', '連続加算'],
 ['plugin_system', '四則演算', 'MAX'],
 ['plugin_system', '四則演算', '最大値'],
 ['plugin_system', '四則演算', 'MIN'],
 ['plugin_system', '四則演算', '最小値'],
 ['plugin_system', '四則演算', 'CLAMP'],
 ['plugin_system', '論理演算', '論理OR'],
 ['plugin_system', '論理演算', '論理AND'],
 ['plugin_system', '論理演算', '論理NOT'],
 ['plugin_system', 'ビット演算', 'OR'],
 ['plugin_system', 'ビット演算', 'AND'],
 ['plugin_system', 'ビット演算', 'XOR'],
 ['plugin_system', 'ビット演算', 'NOT'],
 ['plugin_system', 'ビット演算', 'SHIFT_L'],
 ['plugin_system', 'ビット演算', 'SHIFT_R'],
 ['plugin_system', 'ビット演算', 'SHIFT_UR'],
 ['plugin_system', '文字列処理', '文字数'],
 ['plugin_system', '文字列処理', '何文字目'],
 ['plugin_system', '文字列処理', 'CHR'],
 ['plugin_system', '文字列処理', 'ASC'],
 ['plugin_system', '文字列処理', '文字挿入'],
 ['plugin_system', '文字列処理', '文字検索'],
 ['plugin_system', '文字列処理', '追加'],
 ['plugin_system', '文字列処理', '一行追加'],
 ['plugin_system', '文字列処理', '連結'],
 ['plugin_system', '文字列処理', '文字列連結'],
 ['plugin_system', '文字列処理', '文字列分解'],
 ['plugin_system', '文字列処理', 'リフレイン'],
 ['plugin_system', '文字列処理', '出現回数'],
 ['plugin_system', '文字列処理', 'MID'],
 ['plugin_system', '文字列処理', '文字抜出'],
 ['plugin_system', '文字列処理', 'LEFT'],
 ['plugin_system', '文字列処理', '文字左部分'],
 ['plugin_system', '文字列処理', 'RIGHT'],
 ['plugin_system', '文字列処理', '文字右部分'],
 ['plugin_system', '文字列処理', '区切'],
 ['plugin_system', '文字列処理', '文字列分割'],
 ['plugin_system', '文字列処理', '切取'],
 ['plugin_system', '文字列処理', '範囲切取'],
 ['plugin_system', '文字列処理', '文字削除'],
 ['plugin_system', '文字列処理', '文字始'],
 ['plugin_system', '文字列処理', '文字終'],
 ['plugin_system', '文字列処理', '出現'],
 ['plugin_system', '置換・トリム', '置換'],
 ['plugin_system', '置換・トリム', '単置換'],
 ['plugin_system', '置換・トリム', 'トリム'],
 ['plugin_system', '置換・トリム', '空白除去'],
 ['plugin_system', '置換・トリム', '右トリム'],
 ['plugin_system', '置換・トリム', '左トリム'],
 ['plugin_system', '置換・トリム', '末尾空白除去'],
 ['plugin_system', '文字変換', '大文字変換'],
 ['plugin_system', '文字変換', '小文字変換'],
 ['plugin_system', '文字変換', '平仮名変換'],
 ['plugin_system', '文字変換', 'カタカナ変換'],
 ['plugin_system', '文字変換', '英数全角変換'],
 ['plugin_system', '文字変換', '英数半角変換'],
 ['plugin_system', '文字変換', '英数記号全角変換'],
 ['plugin_system', '文字変換', '英数記号半角変換'],
 ['plugin_system', '文字変換', 'カタカナ全角変換'],
 ['plugin_system', '文字変換', 'カタカナ半角変換'],
 ['plugin_system', '文字変換', '全角変換'],
 ['plugin_system', '文字変換', '半角変換'],
 ['plugin_system', '文字変換', '全角カナ一覧'],
 ['plugin_system', '文字変換', '全角カナ濁音一覧'],
 ['plugin_system', '文字変換', '半角カナ一覧'],
 ['plugin_system', '文字変換', '半角カナ濁音一覧'],
 ['plugin_system', '指定形式', '通貨形式'],
 ['plugin_system', '指定形式', 'ゼロ埋'],
 ['plugin_system', '指定形式', '空白埋'],
 ['plugin_system', '文字種類', 'かなか判定'],
 ['plugin_system', '文字種類', 'カタカナ判定'],
 ['plugin_system', '文字種類', '数字判定'],
 ['plugin_system', '文字種類', '数列判定'],
 ['plugin_system', '配列操作', '配列結合'],
 ['plugin_system', '配列操作', '配列只結合'],
 ['plugin_system', '配列操作', '配列検索'],
 ['plugin_system', '配列操作', '配列要素数'],
 ['plugin_system', '配列操作', '要素数'],
 ['plugin_system', '配列操作', 'LEN'],
 ['plugin_system', '配列操作', '配列挿入'],
 ['plugin_system', '配列操作', '配列一括挿入'],
 ['plugin_system', '配列操作', '配列ソート'],
 ['plugin_system', '配列操作', '配列数値変換'],
 ['plugin_system', '配列操作', '配列数値ソート'],
 ['plugin_system', '配列操作', '配列カスタムソート'],
 ['plugin_system', '配列操作', '配列逆順'],
 ['plugin_system', '配列操作', '配列シャッフル'],
 ['plugin_system', '配列操作', '配列削除'],
 ['plugin_system', '配列操作', '配列切取'],
 ['plugin_system', '配列操作', '配列取出'],
 ['plugin_system', '配列操作', '配列ポップ'],
 ['plugin_system', '配列操作', '配列プッシュ'],
 ['plugin_system', '配列操作', '配列追加'],
 ['plugin_system', '配列操作', '配列複製'],
 ['plugin_system', '配列操作', '配列範囲コピー'],
 ['plugin_system', '配列操作', '参照'],
 ['plugin_system', '配列操作', '配列参照'],
 ['plugin_system', '配列操作', '配列足'],
 ['plugin_system', '配列操作', '配列最大値'],
 ['plugin_system', '配列操作', '配列最小値'],
 ['plugin_system', '配列操作', '配列合計'],
 ['plugin_system', '配列操作', '配列入替'],
 ['plugin_system', '配列操作', '配列連番作成'],
 ['plugin_system', '配列操作', '配列要素作成'],
 ['plugin_system', '配列操作', '配列関数適用'],
 ['plugin_system', '配列操作', '配列マップ'],
 ['plugin_system', '配列操作', '配列フィルタ'],
 ['plugin_system', '二次元配列処理', '表ソート'],
 ['plugin_system', '二次元配列処理', '表数値ソート'],
 ['plugin_system', '二次元配列処理', '表ピックアップ'],
 ['plugin_system', '二次元配列処理', '表完全一致ピックアップ'],
 ['plugin_system', '二次元配列処理', '表検索'],
 ['plugin_system', '二次元配列処理', '表列数'],
 ['plugin_system', '二次元配列処理', '表行数'],
 ['plugin_system', '二次元配列処理', '表行列交換'],
 ['plugin_system', '二次元配列処理', '表右回転'],
 ['plugin_system', '二次元配列処理', '表重複削除'],
 ['plugin_system', '二次元配列処理', '表列取得'],
 ['plugin_system', '二次元配列処理', '表列挿入'],
 ['plugin_system', '二次元配列処理', '表列削除'],
 ['plugin_system', '二次元配列処理', '表列合計'],
 ['plugin_system', '二次元配列処理', '表曖昧検索'],
 ['plugin_system', '二次元配列処理', '表正規表現ピックアップ'],
 ['plugin_system', '日時処理(簡易)', '元号データ'],
 ['plugin_system', '日時処理(簡易)', '今'],
 ['plugin_system', '日時処理(簡易)', 'システム時間'],
 ['plugin_system', '日時処理(簡易)', 'システム時間ミリ秒'],
 ['plugin_system', '日時処理(簡易)', '今日'],
 ['plugin_system', '日時処理(簡易)', '明日'],
 ['plugin_system', '日時処理(簡易)', '昨日'],
 ['plugin_system', '日時処理(簡易)', '今年'],
 ['plugin_system', '日時処理(簡易)', '来年'],
 ['plugin_system', '日時処理(簡易)', '去年'],
 ['plugin_system', '日時処理(簡易)', '今月'],
 ['plugin_system', '日時処理(簡易)', '来月'],
 ['plugin_system', '日時処理(簡易)', '先月'],
 ['plugin_system', '日時処理(簡易)', '曜日'],
 ['plugin_system', '日時処理(簡易)', '曜日番号取得'],
 ['plugin_system', '日時処理(簡易)', 'UNIXTIME変換'],
 ['plugin_system', '日時処理(簡易)', 'UNIX時間変換'],
 ['plugin_system', '日時処理(簡易)', '日時変換'],
 ['plugin_system', '日時処理(簡易)', '日時書式変換'],
 ['plugin_system', '日時処理(簡易)', '和暦変換'],
 ['plugin_system', '日時処理(簡易)', '年数差'],
 ['plugin_system', '日時処理(簡易)', '月数差'],
 ['plugin_system', '日時処理(簡易)', '日数差'],
 ['plugin_system', '日時処理(簡易)', '時間差'],
 ['plugin_system', '日時処理(簡易)', '分差'],
 ['plugin_system', '日時処理(簡易)', '秒差'],
 ['plugin_system', '日時処理(簡易)', '日時差'],
 ['plugin_system', '日時処理(簡易)', '時間加算'],
 ['plugin_system', '日時処理(簡易)', '日付加算'],
 ['plugin_system', '日時処理(簡易)', '日時加算'],
 ['plugin_system', '日時処理(簡易)', '時間ミリ秒取得'],
 ['plugin_system', 'URLエンコードとパラメータ', 'URLエンコード'],
 ['plugin_system', 'URLエンコードとパラメータ', 'URLデコード'],
 ['plugin_system', 'URLエンコードとパラメータ', 'URLパラメータ解析'],
 ['plugin_system', 'BASE64', 'BASE64エンコード'],
 ['plugin_system', 'BASE64', 'BASE64デコード'],
 ['plugin_system', 'パス操作', '拡張子抽出'],
 ['plugin_system', 'パス操作', '拡張子変更'],
 ['plugin_system', 'パス操作', '終端パス追加'],
 ['plugin_system', 'パス操作', '終端パス除去'],
 ['plugin_system', 'パス操作', '終端パス削除'],
 ['plugin_system', 'パス操作', 'ファイル名抽出'],
 ['plugin_system', 'パス操作', 'パス抽出'],
 ['plugin_system', '型変換', '変数型確認'],
 ['plugin_system', '型変換', 'TYPEOF'],
 ['plugin_system', '型変換', '文字列変換'],
 ['plugin_system', '型変換', 'TOSTR'],
 ['plugin_system', '型変換', '整数変換'],
 ['plugin_system', '型変換', 'TOINT'],
 ['plugin_system', '型変換', '実数変換'],
 ['plugin_system', '型変換', 'TOFLOAT'],
 ['plugin_system', '型変換', 'INT'],
 ['plugin_system', '型変換', 'FLOAT'],
 ['plugin_system', '型変換', 'NAN判定'],
 ['plugin_system', '型変換', '非数判定'],
 ['plugin_system', '型変換', 'HEX'],
 ['plugin_system', '型変換', '進数変換'],
 ['plugin_system', '型変換', '二進'],
 ['plugin_system', '型変換', '二進表示'],
 ['plugin_system', '型変換', 'RGB'],
 ['plugin_system', 'JSON', 'JSON変換'],
 ['plugin_system', 'JSON', 'JSON取得'],
 ['plugin_system', 'JSON', 'JSONエンコード'],
 ['plugin_system', 'JSON', 'JSONエンコード整形'],
 ['plugin_system', 'JSON', 'JSONデコード'],
 ['plugin_system', 'JSON', 'JSON_E'],
 ['plugin_system', 'JSON', 'JSON_ES'],
 ['plugin_system', 'JSON', 'JSON_D'],
 ['plugin_system', '正規表現', '正規表現マッチ'],
 ['plugin_system', '正規表現', '正規表現抽出'],
 ['plugin_system', '正規表現', '抽出文字列'],
 ['plugin_system', '正規表現', '正規表現置換'],
 ['plugin_system', '正規表現', '正規表現区切'],
 ['plugin_system', '辞書型変数の操作', '辞書キー列挙'],
 ['plugin_system', '辞書型変数の操作', '辞書キー削除'],
 ['plugin_system', '辞書型変数の操作', '辞書キー存在'],
 ['plugin_system', 'ハッシュ', 'ハッシュキー列挙'],
 ['plugin_system', 'ハッシュ', 'ハッシュ内容列挙'],
 ['plugin_system', 'ハッシュ', 'ハッシュキー削除'],
 ['plugin_system', 'ハッシュ', 'ハッシュキー存在'],
 ['plugin_system', '標準出力', '表示'],
 ['plugin_system', '標準出力', '継続表示'],
 ['plugin_system', '標準出力', '連続表示'],
 ['plugin_system', '標準出力', '連続無改行表示'],
 ['plugin_system', '標準出力', '表示ログ'],
 ['plugin_system', '標準出力', '表示ログクリア'],
 ['plugin_system', '標準出力', '言'],
 ['plugin_system', '標準出力', 'コンソール表示'],
 ['plugin_system', 'タイマー', '秒待'],
 ['plugin_system', 'タイマー', '秒待機'],
 ['plugin_system', 'タイマー', '秒逐次待機'],
 ['plugin_system', 'タイマー', '秒後'],
 ['plugin_system', 'タイマー', '秒毎'],
 ['plugin_system', 'タイマー', '秒タイマー開始時'],
 ['plugin_system', 'タイマー', 'タイマー停止'],
 ['plugin_system', 'タイマー', '全タイマー停止'],
 ['plugin_csv', 'CSV操作', 'CSV取得'],
 ['plugin_csv', 'CSV操作', 'TSV取得'],
 ['plugin_csv', 'CSV操作', '表CSV変換'],
 ['plugin_csv', 'CSV操作', 'CSV変換'],
 ['plugin_csv', 'CSV操作', '表TSV変換'],
 ['plugin_csv', 'CSV操作', 'TSV変換'],
 ['plugin_csv', 'CSV操作', 'CSVオプション設定'],
 ['plugin_toml', 'TOML', 'TOML取得'],
 ['plugin_toml', 'TOML', 'TOML変換'],
 ['plugin_math', '三角関数', 'SIN'],
 ['plugin_math', '三角関数', 'COS'],
 ['plugin_math', '三角関数', 'TAN'],
 ['plugin_math', '三角関数', 'ARCSIN'],
 ['plugin_math', '三角関数', 'ARCCOS'],
 ['plugin_math', '三角関数', 'ARCTAN'],
 ['plugin_math', '三角関数', 'ATAN2'],
 ['plugin_math', '三角関数', '座標角度計算'],
 ['plugin_math', '三角関数', 'RAD2DEG'],
 ['plugin_math', '三角関数', 'DEG2RAD'],
 ['plugin_math', '三角関数', '度変換'],
 ['plugin_math', '三角関数', 'ラジアン変換'],
 ['plugin_math', '算術関数', 'SIGN'],
 ['plugin_math', '算術関数', '符号'],
 ['plugin_math', '算術関数', 'ABS'],
 ['plugin_math', '算術関数', '絶対値'],
 ['plugin_math', '算術関数', 'EXP'],
 ['plugin_math', '算術関数', 'HYPOT'],
 ['plugin_math', '算術関数', '斜辺'],
 ['plugin_math', '算術関数', 'LN'],
 ['plugin_math', '算術関数', 'LOG'],
 ['plugin_math', '算術関数', 'LOGN'],
 ['plugin_math', '算術関数', 'FRAC'],
 ['plugin_math', '算術関数', '小数部分'],
 ['plugin_math', '算術関数', '整数部分'],
 ['plugin_math', '算術関数', '乱数'],
 ['plugin_math', '算術関数', '乱数範囲'],
 ['plugin_math', '算術関数', 'SQRT'],
 ['plugin_math', '算術関数', '平方根'],
 ['plugin_math', '数値切上切捨丸め', 'ROUND'],
 ['plugin_math', '数値切上切捨丸め', '四捨五入'],
 ['plugin_math', '数値切上切捨丸め', '小数点切上'],
 ['plugin_math', '数値切上切捨丸め', '小数点切下'],
 ['plugin_math', '数値切上切捨丸め', '小数点四捨五入'],
 ['plugin_math', '数値切上切捨丸め', 'CEIL'],
 ['plugin_math', '数値切上切捨丸め', '切上'],
 ['plugin_math', '数値切上切捨丸め', 'FLOOR'],
 ['plugin_math', '数値切上切捨丸め', '切捨'],
 ['plugin_promise', '非同期処理の保証の定数', 'そ'],
 ['plugin_promise', '非同期処理の保証', '動時'],
 ['plugin_promise', '非同期処理の保証', '成功時'],
 ['plugin_promise', '非同期処理の保証', '処理時'],
 ['plugin_promise', '非同期処理の保証', '失敗時'],
 ['plugin_promise', '非同期処理の保証', '終了時'],
 ['plugin_promise', '非同期処理の保証', '束'],
 ['plugin_httpserver', '簡易HTTPサーバ', 'HTTPメソッド'],
 ['plugin_httpserver', '簡易HTTPサーバ', 'GETデータ'],
 ['plugin_httpserver', '簡易HTTPサーバ', 'POSTデータ'],
 ['plugin_httpserver', '簡易HTTPサーバ', 'FILESデータ'],
 ['plugin_httpserver', '簡易HTTPサーバ', '簡易HTTPサーバ起動時'],
 ['plugin_httpserver', '簡易HTTPサーバ', '簡易HTTPサーバ静的パス指定'],
 ['plugin_httpserver', '簡易HTTPサーバ', '簡易HTTPサーバ受信時'],
 ['plugin_httpserver', '簡易HTTPサーバ', '簡易HTTPサーバ出力'],
 ['plugin_httpserver', '簡易HTTPサーバ', '簡易HTTPサーバヘッダ出力'],
 ['plugin_httpserver', '簡易HTTPサーバ', '簡易HTTPサーバ移動'],
 ['plugin_markup', 'マークアップ', 'マークダウンHTML変換'],
 ['plugin_markup', 'マークアップ', 'HTML整形'],
 ['plugin_caniuse', 'ブラウザサポート', 'ブラウザ名変換表'],
 ['plugin_caniuse', 'ブラウザサポート', '対応ブラウザ一覧取得'],
 ['plugin_kansuji', '漢数字関連', '漢数字'],
 ['plugin_kansuji', '漢数字関連', '算用数字']]

LNAKO_NODE = [['plugin_node', 'ファイル入出力', '開'],
 ['plugin_node', 'ファイル入出力', '読'],
 ['plugin_node', 'ファイル入出力', 'バイナリ読'],
 ['plugin_node', 'ファイル入出力', '保存'],
 ['plugin_node', 'ファイル入出力', 'SJISファイル読'],
 ['plugin_node', 'ファイル入出力', 'SJISファイル保存'],
 ['plugin_node', 'ファイル入出力', 'EUCファイル読'],
 ['plugin_node', 'ファイル入出力', 'EUCファイル保存'],
 ['plugin_node', 'ファイル入出力', '起動待機'],
 ['plugin_node', 'ファイル入出力', 'コマンド実行'],
 ['plugin_node', 'ファイル入出力', 'コマンド実行待機'],
 ['plugin_node', 'ファイル入出力', '起動'],
 ['plugin_node', 'ファイル入出力', 'コンソールクリア'],
 ['plugin_node', 'ファイル入出力', '起動時'],
 ['plugin_node', 'ファイル入出力', 'ブラウザ起動'],
 ['plugin_node', 'ファイル入出力', 'エクスプローラー起動'],
 ['plugin_node', 'ファイル入出力', 'ファイル列挙'],
 ['plugin_node', 'ファイル入出力', '全ファイル列挙'],
 ['plugin_node', 'ファイル入出力', '存在'],
 ['plugin_node', 'ファイル入出力', 'フォルダ存在'],
 ['plugin_node', 'ファイル入出力', 'フォルダ作成'],
 ['plugin_node', 'ファイル入出力', 'ファイルコピーデフォルト動作'],
 ['plugin_node', 'ファイル入出力', 'ファイルコピー'],
 ['plugin_node', 'ファイル入出力', 'ファイル上書コピー'],
 ['plugin_node', 'ファイル入出力', 'ファイルコピー時'],
 ['plugin_node', 'ファイル入出力', 'ファイル移動'],
 ['plugin_node', 'ファイル入出力', 'ファイル上書移動'],
 ['plugin_node', 'ファイル入出力', 'ファイル処理時'],
 ['plugin_node', 'ファイル入出力', 'ファイル処理強制停止'],
 ['plugin_node', 'ファイル入出力', 'ファイル移動時'],
 ['plugin_node', 'ファイル入出力', 'ファイル削除'],
 ['plugin_node', 'ファイル入出力', 'ファイル削除時'],
 ['plugin_node', 'ファイル入出力', 'ファイル情報取得'],
 ['plugin_node', 'ファイル入出力', 'ファイルサイズ取得'],
 ['plugin_node', 'パス操作', 'ファイル名抽出'],
 ['plugin_node', 'パス操作', 'パス抽出'],
 ['plugin_node', 'パス操作', '絶対パス変換'],
 ['plugin_node', 'パス操作', '相対パス展開'],
 ['plugin_node', 'フォルダ取得', 'カレントディレクトリ取得'],
 ['plugin_node', 'フォルダ取得', 'カレントディレクトリ変更'],
 ['plugin_node', 'フォルダ取得', '作業フォルダ取得'],
 ['plugin_node', 'フォルダ取得', '作業フォルダ変更'],
 ['plugin_node', 'フォルダ取得', 'ホームディレクトリ取得'],
 ['plugin_node', 'フォルダ取得', 'デスクトップ'],
 ['plugin_node', 'フォルダ取得', 'マイドキュメント'],
 ['plugin_node', 'フォルダ取得', '母艦パス'],
 ['plugin_node', 'フォルダ取得', '母艦パス取得'],
 ['plugin_node', 'フォルダ取得', 'テンポラリフォルダ'],
 ['plugin_node', 'フォルダ取得', '一時フォルダ作成'],
 ['plugin_node', '環境変数', '環境変数取得'],
 ['plugin_node', '環境変数', '環境変数一覧取得'],
 ['plugin_node', '圧縮・解凍', '圧縮解凍ツールパス'],
 ['plugin_node', '圧縮・解凍', '圧縮解凍ツールパス変更'],
 ['plugin_node', '圧縮・解凍', '解凍'],
 ['plugin_node', '圧縮・解凍', '解凍時'],
 ['plugin_node', '圧縮・解凍', '圧縮'],
 ['plugin_node', '圧縮・解凍', '圧縮時'],
 ['plugin_node', 'Nodeプロセス', '終'],
 ['plugin_node', 'Nodeプロセス', 'プロセス終'],
 ['plugin_node', 'Nodeプロセス', '強制終了時'],
 ['plugin_node', 'Nodeプロセス', '終了'],
 ['plugin_node', 'Nodeプロセス', 'OS取得'],
 ['plugin_node', 'Nodeプロセス', 'OSアーキテクチャ取得'],
 ['plugin_node', 'コマンドラインと標準入出力', 'コマンドライン'],
 ['plugin_node', 'コマンドラインと標準入出力', 'ナデシコランタイム'],
 ['plugin_node', 'コマンドラインと標準入出力', 'ナデシコランタイムパス'],
 ['plugin_node', 'コマンドラインと標準入出力', '標準入力取得時'],
 ['plugin_node', 'コマンドラインと標準入出力', '尋'],
 ['plugin_node', 'コマンドラインと標準入出力', '文字尋'],
 ['plugin_node', 'コマンドラインと標準入出力', '標準入力全取得'],
 ['plugin_node', 'テスト', 'ASSERT等'],
 ['plugin_node', 'ネットワーク', '自分IPアドレス取得'],
 ['plugin_node', 'ネットワーク', '自分IPV6アドレス取得'],
 ['plugin_node', 'Ajax', 'AJAX送信時'],
 ['plugin_node', 'Ajax', 'AJAX受信時'],
 ['plugin_node', 'Ajax', 'GET送信時'],
 ['plugin_node', 'Ajax', 'POST送信時'],
 ['plugin_node', 'Ajax', 'POSTフォーム送信時'],
 ['plugin_node', 'Ajax', 'AJAX失敗時'],
 ['plugin_node', 'Ajax', 'AJAXオプション'],
 ['plugin_node', 'Ajax', 'AJAXオプション設定'],
 ['plugin_node', 'Ajax', 'AJAX保障送信'],
 ['plugin_node', 'Ajax', 'HTTP保障取得'],
 ['plugin_node', 'Ajax', 'GET保障送信'],
 ['plugin_node', 'Ajax', 'POST保障送信'],
 ['plugin_node', 'Ajax', 'POSTフォーム保障送信'],
 ['plugin_node', 'Ajax', 'AJAX内容取得'],
 ['plugin_node', 'Ajax', 'AJAX受信'],
 ['plugin_node', 'Ajax', 'POSTデータ生成'],
 ['plugin_node', 'Ajax', 'POST送信'],
 ['plugin_node', 'Ajax', 'POSTフォーム送信'],
 ['plugin_node', '新AJAX', 'AJAXテキスト取得'],
 ['plugin_node', '新AJAX', 'AJAX_JSON取得'],
 ['plugin_node', '新AJAX', 'AJAXバイナリ取得'],
 ['plugin_node', '新AJAX', 'DISCORD送信'],
 ['plugin_node', '新AJAX', 'DISCORDファイル送信'],
 ['plugin_node', 'LINE', 'LINE送信'],
 ['plugin_node', 'LINE', 'LINE画像送信'],
 ['plugin_node', '文字コード', '文字コード変換サポート判定'],
 ['plugin_node', '文字コード', 'SJIS変換'],
 ['plugin_node', '文字コード', 'SJIS取得'],
 ['plugin_node', '文字コード', 'エンコーディング変換'],
 ['plugin_node', '文字コード', 'エンコーディング取得'],
 ['plugin_node', 'ハッシュ関数', 'ハッシュ関数一覧取得'],
 ['plugin_node', 'ハッシュ関数', 'ハッシュ値計算'],
 ['plugin_node', 'ハッシュ関数', 'ランダムUUID生成'],
 ['plugin_node', 'ハッシュ関数', 'ランダム配列生成']]

LOWLEVEL_SPECS = [{'name': 'ファイル開く',
  'kana': 'ふぁいるひらく',
  'genre': 'ストリームIO',
  'particles': 'PATHをMODEで/PATHを',
  'returns': 'handle',
  'implemented': True,
  'capability': 'stream_file_io',
  'errors': ['ENOENT', 'EACCES', 'EPERM', 'EISDIR', 'EINVAL', 'EMFILE', 'ENFILE', 'ENOTSUP', 'EROFS', 'ENOSPC'],
  'desc': 'パス PATH のファイルを開き、ファイルハンドルを返します。MODE には読み書きモード（"r", "r+", "w", "w+", "a", "a+" やバイナリ指定の "b" '
          'など）を文字列で指定できます。MODE を省略した場合は読み込み専用（"r"）で開きます。',
  'example': 'F = 「/tmp/test_open.txt」を「w+b」でファイル開く。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_open.txt」をファイルリンク削除。\n'
             '「ファイル開閉成功」と表示。\n'
             '### lnako表示結果: ファイル開閉成功',
  'refs': ['lnako_lowlevel/ファイル閉じる', 'lnako_lowlevel/ファイルバイト読む', 'lnako_lowlevel/ファイルバイト書く']},
 {'name': 'ファイル閉じる',
  'kana': 'ふぁいるとじる',
  'genre': 'ストリームIO',
  'particles': 'HANDLEを/HANDLEの',
  'returns': 'void',
  'implemented': True,
  'capability': 'stream_file_io',
  'errors': ['EBADF'],
  'desc': 'ファイルハンドル HANDLE を閉じ、システムリソースを解放します。すでに閉じたハンドルや無効なハンドルを操作すると EBADF エラーになります。',
  'example': 'F = 「/tmp/test_close.txt」を「w+b」でファイル開く。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_close.txt」をファイルリンク削除。\n'
             '「ファイルクローズ成功」と表示。\n'
             '### lnako表示結果: ファイルクローズ成功',
  'refs': ['lnako_lowlevel/ファイル開く']},
 {'name': 'ファイルバイト読む',
  'kana': 'ふぁいるばいとよむ',
  'genre': 'ストリームIO',
  'particles': 'HANDLEをSIZEで/HANDLEからSIZEを',
  'returns': 'bytes',
  'implemented': True,
  'capability': 'stream_file_io',
  'errors': ['EBADF', 'EINVAL', 'ENOTSUP'],
  'desc': 'ファイルハンドル HANDLE から最大 SIZE バイトのバイナリデータ（Bytes）を読み込んで返します。ファイルの終端（EOF）に達した場合は、長さ 0 の空の Bytes を返します。',
  'example': 'H = 「sha256」でハッシュ開始。\n'
             'B = Hをハッシュ完了。\n'
             'F = 「/tmp/test_read.bin」を「w+b」でファイル開く。\n'
             'FへBをファイルバイト書く。\n'
             'Fをファイル閉じる。\n'
             '\n'
             'F2 = 「/tmp/test_read.bin」を「rb」でファイル開く。\n'
             'B2 = F2から32をファイルバイト読む。\n'
             'F2をファイル閉じる。\n'
             '「/tmp/test_read.bin」をファイルリンク削除。\n'
             '\n'
             'H2 = 「sha256」でハッシュ開始。\n'
             'H2へB2をハッシュ追加。\n'
             'R = H2を「hex」でハッシュ完了。\n'
             'Rを表示。\n'
             '### lnako表示結果: 5df6e0e2761359d30a8275058e299fcc0381534545f55cf43e41983f5d4c9456',
  'refs': ['lnako_lowlevel/ファイル開く', 'lnako_lowlevel/ファイルバイト書く', 'lnako_lowlevel/ファイル閉じる']},
 {'name': 'ファイルバイト書く',
  'kana': 'ふぁいるばいとかく',
  'genre': 'ストリームIO',
  'particles': 'HANDLEをBYTESで/HANDLEへBYTESを',
  'returns': 'number',
  'implemented': True,
  'capability': 'stream_file_io',
  'errors': ['EBADF', 'EINVAL', 'ENOSPC', 'EPIPE', 'ENOTSUP', 'EROFS'],
  'desc': 'ファイルハンドル HANDLE へバイナリデータ BYTES（Bytes 型）を書き込み、実際に書き込まれたバイト数を返します。',
  'example': 'H = 「sha256」でハッシュ開始。\n'
             'B = Hをハッシュ完了。\n'
             'F = 「/tmp/test_write.bin」を「w+b」でファイル開く。\n'
             'N = FへBをファイルバイト書く。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_write.bin」をファイルリンク削除。\n'
             'Nを表示。\n'
             '### lnako表示結果: 32',
  'refs': ['lnako_lowlevel/ファイル開く', 'lnako_lowlevel/ファイルバイト読む', 'lnako_lowlevel/ファイル同期']},
 {'name': 'ファイル同期',
  'kana': 'ふぁいるどうき',
  'genre': 'ストリームIO',
  'particles': 'HANDLEを/HANDLEの',
  'returns': 'void',
  'implemented': True,
  'capability': 'stream_file_io',
  'errors': ['EBADF', 'EINVAL'],
  'desc': 'ファイルハンドル HANDLE の未書き込みデータをストレージへ書き出して同期（フラッシュ）します。POSIX の fsync に相当します。',
  'example': 'H = 「sha256」でハッシュ開始。\n'
             'B = Hをハッシュ完了。\n'
             'F = 「/tmp/test_sync.bin」を「w+b」でファイル開く。\n'
             'FへBをファイルバイト書く。\n'
             'Fをファイル同期。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_sync.bin」をファイルリンク削除。\n'
             '「同期成功」と表示。\n'
             '### lnako表示結果: 同期成功',
  'refs': ['lnako_lowlevel/ファイル開く', 'lnako_lowlevel/ファイルバイト書く']},
 {'name': 'ファイル切詰',
  'kana': 'ふぁいるきりつめ',
  'genre': 'ストリームIO',
  'particles': 'HANDLEをSIZEで/HANDLEをSIZEに',
  'returns': 'void',
  'implemented': True,
  'capability': 'truncate',
  'errors': ['EBADF', 'EINVAL', 'ENOSPC', 'ENOTSUP', 'EPERM', 'EROFS'],
  'desc': '開いているファイルハンドル HANDLE のファイルサイズを SIZE バイトに変更（切り詰め・拡張）します。POSIX の ftruncate に相当します。',
  'example': 'H = 「sha256」でハッシュ開始。\n'
             'B = Hをハッシュ完了。\n'
             'F = 「/tmp/test_trunc.bin」を「w+b」でファイル開く。\n'
             'FへBをファイルバイト書く。\n'
             'Fを16にファイル切詰。\n'
             'Fをファイル閉じる。\n'
             'INFO = 「/tmp/test_trunc.bin」をファイル詳細情報取得。\n'
             '「/tmp/test_trunc.bin」をファイルリンク削除。\n'
             'INFO[「size」]を表示。\n'
             '### lnako表示結果: 16',
  'refs': ['lnako_lowlevel/ファイル開く', 'lnako_lowlevel/ファイル詳細情報取得']},
 {'name': 'ファイル位置変更',
  'kana': 'ふぁいるいちへんこう',
  'genre': 'ストリームIO',
  'particles': 'HANDLEをOFFSETでWHENCEを/HANDLEをOFFSETで',
  'returns': 'offset',
  'implemented': True,
  'capability': 'stream_file_io',
  'errors': ['EBADF', 'EINVAL', 'ENOTSUP'],
  'desc': 'ファイルハンドル HANDLE のシーク位置（オフセット）を変更し、変更後の新しい絶対位置を返します。POSIX の lseek に相当します。WHENCE には基準位置として「開始」（先頭基準、SEEK_SET '
          '相当）、「現在」（現在位置基準、SEEK_CUR 相当）、「終端」（末尾基準、SEEK_END 相当）のいずれかを文字列で指定します。WHENCE を省略した場合は「開始」が基準になります。',
  'example': 'H = 「sha256」でハッシュ開始。\n'
             'B = Hをハッシュ完了。\n'
             'F = 「/tmp/test_seek.bin」を「w+b」でファイル開く。\n'
             'FへBをファイルバイト書く。\n'
             'POS1 = Fを10でファイル位置変更。\n'
             'POS2 = Fを5で「現在」をファイル位置変更。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_seek.bin」をファイルリンク削除。\n'
             '「{POS1},{POS2}」を表示。\n'
             '### lnako表示結果: 10,15',
  'refs': ['lnako_lowlevel/ファイル位置取得',
           'lnako_lowlevel/ファイル位置指定読込',
           'lnako_lowlevel/ファイル位置指定書込',
           'lnako_lowlevel/ファイル開く']},
 {'name': 'ファイル位置取得',
  'kana': 'ふぁいるいちしゅとく',
  'genre': 'ストリームIO',
  'particles': 'HANDLEを/HANDLEの',
  'returns': 'offset',
  'implemented': True,
  'capability': 'stream_file_io',
  'errors': ['EBADF', 'EINVAL', 'ENOTSUP'],
  'desc': 'ファイルハンドル HANDLE の現在のシーク位置（先頭からのバイトオフセット）を取得して返します。POSIX の lseek(fd, 0, SEEK_CUR) に相当します。',
  'example': 'H = 「sha256」でハッシュ開始。\n'
             'B = Hをハッシュ完了。\n'
             'F = 「/tmp/test_tell.bin」を「w+b」でファイル開く。\n'
             'FへBをファイルバイト書く。\n'
             'Fを12でファイル位置変更。\n'
             'POS = Fのファイル位置取得。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_tell.bin」をファイルリンク削除。\n'
             'POSを表示。\n'
             '### lnako表示結果: 12',
  'refs': ['lnako_lowlevel/ファイル位置変更', 'lnako_lowlevel/ファイル開く']},
 {'name': 'ファイル位置指定読込',
  'kana': 'ふぁいるいちしていよみこみ',
  'genre': 'ストリームIO',
  'particles': 'HANDLEをOFFSETからSIZEを/HANDLEからOFFSETにSIZEを',
  'returns': 'bytes',
  'implemented': True,
  'capability': 'stream_file_io',
  'errors': ['EBADF', 'EINVAL', 'ENOTSUP'],
  'desc': 'ファイルハンドル HANDLE の現在のシーク位置を変更せずに、指定したオフセット位置 OFFSET から最大 SIZE バイトのバイナリデータ（Bytes）を読み込んで返します。POSIX の pread '
          'に相当します。ファイルの終端（EOF）に達した場合は、長さ 0 の空の Bytes を返します。',
  'example': 'B = 「ABCDEFGH」を「utf-8」へエンコーディング変換。\n'
             'F = 「/tmp/test_pread.bin」を「w+b」でファイル開く。\n'
             'FへBをファイルバイト書く。\n'
             'Fを0でファイル位置変更。\n'
             'PART = Fを2から4をファイル位置指定読込。\n'
             'POS = Fのファイル位置取得。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_pread.bin」をファイルリンク削除。\n'
             'S = PARTを「utf-8」でエンコーディング取得。\n'
             '「{S}:{POS}」を表示。\n'
             '### lnako表示結果: CDEF:0',
  'refs': ['lnako_lowlevel/ファイル位置指定書込', 'lnako_lowlevel/ファイルバイト読む', 'lnako_lowlevel/ファイル位置変更']},
 {'name': 'ファイル位置指定書込',
  'kana': 'ふぁいるいちしていかきこみ',
  'genre': 'ストリームIO',
  'particles': 'HANDLEへOFFSETにBYTESを/HANDLEをOFFSETからBYTESで',
  'returns': 'number',
  'implemented': True,
  'capability': 'stream_file_io',
  'errors': ['EBADF', 'EINVAL', 'ENOSPC', 'EPIPE', 'ENOTSUP', 'EROFS'],
  'desc': 'ファイルハンドル HANDLE の現在のシーク位置を変更せずに、指定したオフセット位置 OFFSET へバイナリデータ BYTES を書き込み、実際に書き込まれたバイト数を返します。POSIX の pwrite '
          'に相当します。追記モード（"a" や "a+"）で開いたハンドルに対して実行した場合は EINVAL エラーになります。',
  'example': 'B1 = 「AAAAAAAA」を「utf-8」へエンコーディング変換。\n'
             'B2 = 「XY」を「utf-8」へエンコーディング変換。\n'
             'F = 「/tmp/test_pwrite.bin」を「w+b」でファイル開く。\n'
             'FへB1をファイルバイト書く。\n'
             'Fを0でファイル位置変更。\n'
             'N = Fへ3にB2をファイル位置指定書込。\n'
             'POS = Fのファイル位置取得。\n'
             'ALL = Fから8をファイルバイト読む。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_pwrite.bin」をファイルリンク削除。\n'
             'S = ALLを「utf-8」でエンコーディング取得。\n'
             '「{S}:{N}:{POS}」を表示。\n'
             '### lnako表示結果: AAAXYAAA:2:0',
  'refs': ['lnako_lowlevel/ファイル位置指定読込', 'lnako_lowlevel/ファイルバイト書く', 'lnako_lowlevel/ファイル位置変更']},
 {'name': '標準入力バイト読む',
  'kana': 'ひょうじゅんにゅうりょくばいとよむ',
  'genre': '標準入出力',
  'particles': 'SIZEを/SIZEで',
  'returns': 'bytes',
  'implemented': True,
  'capability': 'raw_stdio',
  'errors': ['EINVAL', 'EPIPE', 'ENOSPC', 'ENOTSUP', 'EBADF'],
  'desc': '標準入力から最大 SIZE バイトのバイナリデータ（Bytes）を直接読み込んで返します。終端（EOF）に達した場合は、長さ 0 の空の Bytes を返します。',
  'example': '# 5バイト読み取る例:\nB = 5で標準入力バイト読む。',
  'refs': ['lnako_lowlevel/標準出力バイト書く', 'lnako_lowlevel/標準エラー出力バイト書く']},
 {'name': '標準出力バイト書く',
  'kana': 'ひょうじゅんしゅつりょくばいとかく',
  'genre': '標準入出力',
  'particles': 'BYTESを/BYTESで',
  'returns': 'number',
  'implemented': True,
  'capability': 'raw_stdio',
  'errors': ['EINVAL', 'EPIPE', 'ENOSPC', 'ENOTSUP', 'EBADF'],
  'desc': '標準出力へバイナリデータ BYTES を直接書き込み、実際に書き込まれたバイト数を返します。改行の自動付与や文字コード変換は行いません。',
  'example': 'H = 「sha256」でハッシュ開始。\nB = Hをハッシュ完了。\nBで標準出力バイト書く。',
  'refs': ['lnako_lowlevel/標準出力同期', 'lnako_lowlevel/標準エラー出力バイト書く']},
 {'name': '標準エラー出力バイト書く',
  'kana': 'ひょうじゅんえらーしゅつりょくばいとかく',
  'genre': '標準入出力',
  'particles': 'BYTESを/BYTESで',
  'returns': 'number',
  'implemented': True,
  'capability': 'raw_stdio',
  'errors': ['EINVAL', 'EPIPE', 'ENOSPC', 'ENOTSUP', 'EBADF'],
  'desc': '標準エラー出力へバイナリデータ BYTES を直接書き込み、実際に書き込まれたバイト数を返します。改行の自動付与や文字コード変換は行いません。',
  'example': 'H = 「sha256」でハッシュ開始。\nB = Hをハッシュ完了。\nBで標準エラー出力バイト書く。',
  'refs': ['lnako_lowlevel/標準エラー出力同期', 'lnako_lowlevel/標準出力バイト書く']},
 {'name': '標準出力同期',
  'kana': 'ひょうじゅんしゅつりょくどうき',
  'genre': '標準入出力',
  'particles': '',
  'returns': 'void',
  'implemented': True,
  'capability': 'raw_stdio',
  'errors': ['EPIPE', 'EINVAL', 'ENOTSUP', 'EBADF'],
  'desc': '標準出力のバッファを同期（フラッシュ）します。\n\n端末やパイプ環境では OS の制限によりエラーになる場合があるため、DocTest では実行結果を検証していません。',
  'example': '標準出力同期。',
  'refs': ['lnako_lowlevel/標準出力バイト書く', 'lnako_lowlevel/標準エラー出力同期']},
 {'name': '標準エラー出力同期',
  'kana': 'ひょうじゅんえらーしゅつりょくどうき',
  'genre': '標準入出力',
  'particles': '',
  'returns': 'void',
  'implemented': True,
  'capability': 'raw_stdio',
  'errors': ['EPIPE', 'EINVAL', 'ENOTSUP', 'EBADF'],
  'desc': '標準エラー出力のバッファを同期（フラッシュ）します。\n\n端末やパイプ環境では OS の制限によりエラーになる場合があるため、DocTest では実行結果を検証していません。',
  'example': '標準エラー出力同期。',
  'refs': ['lnako_lowlevel/標準エラー出力バイト書く', 'lnako_lowlevel/標準出力同期']},
 {'name': 'ファイル詳細情報取得',
  'kana': 'ふぁいるしょうさいじょうほうしゅとく',
  'genre': 'ファイルシステム',
  'particles': 'PATHを/PATHの/PATHから',
  'returns': 'stat',
  'implemented': True,
  'capability': 'stat',
  'errors': ['ENOENT', 'EACCES', 'EPERM', 'ENOTDIR', 'ELOOP', 'EINVAL', 'ENOTSUP'],
  'desc': '指定したパス PATH のファイルやディレクトリの詳細情報（stat）を辞書で返します。辞書には種別 kind（"file", "directory", "symlink" など）、サイズ size、権限 '
          'mode、所有者 uid / gid、リンク数 nlink、ナノ秒単位のタイムスタンプ（atimeNs, mtimeNs, ctimeNs, birthtimeNs）などが含まれます。PATH '
          'がシンボリックリンクの場合は、リンク先を追跡した実体の情報を返します。',
  'example': 'F = 「/tmp/test_stat.bin」を「w+b」でファイル開く。\n'
             'Fをファイル閉じる。\n'
             'INFO = 「/tmp/test_stat.bin」をファイル詳細情報取得。\n'
             '「/tmp/test_stat.bin」をファイルリンク削除。\n'
             'INFO[「kind」]を表示。\n'
             '### lnako表示結果: file',
  'refs': ['lnako_lowlevel/シンボリックリンク情報取得', 'lnako_lowlevel/実体パス取得']},
 {'name': 'シンボリックリンク情報取得',
  'kana': 'しんぼりっくりんくじょうほうしゅとく',
  'genre': 'ファイルシステム',
  'particles': 'PATHを/PATHの/PATHから',
  'returns': 'stat',
  'implemented': True,
  'capability': 'lstat',
  'errors': ['ENOENT', 'EACCES', 'EPERM', 'ENOTDIR', 'ELOOP', 'EINVAL', 'ENOTSUP'],
  'desc': '指定したパス PATH の詳細情報（lstat）を辞書で返します。『[[lnako_lowlevel/ファイル詳細情報取得]]』（stat）とは異なり、PATH '
          'がシンボリックリンクであってもリンク先を追跡せず、リンクそのものの属性情報を返します。',
  'example': 'F = 「/tmp/test_lstat_src.txt」を「w+b」でファイル開く。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_lstat_src.txt」を「/tmp/test_lstat_link.txt」へシンボリックリンク作成。\n'
             'LINFO = 「/tmp/test_lstat_link.txt」のシンボリックリンク情報取得。\n'
             '「/tmp/test_lstat_link.txt」をファイルリンク削除。\n'
             '「/tmp/test_lstat_src.txt」をファイルリンク削除。\n'
             'LINFO[「kind」]を表示。\n'
             '### lnako表示結果: symlink',
  'refs': ['lnako_lowlevel/ファイル詳細情報取得', 'lnako_lowlevel/シンボリックリンク作成']},
 {'name': 'シンボリックリンク作成',
  'kana': 'しんぼりっくりんくさくせい',
  'genre': 'ファイルシステム',
  'particles': 'TARGETをLINKへ/LINKにTARGETを',
  'returns': 'void',
  'implemented': True,
  'capability': 'symlink',
  'errors': ['EEXIST', 'ENOENT', 'EACCES', 'ENOTDIR', 'EPERM', 'ELOOP', 'EROFS', 'ENOSPC', 'ENOTSUP', 'EINVAL'],
  'desc': 'TARGET を指すシンボリックリンクを LINK のパスに作成します。POSIX の symlink に相当します。',
  'example': 'F = 「/tmp/test_sym_src.txt」を「w+b」でファイル開く。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_sym_src.txt」を「/tmp/test_sym_link.txt」へシンボリックリンク作成。\n'
             'LINFO = 「/tmp/test_sym_link.txt」のシンボリックリンク情報取得。\n'
             '「/tmp/test_sym_link.txt」をファイルリンク削除。\n'
             '「/tmp/test_sym_src.txt」をファイルリンク削除。\n'
             'LINFO[「kind」]を表示。\n'
             '### lnako表示結果: symlink',
  'refs': ['lnako_lowlevel/シンボリックリンク先取得', 'lnako_lowlevel/ハードリンク作成']},
 {'name': 'シンボリックリンク先取得',
  'kana': 'しんぼりっくりんくさきしゅとく',
  'genre': 'ファイルシステム',
  'particles': 'PATHを/PATHの',
  'returns': 'string',
  'implemented': True,
  'capability': 'readlink',
  'errors': ['EINVAL', 'ENOENT', 'EACCES', 'EPERM', 'ENOTDIR', 'ELOOP', 'ENOTSUP'],
  'desc': 'シンボリックリンク PATH が指している参照先のパスを文字列で返します。POSIX の readlink に相当します。',
  'example': 'F = 「/tmp/test_rlink_src.txt」を「w+b」でファイル開く。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_rlink_src.txt」を「/tmp/test_rlink_link.txt」へシンボリックリンク作成。\n'
             'TARGET = 「/tmp/test_rlink_link.txt」のシンボリックリンク先取得。\n'
             '「/tmp/test_rlink_link.txt」をファイルリンク削除。\n'
             '「/tmp/test_rlink_src.txt」をファイルリンク削除。\n'
             'TARGETを表示。\n'
             '### lnako表示結果: /tmp/test_rlink_src.txt',
  'refs': ['lnako_lowlevel/シンボリックリンク作成', 'lnako_lowlevel/実体パス取得']},
 {'name': 'ハードリンク作成',
  'kana': 'はーどりんくさくせい',
  'genre': 'ファイルシステム',
  'particles': 'TARGETをLINKへ/LINKにTARGETを',
  'returns': 'void',
  'implemented': True,
  'capability': 'hardlink',
  'errors': ['EEXIST',
             'ENOENT',
             'EACCES',
             'EPERM',
             'EXDEV',
             'ENOTDIR',
             'ELOOP',
             'EROFS',
             'ENOSPC',
             'ENOTSUP',
             'EINVAL'],
  'desc': 'TARGET に対する新しいハードリンクを LINK のパスに作成します。POSIX の link、Windows（NTFS）の CreateHardLinkW '
          'に相当します。同一ファイルシステムの既存ファイルに対してのみ作成でき、非対応のファイルシステムでは ENOTSUP エラーになります。',
  'example': 'F = 「/tmp/test_hard_src.txt」を「w+b」でファイル開く。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_hard_src.txt」を「/tmp/test_hard_link.txt」へハードリンク作成。\n'
             'INFO = 「/tmp/test_hard_link.txt」のファイル詳細情報取得。\n'
             '「/tmp/test_hard_link.txt」をファイルリンク削除。\n'
             '「/tmp/test_hard_src.txt」をファイルリンク削除。\n'
             'INFO[「nlink」]を表示。\n'
             '### lnako表示結果: 2',
  'refs': ['lnako_lowlevel/シンボリックリンク作成', 'lnako_lowlevel/ファイルリンク削除']},
 {'name': '実体パス取得',
  'kana': 'じったいぱすしゅとく',
  'genre': 'ファイルシステム',
  'particles': 'PATHを/PATHの',
  'returns': 'string',
  'implemented': True,
  'capability': 'realpath',
  'errors': ['ENOENT', 'EACCES', 'EPERM', 'ENOTDIR', 'ELOOP', 'ENOTSUP', 'EINVAL'],
  'desc': 'パス PATH に含まれるシンボリックリンクや相対パス（"." や ".."）をすべて解決し、正規化した絶対パスを文字列で返します。POSIX の realpath に相当します。',
  'example': 'F = 「/tmp/test_real_src.txt」を「w+b」でファイル開く。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_real_src.txt」を「/tmp/test_real_link.txt」へシンボリックリンク作成。\n'
             'REAL = 「/tmp/test_real_link.txt」の実体パス取得。\n'
             '「/tmp/test_real_link.txt」をファイルリンク削除。\n'
             '「/tmp/test_real_src.txt」をファイルリンク削除。\n'
             'FNAME = REALからファイル名抽出。\n'
             'FNAMEを表示。\n'
             '### lnako表示結果: test_real_src.txt',
  'refs': ['lnako_lowlevel/シンボリックリンク先取得', 'lnako_lowlevel/ファイル詳細情報取得']},
 {'name': 'パス名変更',
  'kana': 'ぱすめいへんこう',
  'genre': 'ファイルシステム',
  'particles': 'SRCをDSTへ/DSTにSRCを',
  'returns': 'void',
  'implemented': True,
  'capability': 'rename',
  'errors': ['ENOENT',
             'EEXIST',
             'EACCES',
             'EPERM',
             'EXDEV',
             'ENOTEMPTY',
             'EISDIR',
             'ENOTDIR',
             'ELOOP',
             'EROFS',
             'ENOSPC',
             'ENOTSUP',
             'EINVAL'],
  'desc': 'ファイルまたはディレクトリのパスを SRC から DST へ変更（移動）します。POSIX の rename に相当します。',
  'example': 'F = 「/tmp/test_ren_old.txt」を「w+b」でファイル開く。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_ren_old.txt」を「/tmp/test_ren_new.txt」へパス名変更。\n'
             'INFO = 「/tmp/test_ren_new.txt」のファイル詳細情報取得。\n'
             '「/tmp/test_ren_new.txt」をファイルリンク削除。\n'
             'INFO[「kind」]を表示。\n'
             '### lnako表示結果: file',
  'refs': ['lnako_lowlevel/ファイルリンク削除', 'lnako_lowlevel/空フォルダ削除']},
 {'name': 'ファイルリンク削除',
  'kana': 'ふぁいるりんくさくじょ',
  'genre': 'ファイルシステム',
  'particles': 'PATHを/PATHの',
  'returns': 'void',
  'implemented': True,
  'capability': 'unlink',
  'errors': ['ENOENT', 'EACCES', 'EPERM', 'EISDIR', 'ENOTDIR', 'ELOOP', 'EROFS', 'ENOTSUP', 'EINVAL'],
  'desc': '指定したパス PATH のファイルリンク（ディレクトリエントリ）を削除します。ハードリンク数が 0 になるとストレージ上の実体も解放されます。POSIX の unlink '
          'に相当します。ディレクトリに対して実行した場合は EISDIR エラーになります。',
  'example': 'F = 「/tmp/test_unlink.txt」を「w+b」でファイル開く。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_unlink.txt」をファイルリンク削除。\n'
             '「削除成功」と表示。\n'
             '### lnako表示結果: 削除成功',
  'refs': ['lnako_lowlevel/空フォルダ削除', 'lnako_lowlevel/ファイル開く']},
 {'name': '空フォルダ削除',
  'kana': 'からふぉるださくじょ',
  'genre': 'ファイルシステム',
  'particles': 'PATHを/PATHの',
  'returns': 'void',
  'implemented': True,
  'capability': 'rmdir',
  'errors': ['ENOENT', 'ENOTDIR', 'EACCES', 'ENOTEMPTY', 'EPERM', 'ELOOP', 'EROFS', 'ENOTSUP', 'EINVAL'],
  'desc': '指定した空のディレクトリ PATH を削除します。POSIX の rmdir に相当します。中身があるディレクトリでは ENOTEMPTY エラー、通常ファイルでは ENOTDIR エラーになります。',
  'example': '「/tmp/test_rmdir_dir」のフォルダ作成。\n「/tmp/test_rmdir_dir」を空フォルダ削除。\n「フォルダ削除成功」と表示。\n### lnako表示結果: フォルダ削除成功',
  'refs': ['lnako_lowlevel/ファイルリンク削除']},
 {'name': 'ファイルサイズ変更',
  'kana': 'ふぁいるさいずへんこう',
  'genre': 'ファイルメタデータ',
  'particles': 'PATHをSIZEで/PATHをSIZEに',
  'returns': 'void',
  'implemented': True,
  'capability': 'truncate',
  'errors': ['ENOENT', 'EACCES', 'EPERM', 'EISDIR', 'ENOTDIR', 'ELOOP', 'EROFS', 'ENOSPC', 'EINVAL', 'ENOTSUP'],
  'desc': 'パス PATH のファイルサイズを SIZE バイトに変更（切り詰め・拡張）します。POSIX の truncate に相当します。ファイルハンドルを開かずに直接サイズを変更できます。',
  'example': 'H = 「sha256」でハッシュ開始。\n'
             'B = Hをハッシュ完了。\n'
             'F = 「/tmp/test_truncate.bin」を「w+b」でファイル開く。\n'
             'FへBをファイルバイト書く。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_truncate.bin」を8にファイルサイズ変更。\n'
             'INFO = 「/tmp/test_truncate.bin」のファイル詳細情報取得。\n'
             '「/tmp/test_truncate.bin」をファイルリンク削除。\n'
             'INFO[「size」]を表示。\n'
             '### lnako表示結果: 8',
  'refs': ['lnako_lowlevel/ファイル切詰', 'lnako_lowlevel/ファイル詳細情報取得']},
 {'name': 'ファイル時刻設定',
  'kana': 'ふぁいるじこくせってい',
  'genre': 'ファイルメタデータ',
  'particles': 'PATHをATIMEからMTIMEまで/PATHをATIMEとMTIMEで',
  'returns': 'void',
  'implemented': True,
  'capability': 'utime',
  'errors': ['ENOENT', 'EACCES', 'ENOTDIR', 'ELOOP', 'EROFS', 'EINVAL', 'EPERM', 'ENOTSUP'],
  'desc': '指定したパス PATH のファイルに対して、アクセス日時（ATIME）と更新日時（MTIME）を設定します。日時には Unix エポックからのナノ秒単位の整数値（Number または '
          'BigInt）を指定するほか、既存の値を維持する null や現在時刻を表す文字列 "now" を指定できます。POSIX の utimensat に相当します。',
  'example': 'F = 「/tmp/test_utime.txt」を「w+b」でファイル開く。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_utime.txt」を1000000000から2000000000までファイル時刻設定。\n'
             'INFO = 「/tmp/test_utime.txt」のファイル詳細情報取得。\n'
             '「/tmp/test_utime.txt」をファイルリンク削除。\n'
             'もし、(INFO[「mtimeNs」] == 2000000000)ならば\n'
             '\u3000\u3000「時刻設定成功」と表示。\n'
             'ここまで\n'
             '### lnako表示結果: 時刻設定成功',
  'refs': ['lnako_lowlevel/ファイル時刻設定済', 'lnako_lowlevel/ファイル詳細情報取得']},
 {'name': 'ファイル時刻設定済',
  'kana': 'ふぁいるじこくせっていずみ',
  'genre': 'ファイルメタデータ',
  'particles': 'HANDLEをATIMEからMTIMEまで/HANDLEをATIMEとMTIMEで',
  'returns': 'void',
  'implemented': True,
  'capability': 'utime',
  'errors': ['EBADF', 'EACCES', 'EROFS', 'EINVAL', 'EPERM', 'ENOTSUP'],
  'desc': '開いているファイルハンドル HANDLE に対して、アクセス日時（ATIME）と更新日時（MTIME）を設定します。日時にはナノ秒単位の整数値（Number または BigInt）、既存の値を維持する '
          'null、または現在時刻を表す文字列 "now" を指定できます。POSIX の futimens に相当します。',
  'example': 'F = 「/tmp/test_futime.txt」を「w+b」でファイル開く。\n'
             'Fを1000000000から2000000000までファイル時刻設定済。\n'
             'Fをファイル閉じる。\n'
             'INFO = 「/tmp/test_futime.txt」のファイル詳細情報取得。\n'
             '「/tmp/test_futime.txt」をファイルリンク削除。\n'
             'もし、(INFO[「mtimeNs」] == 2000000000)ならば\n'
             '\u3000\u3000「時刻設定済成功」と表示。\n'
             'ここまで\n'
             '### lnako表示結果: 時刻設定済成功',
  'refs': ['lnako_lowlevel/ファイル時刻設定', 'lnako_lowlevel/ファイル開く']},
 {'name': 'ハッシュ開始',
  'kana': 'はっしゅかいし',
  'genre': 'ハッシュストリーム',
  'particles': 'ALGORITHMで/ALGORITHMを',
  'returns': 'handle',
  'implemented': True,
  'capability': 'incremental_hash',
  'errors': ['EINVAL', 'ENOTSUP'],
  'desc': '指定したアルゴリズム ALGORITHM（"sha256", "sha512", "sha1", "md5" など）による逐次ハッシュ計算を開始し、ハッシュハンドルを返します。',
  'example': 'H = 「sha256」でハッシュ開始。\nB = Hをハッシュ完了。\n「ハッシュ開始成功」と表示。\n### lnako表示結果: ハッシュ開始成功',
  'refs': ['lnako_lowlevel/ハッシュ追加', 'lnako_lowlevel/ハッシュ完了', 'lnako_lowlevel/ハッシュ破棄']},
 {'name': 'ハッシュ追加',
  'kana': 'はっしゅついか',
  'genre': 'ハッシュストリーム',
  'particles': 'HANDLEをBYTESで/HANDLEへBYTESを',
  'returns': 'void',
  'implemented': True,
  'capability': 'incremental_hash',
  'errors': ['EBADF', 'EINVAL'],
  'desc': 'ハッシュハンドル HANDLE にバイナリデータ BYTES を逐次追加します。大きなファイルやストリームデータをメモリへ一括で読み込まずに、分割してハッシュを計算できます。',
  'example': 'H1 = 「sha256」でハッシュ開始。\n'
             'B = H1をハッシュ完了。\n'
             'H2 = 「sha256」でハッシュ開始。\n'
             'H2へBをハッシュ追加。\n'
             'R = H2を「hex」でハッシュ完了。\n'
             'Rを表示。\n'
             '### lnako表示結果: 5df6e0e2761359d30a8275058e299fcc0381534545f55cf43e41983f5d4c9456',
  'refs': ['lnako_lowlevel/ハッシュ開始', 'lnako_lowlevel/ハッシュ完了', 'lnako_lowlevel/ハッシュ破棄']},
 {'name': 'ハッシュ完了',
  'kana': 'はっしゅかんりょう',
  'genre': 'ハッシュストリーム',
  'particles': 'HANDLEをENCODINGで/HANDLEを',
  'returns': 'hashDigest',
  'implemented': True,
  'capability': 'incremental_hash',
  'errors': ['EBADF', 'EINVAL', 'ENOTSUP'],
  'desc': 'ハッシュハンドル HANDLE の計算を完了し、計算結果（ダイジェスト）を返します。ENCODING に "hex" や "base64" '
          'を指定すると文字列で返し、省略した場合はバイナリデータ（Bytes）で返します。完了後のハンドルは自動的に閉じられ、再利用すると EBADF エラーになります。',
  'example': 'H = 「sha256」でハッシュ開始。\n'
             'R = Hを「hex」でハッシュ完了。\n'
             'Rを表示。\n'
             '### lnako表示結果: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
  'refs': ['lnako_lowlevel/ハッシュ開始', 'lnako_lowlevel/ハッシュ追加', 'lnako_lowlevel/ハッシュ破棄']},
 {'name': 'ハッシュ破棄',
  'kana': 'はっしゅはき',
  'genre': 'ハッシュストリーム',
  'particles': 'HANDLEを/HANDLEの',
  'returns': 'void',
  'implemented': True,
  'capability': 'incremental_hash',
  'errors': ['EBADF'],
  'desc': '進行中のハッシュハンドル HANDLE を破棄し、リソースを解放します。すでに破棄したハンドルや無効なハンドルを指定すると EBADF エラーになります。',
  'example': 'H = 「sha256」でハッシュ開始。\nHをハッシュ破棄。\n「ハッシュ破棄成功」と表示。\n### lnako表示結果: ハッシュ破棄成功',
  'refs': ['lnako_lowlevel/ハッシュ開始', 'lnako_lowlevel/ハッシュ完了']},
 {'name': 'ディレクトリ開く',
  'kana': 'でぃれくとりひらく',
  'genre': 'ディレクトリ走査',
  'particles': 'PATHを/PATHの',
  'returns': 'handle',
  'implemented': True,
  'capability': 'dir_iterator',
  'errors': ['ENOENT', 'ENOTDIR', 'EACCES', 'EPERM', 'EMFILE', 'ENFILE', 'ENOTSUP'],
  'desc': '指定したパス PATH のディレクトリを開き、逐次走査用のディレクトリハンドルを返します。POSIX の opendir に相当します。',
  'example': 'DH = 「/tmp」をディレクトリ開く。\n'
             'ENT = DHのディレクトリ次取得。\n'
             'DHをディレクトリ閉じる。\n'
             'もし、(ENT != 空)ならば\n'
             '\u3000\u3000「ディレクトリ走査成功」と表示。\n'
             'ここまで\n'
             '### lnako表示結果: ディレクトリ走査成功',
  'refs': ['lnako_lowlevel/ディレクトリ次取得', 'lnako_lowlevel/ディレクトリ閉じる', 'lnako_lowlevel/ディレクトリ列挙時']},
 {'name': 'ディレクトリ次取得',
  'kana': 'でぃれくとりつぎしゅとく',
  'genre': 'ディレクトリ走査',
  'particles': 'HANDLEを/HANDLEの',
  'returns': 'dirEntry',
  'implemented': True,
  'capability': 'dir_iterator',
  'errors': ['EBADF', 'EINVAL', 'ENOTSUP'],
  'desc': 'ディレクトリハンドル HANDLE から次のエントリを取得し、名前 name と種別 type（"file", "directory", "symlink" など）を持つ辞書を返します。POSIX の '
          'readdir に相当します。すべてのエントリを読み終えると null を返します。"." と ".." は結果に含まれません。',
  'example': 'DH = 「/tmp」をディレクトリ開く。\n'
             'ENT = DHのディレクトリ次取得。\n'
             'DHをディレクトリ閉じる。\n'
             'もし、(ENT[「name」] != 「」)ならば\n'
             '\u3000\u3000「エントリ取得成功」と表示。\n'
             'ここまで\n'
             '### lnako表示結果: エントリ取得成功',
  'refs': ['lnako_lowlevel/ディレクトリ開く', 'lnako_lowlevel/ディレクトリ閉じる']},
 {'name': 'ディレクトリ閉じる',
  'kana': 'でぃれくとりとじる',
  'genre': 'ディレクトリ走査',
  'particles': 'HANDLEを/HANDLEの',
  'returns': 'void',
  'implemented': True,
  'capability': 'dir_iterator',
  'errors': ['EBADF'],
  'desc': 'ディレクトリハンドル HANDLE を閉じ、リソースを解放します。POSIX の closedir に相当します。',
  'example': 'DH = 「/tmp」をディレクトリ開く。\nDHをディレクトリ閉じる。\n「ディレクトリクローズ成功」と表示。\n### lnako表示結果: ディレクトリクローズ成功',
  'refs': ['lnako_lowlevel/ディレクトリ開く']},
 {'name': 'ディレクトリ列挙時',
  'kana': 'でぃれくとりれっきょじ',
  'genre': 'ディレクトリ走査',
  'particles': 'PATHをCALLBACKで/PATHのCALLBACKを',
  'returns': 'void',
  'implemented': True,
  'capability': 'dir_iterator',
  'errors': ['ENOENT', 'ENOTDIR', 'EACCES', 'EPERM', 'ENOTSUP'],
  'desc': '指定したディレクトリ PATH 内のエントリを 1 件ずつコールバック関数 CALLBACK に渡して反復実行します。コールバック関数にはエントリ辞書 ENT（name, '
          'type）が引数として渡されます。コールバック関数が真（true）を返すと、その時点で列挙を中断します。',
  'example': 'CNT = 0\n'
             '●(ENTで)カウントCB\n'
             '\u3000\u3000CNT = CNT + 1\n'
             'ここまで\n'
             '「/tmp」を「カウントCB」でディレクトリ列挙時。\n'
             'もし、(CNT > 0)ならば\n'
             '\u3000\u3000「ディレクトリ列挙成功」と表示。\n'
             'ここまで\n'
             '### lnako表示結果: ディレクトリ列挙成功',
  'refs': ['lnako_lowlevel/ディレクトリ開く', 'lnako_lowlevel/ディレクトリ次取得']},
 {'name': 'ファイル権限設定',
  'kana': 'ふぁいるけんげんせってい',
  'genre': '権限・属性管理',
  'particles': 'PATHをMODEで/PATHをMODEに',
  'returns': 'void',
  'implemented': True,
  'capability': 'chmod',
  'errors': ['ENOENT', 'EACCES', 'EPERM', 'ENOTDIR', 'ELOOP', 'EROFS', 'ENOSPC', 'EINVAL', 'ENOTSUP'],
  'desc': '指定したパス PATH のアクセス権限（パーミッション）を数値 MODE（例: 0o644, 0o755）で設定します。POSIX の chmod に相当します。',
  'example': 'F = 「/tmp/test_chmod.txt」を「w+b」でファイル開く。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_chmod.txt」を0o644でファイル権限設定。\n'
             '「/tmp/test_chmod.txt」をファイルリンク削除。\n'
             '「権限設定成功」と表示。\n'
             '### lnako表示結果: 権限設定成功',
  'refs': ['lnako_lowlevel/ファイル所有者設定', 'lnako_lowlevel/ファイルアクセス可能']},
 {'name': 'ファイル所有者設定',
  'kana': 'ふぁいるしょゆうしゃせってい',
  'genre': '権限・属性管理',
  'particles': 'PATHをUIDとGIDで/PATHをUIDにGIDを',
  'returns': 'void',
  'implemented': True,
  'capability': 'chown',
  'errors': ['ENOENT', 'EACCES', 'EPERM', 'ENOTDIR', 'ELOOP', 'EROFS', 'ENOSPC', 'EINVAL', 'ENOTSUP'],
  'desc': '指定したパス PATH の所有者 UID とグループ GID を設定します。POSIX の chown に相当します。変更しない項目には -1 を指定します。',
  'example': '# 「data.txt」を所有者1000、グループ1000に設定する例:\n「data.txt」を1000と1000でファイル所有者設定。',
  'refs': ['lnako_lowlevel/シンボリックリンク所有者設定', 'lnako_lowlevel/ファイル権限設定']},
 {'name': 'シンボリックリンク所有者設定',
  'kana': 'しんぼりっくりんくしょゆうしゃせってい',
  'genre': '権限・属性管理',
  'particles': 'PATHをUIDとGIDで/PATHをUIDにGIDを',
  'returns': 'void',
  'implemented': True,
  'capability': 'chown',
  'errors': ['ENOENT', 'EACCES', 'EPERM', 'ENOTDIR', 'ELOOP', 'EROFS', 'ENOSPC', 'EINVAL', 'ENOTSUP'],
  'desc': '指定したパス PATH の所有者 UID とグループ GID を設定します。PATH がシンボリックリンクの場合でもリンク先を追跡せず、リンク自体の所有者を変更します。POSIX の lchown '
          'に相当します。変更しない項目には -1 を指定します。',
  'example': '# 「link.txt」のシンボリックリンク自体の所有者を変更する例:\n「link.txt」を1000と1000でシンボリックリンク所有者設定。',
  'refs': ['lnako_lowlevel/ファイル所有者設定']},
 {'name': 'ファイルアクセス可能',
  'kana': 'ふぁいるあくせすかのう',
  'genre': '権限・属性管理',
  'particles': 'PATHをMODEで/PATHがMODEで',
  'returns': 'boolean',
  'implemented': True,
  'capability': 'access',
  'errors': ['EINVAL', 'ENOTSUP'],
  'desc': '指定したパス PATH のファイルに対して、現在のプロセスがアクセス権限 MODE（読み取り: 4, 書き込み: 2, 実行: 1, 存在確認: 0）を持つかを判定します。POSIX の access '
          'に相当します。アクセス可能なら true、不可なら false を返します。',
  'example': 'F = 「/tmp/test_access.txt」を「w+b」でファイル開く。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_access.txt」を4でファイルアクセス可能。\n'
             'それを表示。\n'
             '「/tmp/test_access.txt」をファイルリンク削除。\n'
             '### lnako表示結果: true',
  'refs': ['lnako_lowlevel/ファイル権限設定', 'lnako_lowlevel/ファイル詳細情報取得']},
 {'name': 'UID取得',
  'kana': 'UIDしゅとく',
  'genre': '権限・属性管理',
  'particles': '',
  'returns': 'uid',
  'implemented': True,
  'capability': 'uid_gid',
  'errors': ['ENOTSUP'],
  'desc': '現在のプロセスの実ユーザー ID（UID）を数値で返します。POSIX の getuid に相当します。',
  'example': 'UID取得。\nU = それ。\nもし、(U >= 0)ならば\n\u3000\u3000「UID取得成功」と表示。\nここまで\n### lnako表示結果: UID取得成功',
  'refs': ['lnako_lowlevel/EUID取得', 'lnako_lowlevel/GID取得']},
 {'name': 'EUID取得',
  'kana': 'EUIDしゅとく',
  'genre': '権限・属性管理',
  'particles': '',
  'returns': 'uid',
  'implemented': True,
  'capability': 'uid_gid',
  'errors': ['ENOTSUP'],
  'desc': '現在のプロセスの実効ユーザー ID（EUID）を数値で返します。POSIX の geteuid に相当します。',
  'example': 'EUID取得。\nU = それ。\nもし、(U >= 0)ならば\n\u3000\u3000「EUID取得成功」と表示。\nここまで\n### lnako表示結果: EUID取得成功',
  'refs': ['lnako_lowlevel/UID取得']},
 {'name': 'GID取得',
  'kana': 'GIDしゅとく',
  'genre': '権限・属性管理',
  'particles': '',
  'returns': 'gid',
  'implemented': True,
  'capability': 'uid_gid',
  'errors': ['ENOTSUP'],
  'desc': '現在のプロセスの実グループ ID（GID）を数値で返します。POSIX の getgid に相当します。',
  'example': 'GID取得。\nG = それ。\nもし、(G >= 0)ならば\n\u3000\u3000「GID取得成功」と表示。\nここまで\n### lnako表示結果: GID取得成功',
  'refs': ['lnako_lowlevel/EGID取得', 'lnako_lowlevel/UID取得']},
 {'name': 'EGID取得',
  'kana': 'EGIDしゅとく',
  'genre': '権限・属性管理',
  'particles': '',
  'returns': 'gid',
  'implemented': True,
  'capability': 'uid_gid',
  'errors': ['ENOTSUP'],
  'desc': '現在のプロセスの実効グループ ID（EGID）を数値で返します。POSIX の getegid に相当します。',
  'example': 'EGID取得。\nG = それ。\nもし、(G >= 0)ならば\n\u3000\u3000「EGID取得成功」と表示。\nここまで\n### lnako表示結果: EGID取得成功',
  'refs': ['lnako_lowlevel/GID取得']},
 {'name': '所属グループID一覧取得',
  'kana': 'しょぞくぐるーぷIDいちらんしゅとく',
  'genre': '権限・属性管理',
  'particles': '',
  'returns': 'array',
  'implemented': True,
  'capability': 'uid_gid',
  'errors': ['ENOTSUP'],
  'desc': '現在のプロセスが所属している補助グループ ID の一覧を数値の配列で返します。POSIX の getgroups に相当します。',
  'example': '所属グループID一覧取得。\nL = それ。\nもし、(Lの要素数 >= 0)ならば\n\u3000\u3000「グループ取得成功」と表示。\nここまで\n### lnako表示結果: グループ取得成功',
  'refs': ['lnako_lowlevel/GID取得']},
 {'name': 'UMASK変更',
  'kana': 'UMASKへんこう',
  'genre': '権限・属性管理',
  'particles': 'MODEで/MODEを',
  'returns': 'number',
  'implemented': True,
  'capability': 'uid_gid',
  'errors': ['ENOTSUP'],
  'desc': 'プロセスのファイル作成マスク（umask）を指定した MODE に変更し、変更前の旧マスク値を数値で返します。POSIX の umask に相当します。',
  'example': '0o022でUMASK変更。\nOLD = それ。\nOLDでUMASK変更。\n「UMASK設定成功」と表示。\n### lnako表示結果: UMASK設定成功',
  'refs': ['lnako_lowlevel/ファイル権限設定']},
 {'name': 'プロセス起動',
  'kana': 'ぷろせすきどう',
  'genre': 'プロセス・端末制御',
  'particles': 'ARGVをOPTIONSで/ARGVを',
  'returns': 'handle',
  'implemented': True,
  'capability': 'argv_spawn',
  'errors': ['ENOENT', 'EACCES', 'EPERM', 'EINVAL', 'ENOTSUP'],
  'desc': 'シェルを介さずに引数配列 ARGV を直接渡して子プロセスを起動し、プロセスハンドルを返します。POSIX の posix_spawnp / execve に相当します。OPTIONS には作業ディレクトリ cwd '
          'や環境変数 env などを辞書で指定できます。',
  'example': 'PROC = [「true」]をプロセス起動。\n'
             'RES = PROCのプロセス待機。\n'
             'もし、(RES[「exitCode」] == 0)ならば\n'
             '\u3000\u3000「プロセス実行成功」と表示。\n'
             'ここまで\n'
             '### lnako表示結果: プロセス実行成功',
  'refs': ['lnako_lowlevel/プロセス待機', 'lnako_lowlevel/シグナル送信']},
 {'name': 'プロセス待機',
  'kana': 'ぷろせすたいき',
  'genre': 'プロセス・端末制御',
  'particles': 'HANDLEを/HANDLEの',
  'returns': 'waitResult',
  'implemented': True,
  'capability': 'argv_spawn',
  'errors': ['EBADF', 'EINVAL', 'ENOTSUP'],
  'desc': '起動した子プロセス HANDLE の終了を待機し、終了コード exitCode と終了シグナル番号 signal を持つ辞書を返します。POSIX の waitpid に相当します。正常終了時は signal が '
          'null になり、POSIX 環境でシグナルにより終了した場合は exitCode が 128 + signal、signal がそのシグナル番号になります。',
  'example': 'PROC = [「true」]をプロセス起動。\nRES = PROCのプロセス待機。\nRES[「exitCode」]を表示。\n### lnako表示結果: 0',
  'refs': ['lnako_lowlevel/プロセス起動']},
 {'name': 'プロセスID取得',
  'kana': 'ぷろせすIDしゅとく',
  'genre': 'プロセス・端末制御',
  'particles': '',
  'returns': 'pid',
  'implemented': True,
  'capability': 'argv_spawn',
  'errors': ['ENOTSUP'],
  'desc': '自プロセスのプロセス ID（PID）を数値で返します。POSIX の getpid に相当します。',
  'example': 'プロセスID取得。\nPID = それ。\nもし、(PID > 0)ならば\n\u3000\u3000「プロセスID取得成功」と表示。\nここまで\n### lnako表示結果: プロセスID取得成功',
  'refs': ['lnako_lowlevel/親プロセスID取得']},
 {'name': '親プロセスID取得',
  'kana': 'おやぷろせすIDしゅとく',
  'genre': 'プロセス・端末制御',
  'particles': '',
  'returns': 'pid',
  'implemented': True,
  'capability': 'argv_spawn',
  'errors': ['ENOTSUP'],
  'desc': '親プロセスのプロセス ID（PPID）を数値で返します。POSIX の getppid に相当します。',
  'example': '親プロセスID取得。\n'
             'PPID = それ。\n'
             'もし、(PPID > 0)ならば\n'
             '\u3000\u3000「親プロセスID取得成功」と表示。\n'
             'ここまで\n'
             '### lnako表示結果: 親プロセスID取得成功',
  'refs': ['lnako_lowlevel/プロセスID取得']},
 {'name': 'シグナル送信',
  'kana': 'しぐなるそうしん',
  'genre': 'プロセス・端末制御',
  'particles': 'PIDにSIGNALを/PIDへSIGNALで',
  'returns': 'void',
  'implemented': True,
  'capability': 'signal',
  'errors': ['EINVAL', 'EPERM', 'ENOTSUP'],
  'desc': '指定した PID のプロセスに対して POSIX シグナル番号 SIGNAL（SIGTERM: 15, SIGINT: 2 など）を送信します。POSIX の kill に相当します。',
  'example': '# 自プロセスへシグナル0（生存確認）を送信する例:\nプロセスID取得。\nPID = それ。\nPIDに0をシグナル送信。\n「シグナル送信成功」と表示。\n### lnako表示結果: シグナル送信成功',
  'refs': ['lnako_lowlevel/プロセス起動', 'lnako_lowlevel/プロセスID取得']},
 {'name': 'プロセス優先度取得',
  'kana': 'ぷろせすゆうせんどしゅとく',
  'genre': 'プロセス・端末制御',
  'particles': 'PIDを/PIDの',
  'returns': 'number',
  'implemented': True,
  'capability': 'priority',
  'errors': ['EINVAL', 'EPERM', 'ENOTSUP'],
  'desc': '指定した PID のプロセスの実行優先度（niceness 値）を数値で返します。PID に 0 を指定した場合は自プロセスが対象になります。POSIX の getpriority に相当します。',
  'example': '0のプロセス優先度取得。\n'
             'PRIO = それ。\n'
             'もし、(PRIO >= -20 かつ PRIO <= 20)ならば\n'
             '\u3000\u3000「優先度取得成功」と表示。\n'
             'ここまで\n'
             '### lnako表示結果: 優先度取得成功',
  'refs': ['lnako_lowlevel/プロセス優先度設定']},
 {'name': 'プロセス優先度設定',
  'kana': 'ぷろせすゆうせんどせってい',
  'genre': 'プロセス・端末制御',
  'particles': 'PIDをVALUEで/PIDをVALUEに',
  'returns': 'void',
  'implemented': True,
  'capability': 'priority',
  'errors': ['EINVAL', 'EPERM', 'ENOTSUP'],
  'desc': '指定した PID のプロセスの実行優先度（niceness 値）を設定します。PID に 0 を指定した場合は自プロセスが対象になります。POSIX の setpriority '
          'に相当します。優先度を下げる（値を大きくする）操作は一般ユーザーでも可能ですが、優先度を上げる（値を小さくする）操作には管理者権限が必要です。\n'
          '\n'
          '※権限や OS 制約があるため、DocTest では特定値の検証を行っていません。',
  'example': '# 自プロセスの優先度を現在の値のまま再設定する例:\n0のプロセス優先度取得。\nPRIO = それ。\n0をPRIOにプロセス優先度設定。',
  'refs': ['lnako_lowlevel/プロセス優先度取得']},
 {'name': '端末判定',
  'kana': 'たんまつはんてい',
  'genre': 'プロセス・端末制御',
  'particles': 'STREAMを/STREAMで',
  'returns': 'boolean',
  'implemented': True,
  'capability': 'tty_isatty',
  'errors': ['EINVAL', 'ENOTSUP'],
  'desc': '指定したストリーム STREAM（"stdin", "stdout", "stderr"）が端末（TTY）に接続されているかを真偽値（true / false）で返します。POSIX の isatty '
          'に相当します。',
  'example': '「stdin」を端末判定。\n'
             'R = それ。\n'
             'もし、(R == true または R == false)ならば\n'
             '\u3000\u3000「端末判定成功」と表示。\n'
             'ここまで\n'
             '### lnako表示結果: 端末判定成功',
  'refs': ['lnako_lowlevel/端末サイズ取得']},
 {'name': '端末サイズ取得',
  'kana': 'たんまつさいずしゅとく',
  'genre': 'プロセス・端末制御',
  'particles': 'STREAMを/STREAMで',
  'returns': 'ttySize',
  'implemented': True,
  'capability': 'tty_isatty',
  'errors': ['EINVAL', 'ENOTSUP'],
  'desc': '指定したストリーム STREAM（"stdin", "stdout", "stderr"）が接続されている端末画面の行数 rows と列数 columns を辞書で返します。ioctl の TIOCGWINSZ '
          'に相当します。',
  'example': '# 端末サイズを取得する例:\n「stdout」を端末サイズ取得。\nSIZE = それ。',
  'refs': ['lnako_lowlevel/端末判定']},
 {'name': 'ファイルシステム情報取得',
  'kana': 'ふぁいるしすてむじょうほうしゅとく',
  'genre': '高度ファイルシステム',
  'particles': 'PATHを/PATHの',
  'returns': 'fsInfo',
  'implemented': True,
  'capability': 'statfs',
  'errors': ['ENOENT', 'EACCES', 'EPERM', 'ENOTDIR', 'EINVAL', 'ENOTSUP'],
  'desc': '指定したパス PATH が属するファイルシステムの情報（ブロックサイズ blockSize、総ブロック数 blocks、空きブロック数 free、利用可能ブロック数 available、総 i ノード数 files '
          'など）を辞書で返します。POSIX の statvfs / statfs に相当します。',
  'example': 'FS = 「/tmp」のファイルシステム情報取得。\n'
             'もし、(FS[「blockSize」] > 0)ならば\n'
             '\u3000\u3000「FS情報取得成功」と表示。\n'
             'ここまで\n'
             '### lnako表示結果: FS情報取得成功',
  'refs': ['lnako_lowlevel/ファイル詳細情報取得']},
 {'name': 'ファイルクローン',
  'kana': 'ふぁいるくろーん',
  'genre': '高度ファイルシステム',
  'particles': 'SRCをDSTへMODEで/SRCをDSTに',
  'returns': 'void',
  'implemented': True,
  'capability': 'reflink',
  'errors': ['ENOENT', 'EEXIST', 'EACCES', 'EPERM', 'EXDEV', 'ENOTSUP', 'EINVAL'],
  'desc': 'Copy-on-Write（CoW / reflink）機能を使って、SRC から DST へ高速かつ省容量でファイルを複製（クローン）します。APFS や Btrfs などの CoW '
          '対応ファイルシステムで利用でき、非対応の環境では ENOTSUP エラーになります。',
  'example': '# クローン対応環境での例:\n'
             '「stream_file_io」を低レイヤー機能対応判定。\n'
             'F = 「/tmp/test_clone_src.bin」を「w+b」でファイル開く。\n'
             'Fをファイル閉じる。\n'
             '「reflink」を低レイヤー機能対応判定。\n'
             'もし、それがtrueならば\n'
             '\u3000\u3000「/tmp/test_clone_src.bin」を「/tmp/test_clone_dst.bin」にファイルクローン。\n'
             '\u3000\u3000「/tmp/test_clone_dst.bin」をファイルリンク削除。\n'
             'ここまで\n'
             '「/tmp/test_clone_src.bin」をファイルリンク削除。\n'
             '「クローン処理完了」と表示。\n'
             '### lnako表示結果: クローン処理完了',
  'refs': ['lnako_lowlevel/ファイル領域確保']},
 {'name': 'ファイルデータ領域検索',
  'kana': 'ふぁいるでーたりょういきけんさく',
  'genre': '高度ファイルシステム',
  'particles': 'HANDLEをOFFSETで/HANDLEをOFFSETから',
  'returns': 'offset',
  'implemented': True,
  'capability': 'seek_data',
  'errors': ['EBADF', 'EINVAL', 'ENOTSUP'],
  'desc': 'スパースファイルにおいて、指定したオフセット OFFSET 以降でデータが存在する次の位置（SEEK_DATA）を検索し、そのオフセットを返します。成功するとファイルハンドル HANDLE '
          'の現在位置もその位置へ移動します。',
  'example': 'F = 「/tmp/test_seek_data.bin」を「w+b」でファイル開く。\n'
             'Fを0に1024でファイル領域確保。\n'
             'Fを0からファイルデータ領域検索。\n'
             'POS = それ。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_seek_data.bin」をファイルリンク削除。\n'
             'もし、(POS >= 0)ならば\n'
             '\u3000\u3000「データ領域検索成功」と表示。\n'
             'ここまで\n'
             '### lnako表示結果: データ領域検索成功',
  'refs': ['lnako_lowlevel/ファイル空洞領域検索', 'lnako_lowlevel/ファイル領域確保']},
 {'name': 'ファイル空洞領域検索',
  'kana': 'ふぁいるくうどうりょういきけんさく',
  'genre': '高度ファイルシステム',
  'particles': 'HANDLEをOFFSETで/HANDLEをOFFSETから',
  'returns': 'offset',
  'implemented': True,
  'capability': 'seek_hole',
  'errors': ['EBADF', 'EINVAL', 'ENOTSUP'],
  'desc': 'スパースファイルにおいて、指定したオフセット OFFSET 以降で空洞領域（ホール、SEEK_HOLE）が存在する次の位置を検索し、そのオフセットを返します。成功するとファイルハンドル HANDLE '
          'の現在位置もその位置へ移動します。',
  'example': 'F = 「/tmp/test_seek_hole.bin」を「w+b」でファイル開く。\n'
             'Fを0に1024でファイル領域確保。\n'
             'Fを0からファイル空洞領域検索。\n'
             'POS = それ。\n'
             'Fをファイル閉じる。\n'
             '「/tmp/test_seek_hole.bin」をファイルリンク削除。\n'
             'もし、(POS >= 0)ならば\n'
             '\u3000\u3000「空洞領域検索成功」と表示。\n'
             'ここまで\n'
             '### lnako表示結果: 空洞領域検索成功',
  'refs': ['lnako_lowlevel/ファイルデータ領域検索']},
 {'name': 'ファイル領域確保',
  'kana': 'ふぁいるりょういきかくほ',
  'genre': '高度ファイルシステム',
  'particles': 'HANDLEをOFFSETにSIZEで/HANDLEをOFFSETとSIZEで',
  'returns': 'void',
  'implemented': True,
  'capability': 'fallocate',
  'errors': ['EBADF', 'EINVAL', 'ENOSPC', 'ENOTSUP'],
  'desc': 'ファイルハンドル HANDLE に対して、オフセット OFFSET から SIZE バイト分の物理ディスク領域を事前に確保します。POSIX の fallocate / posix_fallocate '
          'に相当します。',
  'example': 'F = 「/tmp/test_falloc.bin」を「w+b」でファイル開く。\n'
             'Fを0に1024でファイル領域確保。\n'
             'Fをファイル閉じる。\n'
             'INFO = 「/tmp/test_falloc.bin」のファイル詳細情報取得。\n'
             '「/tmp/test_falloc.bin」をファイルリンク削除。\n'
             'もし、(INFO[「size」] >= 1024)ならば\n'
             '\u3000\u3000「領域確保成功」と表示。\n'
             'ここまで\n'
             '### lnako表示結果: 領域確保成功',
  'refs': ['lnako_lowlevel/ファイル切詰', 'lnako_lowlevel/ファイルデータ領域検索']},
 {'name': '低レイヤー機能対応判定',
  'kana': 'ていれいやーきのうたいおうはんてい',
  'genre': '機能問い合わせ',
  'particles': 'NAMEの/NAMEを',
  'returns': 'boolean',
  'implemented': True,
  'capability': None,
  'errors': [],
  'desc': '現在の実行環境（OS やファイルシステム）で、指定した低レイヤー機能 NAME（capability ID）が利用できるかを判定します。対応していれば true、非対応または未知の機能名であれば false '
          'を返します。',
  'example': '「stream_file_io」を低レイヤー機能対応判定。\n'
             'それを表示。\n'
             '「unknown_cap」を低レイヤー機能対応判定。\n'
             'それを表示。\n'
             '### lnako表示結果: true\n'
             '### false',
  'refs': ['lnako_lowlevel/低レイヤー機能一覧取得']},
 {'name': '低レイヤー機能一覧取得',
  'kana': 'ていれいやーきのういちらんしゅとく',
  'genre': '機能問い合わせ',
  'particles': '',
  'returns': 'array',
  'implemented': True,
  'capability': None,
  'errors': [],
  'desc': 'lnako ランタイムが定義している低レイヤー機能（capability ID）の一覧を文字列の配列で返します。',
  'example': '一覧 = 低レイヤー機能一覧取得。\nN = 一覧の要素数。\nもし、N > 0ならば\n\u3000\u3000「機能一覧取得成功」と表示。\nここまで\n### lnako表示結果: 機能一覧取得成功',
  'refs': ['lnako_lowlevel/低レイヤー機能対応判定']},
 {'name': 'ロケール文字列比較',
  'kana': 'ろけーるもじれつひかく',
  'genre': '国際化・表示幅',
  'particles': 'AをBとOPTIONSで/AをBと',
  'returns': 'number',
  'implemented': True,
  'capability': 'locale_collate',
  'errors': ['EINVAL', 'ENOTSUP'],
  'desc': 'ロケールの照合規則に従って文字列 A と文字列 B を比較します。A < B ならば -1、A = B ならば 0、A > B ならば 1 を返します。OPTIONS には locale キーを持つ辞書（例: '
          '{"locale": "ja_JP.UTF-8"}）を指定できます。OPTIONS を省略した場合や C ロケール（"C", "POSIX", "C.UTF-8" など）を指定した場合は、UTF-8 '
          'バイト列の辞書順で比較します。',
  'example': '「apple」を「banana」とロケール文字列比較。\nC = それ。\nもし、(C < 0)ならば\n\u3000\u3000「比較成功」と表示。\nここまで\n### lnako表示結果: 比較成功',
  'refs': ['lnako_lowlevel/文字表示幅取得']},
 {'name': '文字表示幅取得',
  'kana': 'もじひょうじはばしゅとく',
  'genre': '国際化・表示幅',
  'particles': 'TEXTの',
  'returns': 'number',
  'implemented': True,
  'capability': 'display_width',
  'errors': ['EINVAL'],
  'desc': '文字列 TEXT を端末（ターミナル）に表示したときの幅（半角文字換算のカラム数）を計算して返します。全角文字、半角カタカナ、絵文字、結合文字、制御文字などを考慮した表示幅を算出します。',
  'example': '「なでしこ3」の文字表示幅取得。\nそれを表示。\n### lnako表示結果: 9',
  'refs': ['lnako_lowlevel/ロケール文字列比較']}]

FALLBACK_META = {'JSON_E': ('plugin_system',
            'JSON',
            'JSON_E',
            '関数',
            'JSON_E',
            'Vを|Vの',
            'オブジェクトVをJSON形式の文字列に変換して返す(『JSON変換』と同じ)',
            'https://github.com/kujirahand/nadesiko3/blob/master/core/src/plugin_system_json.mts#L53'),
 'JSON_ES': ('plugin_system',
             'JSON',
             'JSON_ES',
             '関数',
             'JSON_ES',
             'Vを|Vの',
             'オブジェクトVをJSON形式の文字列(整形済み)に変換して返す(『JSONエンコード整形』と同じ)',
             'https://github.com/kujirahand/nadesiko3/blob/master/core/src/plugin_system_json.mts#L61'),
 'JSON_D': ('plugin_system',
            'JSON',
            'JSON_D',
            '関数',
            'JSON_D',
            'Sを|Sの|Sから',
            'JSON文字列Sをオブジェクトにして返す(『JSON取得』と同じ)',
            'https://github.com/kujirahand/nadesiko3/blob/master/core/src/plugin_system_json.mts#L69'),
 '秒逐次待機': ('plugin_system',
           'タイマー',
           '秒逐次待機',
           '関数',
           'びょうちくじたいき',
           'N',
           '(非推奨) 逐次実行構文にて、N秒の間待機する (廃止予定)(非同期関数)',
           'https://github.com/kujirahand/nadesiko3/blob/master/core/src/plugin_system_timer.mts#L53'),
 'LINE送信': ('plugin_node',
            'LINE',
            'LINE送信',
            '関数',
            'LINEそうしん',
            '_TOKENへ_MESSAGEを|_TOKENに',
            'LINEにメッセージを送信する。現在利用不可能。',
            'https://github.com/kujirahand/nadesiko3/tree/master/src/plugin_node.mts#L1608'),
 'LINE画像送信': ('plugin_node',
              'LINE',
              'LINE画像送信',
              '関数',
              'LINEがぞうそうしん',
              '_TOKENへ_IMAGEFILEと_MESSAGEを|_TOKENに',
              'LINEにメッセージを送信する。先にLINE Notifyのページで宛先のトークンを取得する。TOKENへIMAGE_FILEとMESSAGEをLINE画像送信する。',
              'https://github.com/kujirahand/nadesiko3/tree/master/src/plugin_node.mts#L1616')}

COMPAT_JS_DOCS = {'JS実行': '▲lnako での動作\n'
         '\n'
         '[[lnako]] の通常モードでは JavaScript 互換機能が無効になっており、そのまま呼び出すと `ENOTSUP` エラーになります。\n'
         'コマンドライン引数に `--compat-js` フラグを付けて実行したときのみ、内蔵の QuickJS エンジンを使って JavaScript コードを評価・実行できます。\n'
         '\n'
         '#include(plugin_system/JS実行)\n',
 'JSオブジェクト取得': '▲lnako での動作\n'
               '\n'
               '[[lnako]] の通常モードでは JavaScript 互換機能が無効になっており、そのまま呼び出すと `ENOTSUP` エラーになります。\n'
               'コマンドライン引数に `--compat-js` フラグを付けて実行したときのみ利用できます。なでしこ3の関数オブジェクトを取得する場合は、`{関数}関数名` 構文を使ってください。\n'
               '\n'
               '#include(plugin_system/JSオブジェクト取得)\n',
 'JS関数実行': '▲lnako での動作\n'
           '\n'
           '[[lnako]] の通常モードでは JavaScript 互換機能が無効になっており、そのまま呼び出すと `ENOTSUP` エラーになります。\n'
           'コマンドライン引数に `--compat-js` フラグを付けて実行したときのみ、内蔵の QuickJS エンジン上の JavaScript 関数を呼び出せます。\n'
           '\n'
           '#include(plugin_system/JS関数実行)\n',
 'JSメソッド実行': '▲lnako での動作\n'
             '\n'
             '[[lnako]] の通常モードでは JavaScript 互換機能が無効になっており、そのまま呼び出すと `ENOTSUP` エラーになります。\n'
             'コマンドライン引数に `--compat-js` フラグを付けて実行したときのみ、内蔵の QuickJS エンジン上の JavaScript オブジェクトのメソッドを呼び出せます。\n'
             '\n'
             '#include(plugin_system/JSメソッド実行)\n'}

CUSTOM_NODE_DOCS = {'起動待機': '▲説明\n'
         '\n'
         'シェルコマンド S を実行し、その終了を待ってから標準出力を文字列で返します。『[[lnako_node/コマンド実行]]』と同じ動作です。\n'
         '\n'
         '▲利用例\n'
         '\n'
         '{{{#nako3\n'
         '結果 = 「echo hello」を起動待機。\n'
         '「結果:{結果のトリム}」と表示。\n'
         '### lnako表示結果: 結果:hello\n'
         '}}}\n'
         '\n'
         '▲参考\n'
         '\n'
         '- [[lnako_node/起動]]\n'
         '- [[lnako_node/起動時]]\n'
         '- [[lnako_node/コマンド実行]]\n',
 '起動時': '▲説明\n'
        '\n'
        'シェルコマンド B を実行し、その終了を待ってからコールバック関数 A を実行します。コマンドの標準出力はシステム変数『対象』に代入され、コールバック関数 A の第 1 引数にも渡されます。\n'
        '\n'
        '▲利用例\n'
        '\n'
        '{{{#nako3\n'
        '●(Sで)起動CB\n'
        '\u3000\u3000「コールバック:{Sのトリム}」と表示。\n'
        'ここまで\n'
        '「起動CB」で「echo 起動テスト」を起動時。\n'
        '### lnako表示結果: コールバック:起動テスト\n'
        '}}}\n'
        '\n'
        '▲参考\n'
        '\n'
        '- [[lnako_node/起動待機]]\n'
        '- [[lnako_node/起動]]\n',
 'フォルダ存在': '▲説明\n'
           '\n'
           '指定したパス DIR がフォルダ（ディレクトリ）として存在するかを真偽値（true / false）で返します。パスが存在しても通常ファイルである場合は false '
           'を返します。『[[lnako_node/ディレクトリ存在]]』と同じ動作です。\n'
           '\n'
           '▲利用例\n'
           '\n'
           '{{{#nako3\n'
           'TMP = 一時フォルダ作成。\n'
           '「フォルダ:{TMPがフォルダ存在}」と表示。\n'
           '「a」を(TMP & "/a.txt")に保存。\n'
           '「ファイルはフォルダではない:{(TMP & "/a.txt")がフォルダ存在}」と表示。\n'
           '### lnako表示結果: フォルダ:true\n'
           '### ファイルはフォルダではない:false\n'
           '}}}\n'
           '\n'
           '▲参考\n'
           '\n'
           '- [[lnako_node/ディレクトリ存在]]\n'
           '- [[lnako_node/存在]]\n'
           '- [[lnako_node/フォルダ作成]]\n',
 'ファイル移動時': '▲説明\n'
            '\n'
            'パス S1 からパス S2 へファイルまたはフォルダを移動し、完了したあとにコールバック関数 F を実行します。\n'
            '\n'
            '▲利用例\n'
            '\n'
            '{{{#nako3\n'
            'TMP = 一時フォルダ作成。\n'
            '「data」を(TMP & "/a.txt")に保存。\n'
            '●移動CB\n'
            '\u3000\u3000「移動完了」と表示。\n'
            '\u3000\u3000「移動先存在:{(TMP & "/moved.txt")が存在}」と表示。\n'
            'ここまで\n'
            '「移動CB」で(TMP & "/a.txt")から(TMP & "/moved.txt")へファイル移動時。\n'
            '### lnako表示結果: 移動完了\n'
            '### 移動先存在:true\n'
            '}}}\n'
            '\n'
            '▲参考\n'
            '\n'
            '- [[lnako_node/ファイル移動]]\n'
            '- [[lnako_node/ファイルコピー時]]\n',
 'ファイル削除時': '▲説明\n'
            '\n'
            '指定したパス S のファイルを削除し、完了したあとにコールバック関数 F を実行します。\n'
            '\n'
            '▲利用例\n'
            '\n'
            '{{{#nako3\n'
            'TMP = 一時フォルダ作成。\n'
            '「z」を(TMP & "/z.txt")に保存。\n'
            '●削除CB\n'
            '\u3000\u3000「削除完了」と表示。\n'
            '\u3000\u3000「削除後:{(TMP & "/z.txt")が存在}」と表示。\n'
            'ここまで\n'
            '「削除CB」で(TMP & "/z.txt")をファイル削除時。\n'
            '### lnako表示結果: 削除完了\n'
            '### 削除後:false\n'
            '}}}\n'
            '\n'
            '▲参考\n'
            '\n'
            '- [[lnako_node/ファイル削除]]\n',
 'ファイル情報取得': '▲説明\n'
             '\n'
             '指定したパス S のファイルまたはフォルダの統計情報（stat）を調べ、辞書として返します。\n'
             '返される辞書には `size`（バイト単位のサイズ）、`mtimeMs`（更新日時ミリ秒）、`ctimeMs`、`atimeMs`、`ino`、`nlink`、`blksize` '
             'などのキーに加え、`isFile`、`isDirectory`、`isSymbolicLink` などの判定メソッドが含まれます。\n'
             '\n'
             '▲利用例\n'
             '\n'
             '{{{#nako3\n'
             'TMP = 一時フォルダ作成。\n'
             '「hello」を(TMP & "/f.txt")に保存。\n'
             'INFO = (TMP & "/f.txt")のファイル情報取得。\n'
             '「サイズ:{INFO["size"]}」と表示。\n'
             '### lnako表示結果: サイズ:5\n'
             '}}}\n'
             '\n'
             '▲参考\n'
             '\n'
             '- [[lnako_node/ファイルサイズ取得]]\n'
             '- [[lnako_lowlevel/ファイル詳細情報取得]]\n',
 '母艦パス': '▲説明\n'
         '\n'
         '実行中のメインスクリプトが置かれているディレクトリのパスを保持するシステム変数です。\n'
         '\n'
         '▲利用例\n'
         '\n'
         '{{{#nako3\n'
         '# 母艦パスを表示する例\n'
         '母艦パスを表示。\n'
         '}}}\n'
         '\n'
         'スクリプトの配置場所によって結果が変わるため、DocTest では実行結果を検証していません。\n'
         '\n'
         '▲参考\n'
         '\n'
         '- [[lnako_node/母艦パス取得]]\n'
         '- [[lnako_node/作業フォルダ取得]]\n',
 '母艦パス取得': '▲説明\n'
           '\n'
           '実行中のメインスクリプトが置かれているディレクトリのパスを返します。\n'
           '\n'
           '▲利用例\n'
           '\n'
           '{{{#nako3\n'
           '母艦パス取得を表示。\n'
           '}}}\n'
           '\n'
           'スクリプトの配置場所によって結果が変わるため、DocTest では実行結果を検証していません。\n'
           '\n'
           '▲参考\n'
           '\n'
           '- [[lnako_node/母艦パス]]\n'
           '- [[lnako_node/作業フォルダ取得]]\n',
 '環境変数一覧取得': '▲説明\n'
             '\n'
             '現在のプロセスに設定されているすべての環境変数を、変数名をキー、設定値を値とする辞書として返します。\n'
             '\n'
             '▲利用例\n'
             '\n'
             '{{{#nako3\n'
             '一覧 = 環境変数一覧取得。\n'
             '「取得成功:{(一覧の型) != ""}」と表示。\n'
             '### lnako表示結果: 取得成功:true\n'
             '}}}\n'
             '\n'
             '▲参考\n'
             '\n'
             '- [[lnako_node/環境変数取得]]\n',
 '圧縮解凍ツールパス変更': '▲説明\n'
                '\n'
                '圧縮・解凍に使う外部ツールのパス S をシステム変数『[[lnako_node/圧縮解凍ツールパス]]』に設定します。\n'
                '[[lnako]] の『[[lnako_node/圧縮]]』『[[lnako_node/解凍]]』は、初期状態では内蔵の ZIP '
                '処理（stored-ZIP）を使うため外部ツールを必要としません。この命令で外部コマンド（例: `7z` や `unzip`）のパスを設定した場合は、その外部コマンドを呼び出して圧縮・解凍を行います。\n'
                '\n'
                '▲利用例\n'
                '\n'
                '{{{#nako3\n'
                '「7z」に圧縮解凍ツールパス変更。\n'
                '「ツール:{圧縮解凍ツールパス}」と表示。\n'
                '### lnako表示結果: ツール:7z\n'
                '}}}\n'
                '\n'
                '▲参考\n'
                '\n'
                '- [[lnako_node/圧縮]]\n'
                '- [[lnako_node/解凍]]\n'
                '- [[lnako_node/圧縮解凍ツールパス]]\n',
 '圧縮': '▲説明\n'
       '\n'
       'パス FILE で指定したファイルまたはフォルダを ZIP 形式でアーカイブし、パス ZIP へ保存します。フォルダを指定した場合は中身を再帰的に格納します。\n'
       '[[lnako]] は内蔵の ZIP 処理（stored-ZIP）を標準で使うため、7-Zip '
       'などの外部ツールを導入しなくても動作します。『[[lnako_node/圧縮解凍ツールパス変更]]』で外部ツールを指定した場合は、そのツールを呼び出します。\n'
       '\n'
       '▲利用例\n'
       '\n'
       '{{{#nako3\n'
       'TMP = 一時フォルダ作成。\n'
       '(TMP & "/src")のフォルダ作成。\n'
       '「data」を(TMP & "/src/a.txt")に保存。\n'
       '(TMP & "/src")から(TMP & "/out.zip")へ圧縮。\n'
       '「ZIP作成:{(TMP & "/out.zip")が存在}」と表示。\n'
       '### lnako表示結果: ZIP作成:true\n'
       '}}}\n'
       '\n'
       '▲参考\n'
       '\n'
       '- [[lnako_node/解凍]]\n'
       '- [[lnako_node/圧縮時]]\n'
       '- [[lnako_node/圧縮解凍ツールパス変更]]\n',
 '解凍': '▲説明\n'
       '\n'
       'ZIP ファイル ZIP を展開し、フォルダ PATH へ書き出します。\n'
       '[[lnako]] は内蔵の ZIP 展開処理を標準で使うため、外部ツールなしで動作します。展開時には、展開先ディレクトリの外への書き出し（Zip Slip）を防ぐ検査を行います。\n'
       '\n'
       '▲利用例\n'
       '\n'
       '{{{#nako3\n'
       'TMP = 一時フォルダ作成。\n'
       '「data」を(TMP & "/a.txt")に保存。\n'
       '(TMP & "/a.txt")から(TMP & "/out.zip")へ圧縮。\n'
       '(TMP & "/out.zip")から(TMP & "/dest")へ解凍。\n'
       '「復元:{(TMP & "/dest/a.txt")を開く}」と表示。\n'
       '### lnako表示結果: 復元:data\n'
       '}}}\n'
       '\n'
       '▲参考\n'
       '\n'
       '- [[lnako_node/圧縮]]\n'
       '- [[lnako_node/解凍時]]\n'
       '- [[lnako_node/圧縮解凍ツールパス変更]]\n',
 '圧縮時': '▲説明\n'
        '\n'
        '『[[lnako_node/圧縮]]』と同様にパス FILE をパス ZIP へ ZIP 圧縮し、完了したあとにコールバック関数 F を実行します。\n'
        '\n'
        '▲利用例\n'
        '\n'
        '{{{#nako3\n'
        'TMP = 一時フォルダ作成。\n'
        '(TMP & "/src")のフォルダ作成。\n'
        '「data」を(TMP & "/src/a.txt")に保存。\n'
        '●圧縮CB\n'
        '\u3000\u3000「圧縮完了」と表示。\n'
        'ここまで\n'
        '「圧縮CB」で(TMP & "/src")から(TMP & "/out.zip")へ圧縮時。\n'
        '### lnako表示結果: 圧縮完了\n'
        '}}}\n'
        '\n'
        '▲参考\n'
        '\n'
        '- [[lnako_node/圧縮]]\n'
        '- [[lnako_node/解凍時]]\n',
 '解凍時': '▲説明\n'
        '\n'
        '『[[lnako_node/解凍]]』と同様に ZIP ファイル ZIP をフォルダ PATH へ展開し、完了したあとにコールバック関数 F を実行します。\n'
        '\n'
        '▲利用例\n'
        '\n'
        '{{{#nako3\n'
        'TMP = 一時フォルダ作成。\n'
        '「data」を(TMP & "/a.txt")に保存。\n'
        '(TMP & "/a.txt")から(TMP & "/out.zip")へ圧縮。\n'
        '●解凍CB\n'
        '\u3000\u3000「解凍完了」と表示。\n'
        '\u3000\u3000「復元:{(TMP & "/dest/a.txt")が存在}」と表示。\n'
        'ここまで\n'
        '「解凍CB」で(TMP & "/out.zip")から(TMP & "/dest")へ解凍時。\n'
        '### lnako表示結果: 解凍完了\n'
        '### 復元:true\n'
        '}}}\n'
        '\n'
        '▲参考\n'
        '\n'
        '- [[lnako_node/解凍]]\n'
        '- [[lnako_node/圧縮時]]\n',
 '標準入力取得時': '▲説明\n'
            '\n'
            '標準入力から 1 行読み取り、コールバック関数 F を実行します。読み取った文字列はシステム変数『対象』に代入され、コールバック関数 F の第 1 引数にも渡されます。\n'
            '\n'
            '▲利用例\n'
            '\n'
            '{{{#nako3\n'
            '●(Sで)入力CB\n'
            '\u3000\u3000「受取:{S}」と表示。\n'
            'ここまで\n'
            '「入力CB」を標準入力取得時。\n'
            '}}}\n'
            '\n'
            '対話的な標準入力が必要なため、DocTest では実行結果を検証していません。\n'
            '\n'
            '▲参考\n'
            '\n'
            '- [[lnako_node/標準入力全取得]]\n'
            '- [[lnako_node/尋]]\n',
 'ASSERT等': '▲説明\n'
            '\n'
            'テスト用のアサーション命令で、値 A と値 B が等しいかを検証します。等しい場合は true を返し、一致しない場合はアサーション失敗エラーを発生させてプログラムを停止します。\n'
            '\n'
            '▲利用例\n'
            '\n'
            '{{{#nako3\n'
            '(1 + 2)と3がASSERT等。\n'
            '「テスト成功」と表示。\n'
            '### lnako表示結果: テスト成功\n'
            '}}}\n'
            '\n'
            '▲参考\n'
            '\n'
            '- [[lnako_node/ハッシュ値計算]]\n',
 'AJAX送信時': '▲説明\n'
            '\n'
            '指定した URL へ HTTP GET リクエストを送信し、レスポンスを受信したあとにコールバック関数を実行します。取得したレスポンス本文はシステム変数『対象』に代入され、コールバック関数の第 1 '
            '引数にも渡されます。通信に失敗した場合は、『[[lnako_node/AJAX失敗時]]』で登録した関数を呼び出します。\n'
            '\n'
            '▲利用例\n'
            '\n'
            '{{{#nako3\n'
            '●受信完了とは\n'
            '\u3000\u3000「応答: {対象}」と表示。\n'
            'ここまで\n'
            '「受信完了」の「https://example.com/」までAJAX送信時。\n'
            '}}}\n'
            '\n'
            '外部サーバーと通信するため、DocTest では実行結果を検証していません。\n'
            '\n'
            '▲参考\n'
            '\n'
            '- [[lnako_node/AJAXテキスト取得]]\n'
            '- [[lnako_node/GET送信時]]\n'
            '- [[lnako_node/AJAX失敗時]]\n',
 'GET送信時': '▲説明\n'
           '\n'
           '指定した URL へ HTTP GET リクエストを送信し、レスポンスを受信したあとにコールバック関数を実行します。取得したレスポンス本文はシステム変数『対象』に代入され、コールバック関数の第 1 '
           '引数にも渡されます。『[[lnako_node/AJAX送信時]]』の別名です。\n'
           '\n'
           '▲利用例\n'
           '\n'
           '{{{#nako3\n'
           '●受信完了とは\n'
           '\u3000\u3000「応答: {対象}」と表示。\n'
           'ここまで\n'
           '「受信完了」の「https://example.com/」までGET送信時。\n'
           '}}}\n'
           '\n'
           '外部サーバーと通信するため、DocTest では実行結果を検証していません。\n'
           '\n'
           '▲参考\n'
           '\n'
           '- [[lnako_node/AJAX送信時]]\n'
           '- [[lnako_node/AJAXテキスト取得]]\n'
           '- [[lnako_node/AJAX失敗時]]\n',
 'POST送信時': '▲説明\n'
            '\n'
            '指定した URL へ辞書データ PARAMS を URL エンコード形式（`application/x-www-form-urlencoded`）で HTTP POST '
            '送信し、レスポンスを受信したあとにコールバック関数を実行します。取得したレスポンス本文はシステム変数『対象』に代入され、コールバック関数の第 1 引数にも渡されます。\n'
            '\n'
            '▲利用例\n'
            '\n'
            '{{{#nako3\n'
            '●送信完了とは\n'
            '\u3000\u3000「応答: {対象}」と表示。\n'
            'ここまで\n'
            'P = {"name": "太郎", "age": "20"}\n'
            '「送信完了」の「https://example.com/api」までPをPOST送信時。\n'
            '}}}\n'
            '\n'
            '外部サーバーと通信するため、DocTest では実行結果を検証していません。\n'
            '\n'
            '▲参考\n'
            '\n'
            '- [[lnako_node/POSTデータ生成]]\n'
            '- [[lnako_node/POSTフォーム送信時]]\n'
            '- [[lnako_node/AJAX失敗時]]\n',
 'POSTフォーム送信時': '▲説明\n'
                '\n'
                '指定した URL へ辞書データ PARAMS をフォームデータとして HTTP POST '
                '送信し、レスポンスを受信したあとにコールバック関数を実行します。取得したレスポンス本文はシステム変数『対象』に代入され、コールバック関数の第 1 引数にも渡されます。\n'
                '\n'
                '▲利用例\n'
                '\n'
                '{{{#nako3\n'
                '●送信完了とは\n'
                '\u3000\u3000「応答: {対象}」と表示。\n'
                'ここまで\n'
                'P = {"name": "太郎", "age": "20"}\n'
                '「送信完了」の「https://example.com/api」までPをPOSTフォーム送信時。\n'
                '}}}\n'
                '\n'
                '外部サーバーと通信するため、DocTest では実行結果を検証していません。\n'
                '\n'
                '▲参考\n'
                '\n'
                '- [[lnako_node/POST送信時]]\n'
                '- [[lnako_node/AJAX失敗時]]\n',
 'AJAX失敗時': '▲説明\n'
            '\n'
            '『[[lnako_node/AJAX送信時]]』『[[lnako_node/GET送信時]]』『[[lnako_node/POST送信時]]』などの非同期 HTTP '
            '通信命令でエラーが発生したときに呼び出すコールバック関数を登録します。\n'
            '\n'
            '▲利用例\n'
            '\n'
            '{{{#nako3\n'
            '●通信エラー処理(ERR)とは\n'
            '\u3000\u3000「通信に失敗しました: {ERR}」と表示。\n'
            'ここまで\n'
            '「通信エラー処理」にAJAX失敗時。\n'
            '}}}\n'
            '\n'
            '▲参考\n'
            '\n'
            '- [[lnako_node/AJAX送信時]]\n'
            '- [[lnako_node/GET送信時]]\n'
            '- [[lnako_node/POST送信時]]\n',
 'AJAXオプション': '▲説明\n'
              '\n'
              'HTTP 通信（AJAX / Fetch）命令で使うオプション辞書を保持するシステム変数です。`method`（HTTP '
              'メソッド）、`headers`（リクエストヘッダ辞書）、`body`（送信ボディ）などを指定できます。\n'
              '\n'
              '▲利用例\n'
              '\n'
              '{{{#nako3\n'
              'AJAXオプションを表示。\n'
              '}}}\n'
              '\n'
              '▲参考\n'
              '\n'
              '- [[lnako_node/AJAXオプション設定]]\n'
              '- [[lnako_node/AJAXテキスト取得]]\n',
 'AJAXオプション設定': '▲説明\n'
                '\n'
                'HTTP 通信（AJAX / Fetch）命令で使うオプション辞書をシステム変数『[[lnako_node/AJAXオプション]]』に設定します。\n'
                '\n'
                '▲利用例\n'
                '\n'
                '{{{#nako3\n'
                '{"headers": {"X-Custom": "1"}}にAJAXオプション設定。\n'
                'AJAXオプション["headers"]["X-Custom"]を表示。\n'
                '### lnako表示結果: 1\n'
                '}}}\n'
                '\n'
                '▲参考\n'
                '\n'
                '- [[lnako_node/AJAXオプション]]\n'
                '- [[lnako_node/AJAXテキスト取得]]\n',
 'SJIS取得': '▲説明\n'
           '\n'
           'Shift_JIS のバイト列（バイナリデータ）を UTF-8 の文字列にデコードして返します。『[[lnako_node/SJIS変換]]』で変換したバイナリデータを元の文字列に戻すときに使います。\n'
           '\n'
           '▲利用例\n'
           '\n'
           '{{{#nako3\n'
           'BIN = 「こんにちは」をSJIS変換。\n'
           'S = BINからSJIS取得。\n'
           'Sを表示。\n'
           '### lnako表示結果: こんにちは\n'
           '}}}\n'
           '\n'
           '▲参考\n'
           '\n'
           '- [[lnako_node/SJIS変換]]\n'
           '- [[lnako_node/エンコーディング取得]]\n'
           '- [[lnako_node/エンコーディング変換]]\n',
 'エンコーディング変換': '▲説明\n'
               '\n'
               'UTF-8 の文字列 S を指定した文字コード CODE のバイト列（バイナリデータ）へ変換して返します。\n'
               '[[lnako]] は文字コード変換エンジンを内蔵しており、`UTF-8`、`Shift_JIS`（`sjis` / `cp932`）、`EUC-JP`（`euc-jp`）、`UTF-16` / '
               '`UTF-16LE` / `UTF-16BE`、`UTF-32` / `UTF-32LE` / '
               '`UTF-32BE`、`CESU-8`、`UTF-7`、`ASCII`、`latin1`、`hex`、`base64` などに対応しています。\n'
               '\n'
               '▲利用例\n'
               '\n'
               '{{{#nako3\n'
               'BIN = 「あいう」を「sjis」へエンコーディング変換。\n'
               'S = BINを「sjis」でエンコーディング取得。\n'
               'Sを表示。\n'
               '### lnako表示結果: あいう\n'
               '}}}\n'
               '\n'
               '▲参考\n'
               '\n'
               '- [[lnako_node/エンコーディング取得]]\n'
               '- [[lnako_node/SJIS変換]]\n'
               '- [[lnako_node/SJIS取得]]\n',
 'エンコーディング取得': '▲説明\n'
               '\n'
               '文字コード CODE のバイト列（バイナリデータ）を UTF-8 の文字列へデコードして返します。\n'
               '`Shift_JIS`（`sjis`）、`EUC-JP`、`UTF-8`、`UTF-16`、`UTF-16LE`、`UTF-16BE`、`UTF-32`、`CESU-8`、`UTF-7`、`ASCII`、`latin1`、`hex`、`base64` '
               'などの文字コード名を指定できます。\n'
               '\n'
               '▲利用例\n'
               '\n'
               '{{{#nako3\n'
               'BIN = 「なでしこ3」を「euc-jp」へエンコーディング変換。\n'
               'S = BINを「euc-jp」でエンコーディング取得。\n'
               'Sを表示。\n'
               '### lnako表示結果: なでしこ3\n'
               '}}}\n'
               '\n'
               '▲参考\n'
               '\n'
               '- [[lnako_node/エンコーディング変換]]\n'
               '- [[lnako_node/SJIS取得]]\n'
               '- [[lnako_node/SJIS変換]]\n'}

def main():
    os.makedirs(os.path.join(DATA_DIR, 'lnako'), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, 'lnako_node'), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, 'lnako_lowlevel'), exist_ok=True)

    # Read metadata from data/nako3commands.db
    src_conn = sqlite3.connect(NAKO3_DB_PATH)
    src_cur = src_conn.cursor()
    src_cur.execute("SELECT plugin, genre, name, type, kana, args, desc, src_url FROM commands")
    meta_by_plug_name = {}
    meta_by_name = {}
    for row in src_cur.fetchall():
        plug, genre, name, ctype, kana, args, desc, src_url = row
        meta_by_plug_name[(plug, name)] = row
        if name not in meta_by_name:
            meta_by_name[name] = row
    src_conn.close()

    for name, row in FALLBACK_META.items():
        plug = row[0]
        meta_by_plug_name.setdefault((plug, name), row)
        meta_by_name.setdefault(name, row)

    # Create data/lnako-commands.db
    if os.path.exists(LNAKO_DB_PATH):
        os.remove(LNAKO_DB_PATH)
    conn = sqlite3.connect(LNAKO_DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE commands (
            command_id INTEGER PRIMARY KEY,
            pagename TEXT,
            plugin TEXT,
            genre TEXT,
            name TEXT,
            type TEXT,
            kana TEXT,
            args TEXT,
            desc TEXT,
            src_url TEXT,
            ctime INTEGER,
            mtime INTEGER
        )
    """)
    cur.execute("""
        CREATE TABLE plugins (
            plugin_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            desc TEXT,
            nakotype TEXT
        )
    """)

    plugins_rows = [
        ('lnako', 'なでしこ3(高速ネイティブ版) 基本命令', '基本プラグイン,lnako'),
        ('lnako_node', 'lnako PC・コンソール向け命令 (plugin_node互換)', '基本プラグイン,lnako'),
        ('lnako_lowlevel', 'lnako 低レイヤーAPI命令', '基本プラグイン,lnako'),
    ]
    for pname, pdesc, ptype in plugins_rows:
        cur.execute("INSERT INTO plugins (name, desc, nakotype) VALUES (?, ?, ?)", (pname, pdesc, ptype))

    now_ts = 1789700000

    # 1. Generate data/lnako/*.txt and insert into commands
    for orig_plug, genre, name in LNAKO_STD:
        row = meta_by_plug_name.get((orig_plug, name)) or meta_by_name.get(name)
        if not row:
            raise RuntimeError(f"Metadata not found for {orig_plug}/{name}")
        _, _, _, ctype, kana, args, desc, src_url = row
        file_stem = 'TRUE' if name == 'true' else ('FALSE' if name == 'false' else name)
        if name in COMPAT_JS_DOCS:
            desc = f"※要 --compat-js フラグ。{desc}"
            file_body = COMPAT_JS_DOCS[name]
        else:
            file_body = f"#include({orig_plug}/{file_stem})\n"

        pagename = f"lnako/{file_stem}"
        target_file = os.path.join(DATA_DIR, 'lnako', f"{file_stem}.txt")
        with open(target_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(file_body)

        cur.execute("""
            INSERT INTO commands (pagename, plugin, genre, name, type, kana, args, desc, src_url, ctime, mtime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (pagename, 'lnako', genre, name, ctype, kana, args, desc, src_url, now_ts, now_ts))

    # 2. Generate data/lnako_node/*.txt and insert into commands
    for orig_plug, genre, name in LNAKO_NODE:
        row = meta_by_plug_name.get((orig_plug, name)) or meta_by_name.get(name)
        if not row:
            raise RuntimeError(f"Metadata not found for {orig_plug}/{name}")
        _, _, _, ctype, kana, args, desc, src_url = row
        if name in CUSTOM_NODE_DOCS:
            file_body = CUSTOM_NODE_DOCS[name]
        else:
            file_body = f"#include(plugin_node/{name})\n"

        pagename = f"lnako_node/{name}"
        target_file = os.path.join(DATA_DIR, 'lnako_node', f"{name}.txt")
        with open(target_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(file_body)

        cur.execute("""
            INSERT INTO commands (pagename, plugin, genre, name, type, kana, args, desc, src_url, ctime, mtime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (pagename, 'lnako_node', genre, name, ctype, kana, args, desc, src_url, now_ts, now_ts))

    # 3. Generate data/lnako_lowlevel/*.txt and insert into commands
    for spec in LOWLEVEL_SPECS:
        name = spec['name']
        kana = spec['kana']
        genre = spec['genre']
        particles = spec['particles']
        args_db = particles.replace('/', '|')
        returns = spec['returns']
        impl = spec['implemented']
        cap = spec['capability']
        errors = spec['errors']
        desc_text = spec['desc']
        example_text = spec['example']
        refs = spec['refs']

        lines = []
        lines.append('▲説明')
        lines.append('')
        lines.append(desc_text)
        lines.append('')
        lines.append('▲仕様')
        lines.append('')
        lines.append('- 対応環境: [[lnako]] 専用 (Web ブラウザ版 [[wnako]] や Node.js 版 [[cnako]] では動作しません)')
        lines.append('- プラグイン: [[lnako_lowlevel]]')
        lines.append(f'- 分類: {genre}')
        lines.append(f'- 助詞: {particles if particles else "なし（引数なし）"}')
        lines.append(f'- 戻り値: `{returns}`')
        lines.append(f'- 実装状況: {"実装済み" if impl else "未実装（策定中・ENOTSUP）"}')
        if cap:
            lines.append(f'- 機能 ID (capability): `{cap}`')
        if errors:
            lines.append(f'- 発生し得るエラー: {", ".join(errors)}')
        lines.append('')
        lines.append('▲利用例')
        lines.append('')
        lines.append('{{{#nako3')
        lines.append(example_text)
        lines.append('}}}')
        lines.append('')
        if refs:
            lines.append('▲参考')
            lines.append('')
            for ref in refs:
                lines.append(f'- [[{ref}]]')
            lines.append('')

        file_body = '\n'.join(lines)
        target_file = os.path.join(DATA_DIR, 'lnako_lowlevel', f"{name}.txt")
        with open(target_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(file_body)

        short_desc = desc_text.split('\n')[0]
        if not impl and not short_desc.startswith('※'):
            short_desc = '※未実装（策定中）' + short_desc
        pagename = f"lnako_lowlevel/{name}"
        cur.execute("""
            INSERT INTO commands (pagename, plugin, genre, name, type, kana, args, desc, src_url, ctime, mtime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (pagename, 'lnako_lowlevel', genre, name, '関数', kana, args_db, short_desc, 'https://github.com/soramikan/lnako', now_ts, now_ts))

    conn.commit()
    conn.close()

    # 4. Generate overview pages
    lnako_top = """■ [[lnako]] / 機能順 / lnako - PC向け(高速ネイティブ版)

[[lnako]] とは「なでしこ3(高速ネイティブ版)」のことで、Node.js 不要の単一バイナリで動作し、単体のネイティブ実行ファイルのビルド（AOT コンパイル）にも対応した PC・コンソール向けランタイムです。（詳しくは[[ランタイムについて:FAQ/ランタイムについて]]や [[GitHub リポジトリ:https://github.com/soramikan/lnako]] をご覧ください。） [[→カナ順:lnako-カナ順]]

- 基本命令（[[lnako]]）: 392 件（[[plugin_system]]・[[plugin_math]]・[[plugin_csv]]・[[plugin_toml]]・[[plugin_promise]]・[[plugin_httpserver]]・[[plugin_markup]]・[[plugin_caniuse]]・[[plugin_kansuji]] 互換）
- PC・コンソール向け命令（[[lnako_node]]）: 107 件（[[plugin_node]] 互換）
- 低レイヤー API 命令（[[lnako_lowlevel]]）: 63 件（[[lnako]] 独自拡張・全 63 件実装済み）

#nako3doc(list-func,lnako)
"""
    with open(os.path.join(DATA_DIR, 'lnako.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(lnako_top)

    lnako_kana = """■ [[lnako]] / [[カナ順:lnako-カナ順]] / lnako - PC向け(高速ネイティブ版)

[[lnako]] とは「なでしこ3(高速ネイティブ版)」のことで、PC 上でなでしこ3を高速に動かすためのネイティブランタイムです。 [[→機能順:lnako]]

#nako3doc2kana(kana,lnako)
"""
    with open(os.path.join(DATA_DIR, 'lnako-カナ順.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(lnako_kana)

    lnako_node_page = """[[lnako_node]] とは、[[なでしこ3(高速ネイティブ版):lnako]] の PC・コンソール向けプラグイン（[[plugin_node]] 互換）です。ファイル操作、プロセス起動、環境変数、HTTP 通信、内蔵 ZIP 圧縮・解凍、文字コード変換などの機能を提供します。
"""
    with open(os.path.join(DATA_DIR, 'lnako_node.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(lnako_node_page)

    lnako_lowlevel_page = """[[lnako_lowlevel]] とは、[[なでしこ3(高速ネイティブ版):lnako]] 専用の低レイヤー API プラグインです。バイナリストリーム I/O（シーク・位置指定読込・位置指定書込を含む）、Raw 標準入出力、ファイルシステム詳細操作（stat / lstat / symlink / hardlink / realpath）、逐次ハッシュ計算、ディレクトリ逐次走査、POSIX 権限・プロセス管理、ロケール文字列比較・端末表示幅計算などの機能を提供します。
"""
    with open(os.path.join(DATA_DIR, 'lnako_lowlevel.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(lnako_lowlevel_page)

    print(f"Generated lnako ({len(LNAKO_STD)}), lnako_node ({len(LNAKO_NODE)}), lnako_lowlevel ({len(LOWLEVEL_SPECS)}), and {LNAKO_DB_PATH}")

if __name__ == '__main__':
    main()
