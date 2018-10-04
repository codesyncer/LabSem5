<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Delete Cookie</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <?php
        if(isset($_COOKIE['username'])){
            setcookie('username', '', time() - 3600);
            echo('Deleted Cookie!');
        }
        else
            echo('Cookie not found!');
    ?>
</body>
</html>