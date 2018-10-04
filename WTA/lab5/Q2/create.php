<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Create Cookie</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <form action="create.php" method="POST" style="display:
        <?php
            if(isset($_COOKIE['username']) || isset($_POST['username']))
                echo('none');
            else
                echo('block');
        ?>
    ;">
        <input name="username" type="text" placeholder="Username">
        <input type="submit">
    </form>    
    
    <?php
        if(isset($_COOKIE['username']))
            echo('Username: '.$_COOKIE['username']);
        else if(isset($_POST['username'])){
            setcookie('username', $_POST['username']);
            echo('Cookie set!');
        }
    ?>
</body>
</html>