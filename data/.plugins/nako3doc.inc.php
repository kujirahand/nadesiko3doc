<?php

/** なでしこ3のマニュアル生成スクリプト
 * - [備考] data/nako3commands.db に nadesiko3doc リポジトリのDBを配置
 */

require_once __DIR__ . '/nako3doc_utils.php';

/** ページの編集履歴(GitHub)へのリンク書式 - {WikiName} がページ名に置換される */
if (!defined('NAKO3DOC_HISTORY_URL')) {
    define('NAKO3DOC_HISTORY_URL', 'https://github.com/kujirahand/nadesiko3doc/commits/master/data/{WikiName}.txt');
}
/** 履歴リンクのラベル */
if (!defined('NAKO3DOC_HISTORY_LABEL')) {
    define('NAKO3DOC_HISTORY_LABEL', '📝履歴');
}

function kona3plugins_nako3doc_execute($parg)
{
    global $kona3conf;
    $page = $kona3conf['page'];
    // check args
    $pa = array_shift($parg);

    if ($pa == 'list-func') {
        $type = array_shift($parg);
        return nako3doc_list_func($type);
    }
    // カナ順/読み順の一覧は nako3doc2kana.inc.php に分離(互換のため委譲)
    if ($pa == 'list-kana' || $pa == 'list-yomi') {
        require_once __DIR__ . '/nako3doc2kana.inc.php';
        $env = array_shift($parg);
        return nako3doc_list_kana($pa == 'list-kana' ? 'kana' : 'yomi', $env);
    }
    if ($pa == 'list-plugins' || $pa == 'plugins') {
        return nako3doc_list_plugins();
    }
    // gonako ページは何も出力しない
    if ($page == 'gonako') {
        return '';
    }
    // check page
    $ra = nako3doc_run(
        'SELECT * FROM commands WHERE pagename=?',
        [$page]
    );
    if (!$ra) {
        return nako3doc_checkGenre($page);
    }
    $r = $ra[0];
    // --- page ---
    $plugin = $r['plugin'];
    $genre = $r['genre'];
    $type = $r['type'];
    $name = $r['name'];
    $args = $r['args'];
    $desc = $r['desc'];
    $kana = $r['kana'];
    $src_url = $r['src_url'];
    $ctime = $r['ctime'];
    $mtime = $r['mtime'];
    $nakotype = nako3doc_getNakoTypeWiki($plugin);
    // 拡張かどうか
    $extra_plugin = "";
    if (strpos($page, 'gonako/') === 0) {
        $extra_plugin = "[[なでしこ3(Go版):gonako]]でのみ実行できる命令です。\n";
    } elseif (strpos($nakotype, '拡張プラグイン') !== FALSE) {
        $pluginUrl = $plugin;
        if (strpos($nakotype, '[[wnako]]') !== FALSE) {
            $pluginUrl = "https://cdn.jsdelivr.net/npm/{$plugin}@latest/{$plugin}.js";
        }
        $extra_plugin = "{{{\n" .
            "# [拡張プラグイン] 以下の宣言が必要:\n" .
            "!『{$pluginUrl}』を取り込む\n" .
            "}}}\n";
    }
    $nakotype = str_replace('基本プラグイン,', '', $nakotype);
    $nakotype = str_replace('拡張プラグイン,', '', $nakotype);
    // search in nako3storage
    $nameenc = urlencode($name);
    // $search_url = "https://nadesi.com/v3/storage/index.php?search_word={$nameenc}&action=search&target=program";
    // $search_name = "[[→『{$name}』を貯蔵庫で検索:$search_url]]";
    $search_url = "https://www.google.com/search?q=site%3A%2F%2Fnadesi.com%2Fv3%2Fdoc+{$nameenc}";
    $search_name = "[[🔍マニュアル:{$search_url}]]";
    $search_url = "https://github.com/search?q=repo%3Akujirahand%2Fnadesiko3hub+{$nameenc}";
    $search_name_n3s = "[[🔍貯蔵庫ハブ:{$search_url}]]";
    $search_url = "https://www.google.com/search?q=site%3A%2F%2Fn3s.nadesi.com+{$nameenc}";
    $search_name_n3s .= " / [[🔍貯蔵庫:{$search_url}]]";
    $src_link = "[[👓ソース:{$src_url}]]";
    $history_link = nako3doc_getHistoryLink($page);
    $wiki = <<<EOS
* {$name} ($kana)

{{{#csv(flag=||)
カテゴリ || [[$plugin]] > [[$genre:$plugin/$genre]]
環境 || $nakotype
種類 || $type
引数 || $args
説明 || $desc
}}}
{$extra_plugin}
EOS;
    if ($type == '定数') {
        $wiki = <<<EOS
* {$name} ($kana)

{{{#csv(flag=||)
カテゴリ || [[$plugin]] > [[$genre:$plugin/$genre]]
種類   || $type
初期値 || $desc
}}}
EOS;
    }
    $wiki = $wiki . "\n{$search_name_n3s} / {$search_name} / {$src_link}";
    if ($history_link != '') {
        $wiki .= " / {$history_link}";
    }
    $wiki .= "\n";
    $s = konawiki_parser_convert($wiki);

    return $s;
}

/** ページのGitHub履歴へのリンク(Wiki書式)を返す */
function nako3doc_getHistoryLink($page)
{
    $url = nako3doc_getHistoryURL($page);
    if ($url == '') {
        return '';
    }
    $label = NAKO3DOC_HISTORY_LABEL;
    return "[[{$label}:{$url}]]";
}

/** ページのGitHub履歴のURLを返す */
function nako3doc_getHistoryURL($page)
{
    if ($page == '' || NAKO3DOC_HISTORY_URL == '') {
        return '';
    }
    // パス区切りの「/」は残したままURLエンコードする
    $parts = explode('/', $page);
    foreach ($parts as $i => $part) {
        $parts[$i] = rawurlencode($part);
    }
    $pageenc = implode('/', $parts);
    return str_replace('{WikiName}', $pageenc, NAKO3DOC_HISTORY_URL);
}

function nako3doc_checkGenre($page)
{
    $a = explode('/', $page, 2);
    $plug = $a[0];
    $genre = $a[1];
    $ra = nako3doc_run(
        "SELECT * FROM commands " .
            "WHERE plugin=? AND genre=?",
        [$plug, $genre]
    );
    if (!$ra) {
        return nako3doc_checkPlugin($page);
    }
    $wiki = "* 🔌 [[$plug]] / [[$genre:$page]]\n";
    $wiki .=
        "#html(<blockquote style='background-color:#fff0f0;'>);\n" .
        "#page($plug)\n" .
        "#html(</blockquote>);\n" .
        "** 🌴 [[$genre:$page]]\n";
    foreach ($ra as $r) {
        $plugin = $r['plugin'];
        $genre = $r['genre'];
        $pagename = $r['pagename'];
        $type = $r['type'];
        $name = $r['name'];
        $args = $r['args'];
        $desc = $r['desc'];
        $kana = $r['kana'];
        $ctime = $r['ctime'];
        $mtime = $r['mtime'];
        if ($type == '定数') {
            $wiki .= "- [[$name:$pagename]]\n";
            $wiki .= "-- 定数\n";
        } else {
            $arg_desc = "";
            if ($args) {
                $arg_desc = "($args)";
            }
            $wiki .= "- [[$name:$pagename]] $arg_desc\n";
            $wiki .= "-- $desc\n";
        }
    }
    return konawiki_parser_convert($wiki);
}

function nako3doc_getNakoTypeWiki($plugin)
{
    $nakotype = nako3doc_getNakoType($plugin);
    if (!$nakotype) return '';
    return preg_replace('#([a-z]+)#', '[[\1]]', $nakotype);
}

function nako3doc_getNakoType($plugin)
{
    $q = nako3doc_run(
        "SELECT * FROM plugins WHERE name=?",
        [$plugin]
    );
    if (!$q) {
        return null;
    }
    return $q[0]['nakotype'];
}

function nako3doc_getPluginInfo($plugin)
{
    $p = [
        "wnako" => FALSE,
        "cnako" => FALSE,
        "phpnako" => FALSE,
        "gonako" => FALSE,
        "基本プラグイン" => FALSE,
        "拡張プラグイン" => FALSE,
        "nakotype" => "",
    ];
    $nakotype = nako3doc_getNakoType($plugin);
    if (!$nakotype) return $p;
    $qqq = explode(',', $nakotype);
    foreach ($qqq as $k) {
        $p[$k] = TRUE;
    }
    $p['nakotype'] = $nakotype;
    return $p;
}

function nako3doc_getPlugins($pagetype = '', $env = null)
{
    if ($pagetype) {
        $pluginQ = nako3doc_run(
            "SELECT * FROM plugins WHERE nakotype LIKE ?",
            ["%$pagetype%"],
            $env
        );
    } else {
        // all
        $pluginQ = nako3doc_run("SELECT * FROM plugins", [], $env);
    }
    $pluginInfo = [];
    foreach ($pluginQ as $q) {
        $pluginInfo[$q['name']] = $q['nakotype'];
    }
    return $pluginInfo;
}


function nako3doc_list_func($pagetype)
{
    if (!$pagetype) {
        $pagetype = '';
    }

    $cache_dir = KONA3_DIR_CACHE;
    $cache_file = $cache_dir . "/nako3doc.cache.list_func_{$pagetype}.html";

    // cache=0 が指定された場合は既存のキャッシュファイルを削除
    if (isset($_GET['cache']) && intval($_GET['cache']) === 0) {
        if (file_exists($cache_file)) {
            @unlink($cache_file);
        }
    }

    // check page cache
    $conf_use_cache = isset($_GET['cache']) ? (intval($_GET['cache']) == 1) : TRUE;
    if ($conf_use_cache) {
        $use_cache = FALSE;
        if (file_exists($cache_file)) {
            $cache_time = filemtime($cache_file);
            $db_time = nako3doc_getDBTime();
            if ($db_time < $cache_time) {
                $use_cache = TRUE;
            }
        }
        // use cache
        if ($use_cache) {
            $html = file_get_contents($cache_file);
            if (kona3isLogin()) {
                $page_nocache = kona3getPageURL('', '', '', 'cache=0');
                $html = "<div class='block'>[CACHE mode : <a href='$page_nocache'>nocache</a>]</div>" . $html;
            }
            return $html;
        }
    }

    // 該当するプラグインを取得
    $pluginInfo = nako3doc_getPlugins($pagetype);
    // 拡張プラグインかどうかを調べる
    $pluginIsBasic = [];
    foreach ($pluginInfo as $pname => $v) {
        $a = explode(",", $v);
        $is_basic = array_shift($a);
        // 基本プラグインかどうか
        $pluginIsBasic[$pname] = ($is_basic === '基本プラグイン');
    }

    // コマンド一覧を得る
    $ra = nako3doc_run(
        "SELECT * FROM commands " .
            "ORDER BY plugin ASC",
        []
    );
    if (!$ra) {
        return "[ERROR]";
    }
    $command_count = count($ra);
    $count_str = "▲命令数\n\n命令数: {$command_count}個です。";

    $plugins = [];
    $pluginLast = '';
    $genreLast = '';
    $cmd = [];
    foreach ($ra as $r) {
        $plugin = $r['plugin'];
        if (!isset($pluginInfo[$plugin])) continue;
        $genre = $r['genre'];
        $pagename = $r['pagename'];
        $type = $r['type'];
        $name = $r['name'];
        $args = $r['args'];
        $desc = $r['desc'];
        $kana = $r['kana'];
        $ctime = $r['ctime'];
        $mtime = $r['mtime'];

        // plugin
        if (!isset($cmd[$plugin])) {
            $cmd[$plugin]  = [];
        }
        // genre
        if (!isset($cmd[$plugin][$genre])) {
            $cmd[$plugin][$genre] = [];
        }
        // command
        $cmd[$plugin][$genre][] = "[[$name:$pagename]]";
    }
    // プラグイン順に出力
    $fn = function ($cmd, $plugin) use ($pluginInfo) {
        // このプラグインの命令がない場合は出力しない
        if (empty($cmd[$plugin])) {
            return ['', ''];
        }
        $type = $pluginInfo[$plugin];
        $type = preg_replace('#([a-z]+)#', '[[$1]]', $type);
        $type = str_replace(',', ', ', $type);
        $w = "** 🔌 [[$plugin]]\n[[$plugin]]は{$type}で使えます。\n";
        $ps = preg_replace('#^(plugin_|nadesiko3-)#', '', $plugin);
        $alias = [
            'system' => 'システム',
            'browser' => 'ブラウザ',
            'datetime' => '日時',
            'math' => '数学関数',
            'kansuji' => '漢数字'
        ];
        if (isset($alias[$ps])) {
            $ps = $alias[$ps];
        }
        $t = "| 🔌 [[$ps:$plugin]] | ";
        $groupList = [];
        $i = 0;
        $marks = ['🌿', '🌱', '🍃', '🍃', '🌲'];
        foreach ($cmd[$plugin] as $genre => $list) {
            $mark = $marks[$i % count($marks)];
            $i++;
            $w .= "*** [[🌲 {$ps}:$plugin]] > [[{$genre}:$plugin/$genre]]:\n";
            $w .= '{{{#column' . "\n";
            $w .= implode(' 🌲 ', $list) . "\n";
            $w .= '}}}' . "\n\n";
            $w .= "\n\n";
            $groupList[] = "[[$genre:$plugin/$genre]]";
        }
        $t .= implode(' 🌲 ', $groupList) . "\n";
        return [$w, $t];
    };
    // 出力
    $index = '';
    $wiki = '';
    list($w, $t) = $fn($cmd, 'plugin_system');
    $wiki .= $w;
    $index .= $t;
    list($w, $t) = $fn($cmd, 'plugin_math');
    $wiki .= $w;
    $index .= $t;
    list($w, $t) = $fn($cmd, 'plugin_csv');
    $wiki .= $w;
    $index .= $t;
    if (!$pagetype || $pagetype == 'wnako') {
        list($w, $t) = $fn($cmd, 'plugin_browser');
        $wiki .= $w;
        $index .= $t;
        list($w, $t) = $fn($cmd, 'plugin_turtle');
        $wiki .= $w;
        $index .= $t;
    }
    if (!$pagetype || $pagetype == 'cnako') {
        list($w, $t) = $fn($cmd, 'plugin_node');
        $wiki .= $w;
        $index .= $t;
    }
    foreach ([TRUE, FALSE] as $isBasic) {
        foreach ($cmd as $plug => $v) {
            // 既に追加済みならスキップ
            if (
                $plug == 'plugin_system' ||
                $plug == 'plugin_math' ||
                $plug == 'plugin_csv' ||
                $plug == 'plugin_browser' ||
                $plug == 'plugin_turtle' ||
                $plug == 'plugin_node'
            ) {
                continue;
            }
            if ($pluginIsBasic[$plug] == $isBasic) {
                list($w, $t) = $fn($cmd, $plug);
                $wiki .= $w;
                $index .= $t;
            }
        }
    }
    $wiki =
        $index . "\n\n" .
        $wiki . "\n\n" .
        $count_str .
        "";

    $wiki_html = konawiki_parser_convert($wiki);
    // save cache
    if ($conf_use_cache && $cache_dir != '') {
        @file_put_contents($cache_file, $wiki_html);
    }
    return $wiki_html;
}

function nako3doc_list_plugins()
{
    // 全てのDB(通常版・Go版)からプラグインの一覧を取得
    $plugins = [];
    foreach (['nako3', 'gonako'] as $env) {
        foreach (nako3doc_getPlugins('', $env) as $name => $nakotype) {
            if (!isset($plugins[$name])) {
                $plugins[$name] = $nakotype;
            }
        }
    }
    $wiki = "* [[命令一覧]] > プラグイン一覧\n";
    foreach ($plugins as $plugin => $r) {
        $type = preg_replace('/([a-z]+)/', '[[\1]]', $r);
        $wiki .= "*** 🔌[[$plugin]]\n";
        $wiki .= "#html(<blockquote>)";
        $wiki .= "#include($plugin)\n";
        $wiki .= "($type)\n";
        $wiki .= "#html(</blockquote>)\n";
        $wiki .= "\n";
    }
    return konawiki_parser_convert($wiki);
}

function nako3doc_checkPlugin($page)
{
    $ra = nako3doc_run(
        "SELECT * FROM commands " .
            "WHERE plugin=? " .
            "ORDER BY genre ASC,command_id ASC",
        [$page]
    );
    if (!$ra) {
        return "";
    }
    $wiki = "* [[プラグイン一覧]] > 🔌 [[$page]]\n";
    $nakotype = nako3doc_getNakoTypeWiki($page);
    $wiki .= "#html(<blockquote>)\n";
    $wiki .= "#include($page)\n";
    $wiki .= "({$nakotype}で利用できます)\n";
    $wiki .= "#html(</blockquote>)\n";
    $genreLast = "";
    foreach ($ra as $r) {
        $plugin = $r['plugin'];
        $genre = $r['genre'];
        $pagename = $r['pagename'];
        $type = $r['type'];
        $name = $r['name'];
        $name_show = $r['name_show'];
        $args = $r['args'];
        $desc = $r['desc'];
        $kana = $r['kana'];
        if ($genreLast != $genre) {
            $genreLast = $genre;
            $wiki .= "*** 🌴 [[$genre:$plugin/$genre]]\n";
        }
        if ($type == '定数') {
            $wiki .= "- [[$name:$pagename]] \n";
        } else {
            if ($args) {
                $args = "($args)";
            }
            $wiki .= "- [[$name:$pagename]] $args\n";
        }
    }
    return konawiki_parser_convert($wiki);
}

// action
function kona3plugins_nako3doc_action()
{
    $q = isset($_GET['q']) ? $_GET['q'] : '';
    $qhtml = htmlspecialchars($q);
    $rows = nako3doc_run(
        'SELECT * FROM commands WHERE name=? OR pagename=?',
        [$q, $q]
    );
    $html = "<div style='color:gray;'>命令『{$qhtml}』の検索結果:</div>" .
        "<div><ul>";
    if (!$rows) {
        $html .= '<li>見つかりません</li>';
    } else {
        foreach ($rows as $r) {
            $pagename = $r['pagename'];
            $desc = htmlspecialchars($r['desc']);
            $args = htmlspecialchars($r['args']);
            $url = kona3getPageURL($pagename);
            $name = htmlspecialchars($pagename);
            $html .= "<li><a href='$url'>$name</a> ($args)" .
                "<br>$desc</li>";
        }
    }
    $html .= '</ul></div>';
    kona3showMessage('#nako3doc - 命令検索', $html, 'white.html');
}
