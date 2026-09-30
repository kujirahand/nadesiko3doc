<?php
/**
 * data/ 以下のページについて、gitの履歴から konawiki3 のメタ情報(data/.meta/*.json)を生成・更新する
 * - PR経由で更新されたページも #recent に表示するためのスクリプト
 * - [使い方] php script/update-meta.php  (リポジトリ内のどこから実行しても良い)
 * - メタ情報が無ければ新規作成し、gitの最終更新日時の方が新しければ updated_at を更新する
 * - 既存の tags / page_id などはそのまま保持する
 */

$root = dirname(__DIR__);
chdir($root);

// 全コミットを新しい順に列挙し、ファイルごとの最新/最古のコミット時刻を得る
$cmd = 'git -c core.quotepath=false log --no-renames --name-only --format=@@%ct -- data 2>&1';
exec($cmd, $lines, $status);
if ($status !== 0) {
    fwrite(STDERR, "git log failed:\n" . implode("\n", $lines) . "\n");
    exit(1);
}
$times = []; // ファイル => [最新, 最古]
$ct = 0;
foreach ($lines as $line) {
    if ($line === '') {
        continue;
    }
    if (strncmp($line, '@@', 2) === 0) {
        $ct = intval(substr($line, 2));
        continue;
    }
    if (!isset($times[$line])) {
        $times[$line] = [$ct, $ct];
    } else {
        $times[$line][1] = $ct; // 新しい順なので、後に出るほど古い
    }
}

$created = 0;
$updated = 0;
foreach ($times as $file => list($latest, $oldest)) {
    // 現存する data/**/*.txt のみ対象(隠しフォルダは除外)
    if (!preg_match('#^data/(.+)\.txt$#u', $file, $m)) {
        continue;
    }
    $page = $m[1];
    if (preg_match('#(^|/)\.#u', $page) || !is_file($file)) {
        continue;
    }
    $metaFile = "data/.meta/$page.json";
    $meta = [];
    if (is_file($metaFile)) {
        $meta = json_decode(file_get_contents($metaFile), true);
        if (!is_array($meta)) {
            $meta = [];
        }
    }
    $isNew = !isset($meta['updated_at']);
    if (!$isNew && intval($meta['updated_at']) >= $latest) {
        continue; // 最新
    }
    if (!isset($meta['tags'])) {
        $meta['tags'] = [];
    }
    $meta['page'] = $page;
    if (!isset($meta['created_at'])) {
        $meta['created_at'] = $oldest;
    }
    $meta['updated_at'] = $latest;
    @mkdir(dirname($metaFile), 0755, true);
    file_put_contents(
        $metaFile,
        json_encode($meta, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT)
    );
    $isNew ? $created++ : $updated++;
}
echo "meta: created=$created updated=$updated\n";
