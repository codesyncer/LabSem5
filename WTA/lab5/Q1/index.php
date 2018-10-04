<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Greetings!</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <?php
        include 'var_count.php';
        date_default_timezone_set('Asia/Calcutta');
        $greets = array("Hi","Hello","Yello","Hola","Namaste");
        echo($greets[mt_rand(0, 4)]." visitor #".$m_count."!<br>The time is ".date("h:i:s a"));
        $var_count = fopen(__DIR__.DIRECTORY_SEPARATOR."var_count.php", "w") or die("Unable to open file!");
        fwrite($var_count, '<?php $m_count = '.($m_count+1).'; ?>');
        fclose($var_count);
    ?>
</body>
</html>