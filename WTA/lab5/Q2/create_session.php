<?php
    session_start();
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Create Session</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <form action="create_session.php" method="POST" style="display:
        <?php
            if(isset($_SESSION['username']) || isset($_POST['username']))
                echo('none');
            else
                echo('block');
        ?>
    ;">
        <input name="username" type="text" placeholder="Username">
        <input type="submit">
    </form>    
    
    <?php
        if(isset($_SESSION['username']))
            echo('Username: '.$_SESSION['username']);
        else if(isset($_POST['username'])){
            $_SESSION['username'] = $_POST['username'];
            echo('Username set!');
        }
    ?>
</body>
</html>