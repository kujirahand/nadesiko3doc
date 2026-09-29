<?php

/** なでしこ3のマニュアル生成スクリプト - カナ順/読み順の命令一覧
 * - DBの中の命令をカナ順に並べて一覧表示する
 * - DBアクセスなどの共通関数は nako3doc_utils.php を利用する
 * - 使い方: #nako3doc2kana(kana) / #nako3doc2kana(yomi)
 *   (従来の #nako3doc(list-kana) / #nako3doc(list-yomi) も利用可能)
 */

require_once __DIR__ . '/nako3doc_utils.php';

function kona3plugins_nako3doc2kana_execute($parg)
{
    $mode = array_shift($parg);
    $env = array_shift($parg);
    if ($mode == 'yomi' || $mode == 'list-yomi') {
        return nako3doc_list_kana('yomi', $env);
    }
    return nako3doc_list_kana('kana', $env);
}

function nako3doc_list_kana($mode, $env = null)
{
    $ra = nako3doc_run(
        "SELECT * FROM commands " .
            "ORDER BY kana ASC",
        [],
        $env
    );
    if (!$ra) {
        return "[ERROR]";
    }
    if ($env === 'gonako') {
        $wiki = "* [[命令一覧:gonako]] / [[カナ順:gonako-カナ順]]\n";
    } elseif ($env === 'wnako') {
        $wiki = "* [[命令一覧:wnako]] / [[カナ順:wnako-カナ順]]\n";
    } elseif ($env === 'cnako') {
        $wiki = "* [[命令一覧:cnako]] / [[カナ順:cnako-カナ順]]\n";
    } else {
        $wiki = "* [[命令一覧]] / [[カナ順:命令一覧/カナ順]]\n";
    }
    // ページ内リンクを生成する(五十音順・1行5文字)
    $navFirst = []; // 行の基本文字 => 最初に現れる見出し文字
    foreach ($ra as $r) {
        $ch = mb_substr($r['kana'], 0, 1);
        if ($ch === '') continue;
        $base = nako3doc_kana_base($ch);
        if (!isset($navFirst[$base])) {
            $navFirst[$base] = $ch;
        }
    }
    $rows = [
        ['あ', 'い', 'う', 'え', 'お'],
        ['か', 'き', 'く', 'け', 'こ'],
        ['さ', 'し', 'す', 'せ', 'そ'],
        ['た', 'ち', 'つ', 'て', 'と'],
        ['な', 'に', 'ぬ', 'ね', 'の'],
        ['は', 'ひ', 'ふ', 'へ', 'ほ'],
        ['ま', 'み', 'む', 'め', 'も'],
        ['や', '', 'ゆ', '', 'よ'],
        ['ら', 'り', 'る', 'れ', 'ろ'],
        ['わ', '', '', '', 'を'],
    ];
    // 五十音表にない先頭文字(英数字など)は最後の行にまとめる
    $gridChars = [];
    foreach ($rows as $row) {
        foreach ($row as $c) {
            if ($c !== '') $gridChars[$c] = true;
        }
    }
    $others = [];
    foreach ($navFirst as $base => $ch) {
        if ($base !== 'ん' && !isset($gridChars[$base])) $others[$base] = $ch;
    }
    $btnBase = "display:inline-block;box-sizing:border-box;min-width:3.2em;" .
        "text-align:center;font-family:monospace;font-size:1.2em;padding:6px 10px;" .
        "margin:2px;border-radius:4px;";
    $btnOn = $btnBase . "border:1px solid #aaa;background:#f4f4f4;";
    $btnOff = $btnBase . "border:1px solid #ddd;background:#eee;color:#bbb;";
    $btnBlank = $btnBase . "border:1px solid transparent;visibility:hidden;";
    $makeBtn = function ($label, $target) use ($btnOn, $btnOff) {
        $l = htmlspecialchars($label);
        if ($target === null) {
            return "<span style=\"{$btnOff}\">{$l}</span>";
        }
        $t = htmlspecialchars($target);
        return "<span style=\"{$btnOn}\">" .
            "<a href=\"#kana-{$t}\" style=\"text-decoration:none;\">{$l}</a></span>";
    };
    $nav = "<div class='block'>";
    foreach ($rows as $row) {
        foreach ($row as $c) {
            if ($c === '') {
                $nav .= "<span style=\"{$btnBlank}\">あ</span>";
            } else {
                $nav .= $makeBtn($c, isset($navFirst[$c]) ? $navFirst[$c] : null);
            }
        }
        $nav .= "<br>";
    }
    if ($others) {
        $n = 0;
        foreach ($others as $base => $ch) {
            $nav .= $makeBtn($base, $ch);
            $n++;
            if ($n % 5 == 0) $nav .= "<br>";
        }
        if ($n % 5 != 0) $nav .= "<br>";
    }
    $nav .= "</div>";

    // 同名の命令があればプラグインを明示
    $names = [];
    for ($i = 0; $i < count($ra) - 1; $i++) {
        $j = $i;
        $name1 = $ra[$i]['name'];
        if (!empty($names[$name1])) {
            $j = $names[$name1];
        } else {
            $names[$name1] = $i;
        }
        if ($i == $j) {
            if (isset($ra[$i]['name_show'])) continue;
            $ra[$i]['name_show'] = $ra[$i]['name'];
            $ra[$i]['kana_show'] = $ra[$i]['kana'];
            continue;
        }
        $plugin1 = $ra[$i]['plugin'];
        $plugin2 = $ra[$j]['plugin'];
        $plugin1 = str_replace('plugin_', '', $plugin1);
        $plugin2 = str_replace('plugin_', '', $plugin2);
        $plugin1 = str_replace('nadesiko3-', '', $plugin1);
        $plugin2 = str_replace('nadesiko3-', '', $plugin2);
        $kana1 = $ra[$i]['kana'];
        $ra[$i]['name_show'] = "$name1 ($plugin1)";
        $ra[$j]['name_show'] = "$name1 ($plugin2)";
        $ra[$i]['kana_show'] = "$kana1 ($plugin1)";
        $ra[$j]['kana_show'] = "$kana1 ($plugin2)";
    }

    $chLast = '';
    foreach ($ra as $r) {
        $pagename = $r['pagename'];
        $name = $r['name'];
        $name_show = $r['name_show'];
        $kana_show = $r['kana_show'];
        $kana = $r['kana'];
        $ch = mb_substr($kana, 0, 1);
        if ($ch != $chLast) {
            $chHtml = htmlspecialchars($ch);
            $wiki .= "#html(<span id=\"kana-{$chHtml}\"></span>)\n";
            $wiki .= "** $ch\n";
            $chLast = $ch;
        }
        if ($mode == 'kana') {
            $wiki .= "- [[$name_show:$pagename]]\n";
        } else {
            $wiki .= "- [[$kana_show - $name:$pagename]]\n";
        }
    }
    return $nav . konawiki_parser_convert($wiki);
}

/** 濁音・半濁音・小書き文字・カタカナを、五十音表の基本文字(ひらがな)に変換する */
function nako3doc_kana_base($ch)
{
    // カタカナ → ひらがな
    $ch = mb_convert_kana($ch, 'c', 'UTF-8');
    // 濁点・半濁点を除去
    if (class_exists('Normalizer')) {
        $n = Normalizer::normalize($ch, Normalizer::FORM_D);
        if ($n !== false) {
            $ch = mb_substr(preg_replace('/[\x{3099}\x{309A}]/u', '', $n), 0, 1);
        }
    }
    $ch = mb_convert_kana($ch, 'c', 'UTF-8');
    // 小書き文字
    $small = [
        'ぁ' => 'あ', 'ぃ' => 'い', 'ぅ' => 'う', 'ぇ' => 'え', 'ぉ' => 'お',
        'っ' => 'つ', 'ゃ' => 'や', 'ゅ' => 'ゆ', 'ょ' => 'よ', 'ゎ' => 'わ',
        'ゔ' => 'う', 'ヴ' => 'う',
    ];
    return isset($small[$ch]) ? $small[$ch] : $ch;
}
