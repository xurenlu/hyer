#!/usr/bin/php
<?php
ob_start();
$html=file_get_contents($_SERVER["argv"][1]);
//"./252.html";
//$html = ob_get_clean();

// Specify configuration
$config = array(
           'indent'         => true,
           'output-xhtml'   => true,
           'wrap'           => 200);

// Tidy
$tidy = new tidy;
$tidy->parseString($html, $config, 'utf8');
$tidy->cleanRepair();

// Output
echo $tidy;
?>

