<?php

/** なでしこ3のマニュアル生成スクリプト - 共通関数
 * - nako3doc.inc.php / nako3doc2kana.inc.php から利用される
 * - DBファイル(data/nako3commands.db, data/gonako-commands.db)の判定と読み込み
 */

function nako3doc_getDBFile($env = null)
{
    global $kona3conf;
    // $env が指定されていれば、それを優先する(ページ名からは判定しない)
    if ($env !== null && $env !== '') {
        if ($env === 'gonako') {
            return KONA3_DIR_DATA . '/gonako-commands.db';
        }
        return KONA3_DIR_DATA . '/nako3commands.db';
    }
    $page = isset($kona3conf['page']) ? $kona3conf['page'] : '';
    if (preg_match('#^gonako(?:[/_\-]|$)#', $page)) {
        return KONA3_DIR_DATA . '/gonako-commands.db';
    }
    $dbfile = KONA3_DIR_DATA . '/nako3commands.db';
    return $dbfile;
}

function nako3doc_getDBTime($env = null)
{
    $dbfile = nako3doc_getDBFile($env);
    if (!file_exists($dbfile)) {
        return 0;
    }
    return filemtime($dbfile);
}

function nako3doc_getDB($env = null)
{
    global $nako3doc_db;
    $dbfile = nako3doc_getDBFile($env);
    if (!isset($nako3doc_db) || !is_array($nako3doc_db)) {
        $nako3doc_db = [];
    }
    // DBファイルごとに接続をキャッシュ
    if (!isset($nako3doc_db[$dbfile])) {
        $nako3doc_db[$dbfile] = new PDO("sqlite:$dbfile");
    }
    return $nako3doc_db[$dbfile];
}

function nako3doc_run($sql, $params = [], $env = null)
{
    // DBファイルが無い場合は、空のDBを作らずに空の結果を返す
    if (!file_exists(nako3doc_getDBFile($env))) {
        return [];
    }
    $db = nako3doc_getDB($env);
    try {
        $stmt = $db->prepare($sql);
        $stmt->execute($params);
        $r = $stmt->fetchAll(PDO::FETCH_BOTH);
    } catch (PDOException $e) {
        // テーブルが無いなど、DBが不完全な場合
        return [];
    }
    if (empty($r)) {
        return [];
    }
    return $r;
}
