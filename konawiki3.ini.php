<?php
// ----------------------------------------------------
// konawiki3.ini.php
// ----------------------------------------------------
$file_doc_ini = dirname(__FILE__).'/nadesiko3doc.ini.php';

define("KONA3_WIKI_TITLE", "なでしこ3マニュアル");
define("KONA3_WIKI_PRIVATE", FALSE); # TRUE or FALSE
define("KONA3_WIKI_SKIN", "def"); // def/single
define("KONA3_WIKI_USERS", "nako3:nako3"); # admin users

// Setting
define("KONA3_ALLPAGE_FOOTER", "#comment\n#analytics"); // footer
define("KONA3_ENC_PAGENAME", FALSE);

// 本番と異なる設定
if (file_exists($file_doc_ini)) {
  include_once($file_doc_ini);
} else {
  define("KONA3_SHOW_DATA_DIR", TRUE); // show local path 
  define("KONA3_DIR_ENGINE", 
  dirname(dirname(__FILE__)).'/konawiki3/kona3engine');
  define("KONA3_DIR_DATA", dirname(__FILE__).'/data');
  define("KONA3_DIR_PRIVATE", dirname(__FILE__).'/private');
  define("KONA3_DSN", "sqlite:".KONA3_DIR_PRIVATE."/data.sqlite");
  define("KONA3_GIT_ENABLED", TRUE);
}


