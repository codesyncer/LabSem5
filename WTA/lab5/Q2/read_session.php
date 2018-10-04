<?php
    session_start();
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Read Session</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <?php
        if(isset($_SESSION['username']))
            echo('Hello '.$_SESSION['username'].'!');
        else
            echo('No username in session');
    ?>
</body>
</html>