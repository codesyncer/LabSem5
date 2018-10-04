<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Read Cookie</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <?php
        if(isset($_COOKIE['username']))
            echo('Hello '.$_COOKIE['username'].'!');
        else
            echo('No username in cookie');
    ?>
</body>
</html>