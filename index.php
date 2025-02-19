<?php
// ----------------------------------------------------
// konawiki3 - index.php
// ----------------------------------------------------
define('KONA3_DIR_INDEX', __DIR__);

// Read Directories info
$file_kona3dir_def = __DIR__ . '/kona3dir.def.php';
if (file_exists($file_kona3dir_def)) {
    require_once $file_kona3dir_def;
} else {
    // Search engine path
    $root = __DIR__;
    $engine = "{$root}/kona3engine/index.inc.php";
    if (!file_exists($engine)) {
        $root = dirname(__DIR__) . '/konawiki3';
        $engine = "{$root}/kona3engine/index.inc.php";
        if (!file_exists($engine)) {
            error_kona3dir_def();
            exit;
        }
    }
    // generate kona3dir.def.php
    $here = __DIR__;
    $def = <<< __EOS__
<?php
// --- konawiki3 directories setting ---
// generated by konawiki3-auto-install
define('KONA3_DIR_ENGINE',  '{$root}/kona3engine');
define('KONA3_DIR_SKIN',    '{$root}/skin');
define('KONA3_DIR_DATA',    '{$here}/data');
define('KONA3_DIR_PRIVATE', '{$here}/private');
define('KONA3_DIR_CACHE',   '{$here}/cache');
__EOS__;
    file_put_contents($file_kona3dir_def, $def . "\n");
    // mkdir
    foreach (['data', 'private', 'cache'] as $d) {
        $dir = "{$here}/{$d}";
        if (!file_exists($dir)) {
            mkdir($dir, 0777, TRUE);
        }
    }
    require_once $file_kona3dir_def;
}

function error_kona3dir_def()
{
    // show error
    $url = "https://kujirahand.com/konawiki3/index.php?install%2Fkona3dir.def.php";
    $err = "<div>";
    $err .= "<h3>Please set up `kona3dir.def.php`.</h3>";
    $err .= "<a href='$url'></a>";
    echo '<p>Please check KONA3_DIR_ENGINE</a></p>' . "\n";
}

// Execute kona3engine/index.inc.php
$engine_index = KONA3_DIR_ENGINE . '/index.inc.php';
if (!file_exists($engine_index)) {
    error_kona3dir_def();
    exit;
}
include_once $engine_index;
