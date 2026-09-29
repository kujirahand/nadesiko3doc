<?php
// ----------------------------------------------------
// doc-api.php - なでしこの命令情報をJSONで返すAPI
// 使い方は data/doc-api.txt を参照
// ----------------------------------------------------
if (!defined('KONA3_DIR_DATA')) {
    define('KONA3_DIR_DATA', __DIR__ . '/data');
}
require_once KONA3_DIR_DATA . '/.plugins/nako3doc_utils.php';

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

/** JSONを出力して終了 */
function doc_api_output($data, $status = 200)
{
    http_response_code($status);
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT);
    exit;
}

function doc_api_error($message, $status = 400)
{
    doc_api_output(['ok' => false, 'error' => $message], $status);
}

/** runtime から、利用するDBの環境と nakotype の絞り込み条件を得る */
function doc_api_getEnv($runtime)
{
    if ($runtime === 'gonako') {
        return ['gonako', ''];
    }
    // wnako / cnako / phpnako / enako 等は通常のDBを nakotype で絞り込む
    return ['nako3', $runtime];
}

/** 命令1件分の行を、APIの出力形式に変換する */
function doc_api_commandInfo($r)
{
    $args = $r['args'] === null ? '' : $r['args'];
    return [
        'name' => $r['name'],
        'kana' => $r['kana'],
        'plugin' => $r['plugin'],
        'group' => $r['genre'],
        'type' => $r['type'],
        'args' => ($args === '') ? [] : explode('|', $args),
        'desc' => $r['desc'],
        'pagename' => $r['pagename'],
        'src_url' => $r['src_url'],
    ];
}

$runtime = isset($_GET['runtime']) ? trim($_GET['runtime']) : '';
$action = isset($_GET['action']) ? trim($_GET['action']) : '';
$name = isset($_GET['name']) ? trim($_GET['name']) : '';
$validRuntimes = ['', 'wnako', 'cnako', 'phpnako', 'enako', 'gonako'];
if (!in_array($runtime, $validRuntimes, true)) {
    doc_api_error("不明なruntimeです: {$runtime}");
}
list($env, $nakotype) = doc_api_getEnv($runtime);

// プラグイン一覧を取得(runtime で絞り込み)
$plugins = [];
foreach (nako3doc_run('SELECT * FROM plugins ORDER BY rowid', [], $env) as $p) {
    if ($nakotype !== '' && !in_array($nakotype, explode(',', $p['nakotype']), true)) {
        continue;
    }
    $plugins[$p['name']] = $p['nakotype'];
}

// action が省略された場合は name から推測する
if ($action === '') {
    if ($name === '') {
        $action = 'plugins';
    } elseif (isset($plugins[$name])) {
        $action = 'groups';
    } elseif (strpos($name, '/') !== false) {
        $action = 'commands';
    } else {
        $action = 'command';
    }
}

switch ($action) {
    // プラグイン一覧
    case 'plugins':
        $list = [];
        foreach ($plugins as $pname => $type) {
            $list[] = ['name' => $pname, 'runtime' => explode(',', $type)];
        }
        doc_api_output(['ok' => true, 'action' => $action, 'runtime' => $runtime, 'plugins' => $list]);

    // プラグインに属する命令グループの一覧 (name=プラグイン名)
    case 'groups':
        if ($name === '' || !isset($plugins[$name])) {
            doc_api_error("プラグイン『{$name}』が見つかりません。", 404);
        }
        $rows = nako3doc_run(
            'SELECT genre, COUNT(*) AS cnt FROM commands WHERE plugin=? GROUP BY genre ORDER BY MIN(command_id)',
            [$name],
            $env
        );
        $list = [];
        foreach ($rows as $r) {
            $list[] = ['name' => $r['genre'], 'count' => intval($r['cnt'])];
        }
        doc_api_output(['ok' => true, 'action' => $action, 'plugin' => $name, 'groups' => $list]);

    // 命令グループに属する命令の一覧 (name=プラグイン名/グループ名)
    case 'commands':
        $a = explode('/', $name, 2);
        if (count($a) < 2 || $a[1] === '') {
            doc_api_error('name には「プラグイン名/グループ名」を指定してください。');
        }
        if (!isset($plugins[$a[0]])) {
            doc_api_error("プラグイン『{$a[0]}』が見つかりません。", 404);
        }
        $rows = nako3doc_run(
            'SELECT * FROM commands WHERE plugin=? AND genre=? ORDER BY command_id',
            [$a[0], $a[1]],
            $env
        );
        if (!$rows) {
            doc_api_error("グループ『{$name}』が見つかりません。", 404);
        }
        $list = array_map('doc_api_commandInfo', $rows);
        doc_api_output(['ok' => true, 'action' => $action, 'plugin' => $a[0], 'group' => $a[1], 'commands' => $list]);

    // 命令の情報 (name=命令名)。属するグループやプラグインも含まれる
    case 'command':
        if ($name === '') {
            doc_api_error('name に命令名を指定してください。');
        }
        $rows = nako3doc_run(
            'SELECT * FROM commands WHERE name=? OR pagename=? ORDER BY command_id',
            [$name, $name],
            $env
        );
        $list = [];
        foreach ($rows as $r) {
            if (isset($plugins[$r['plugin']])) {
                $list[] = doc_api_commandInfo($r);
            }
        }
        if (!$list) {
            doc_api_error("命令『{$name}』が見つかりません。", 404);
        }
        doc_api_output(['ok' => true, 'action' => $action, 'commands' => $list]);

    default:
        doc_api_error("未知のactionです: {$action}");
}
