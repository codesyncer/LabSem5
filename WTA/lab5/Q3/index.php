<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Bill</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" media="screen" href="main.css" />
</head>
<body>
    <?php
        if(!isset($_POST['first_name']) || !isset($_POST['last_name']) || !isset($_POST['n_tickets']) || !isset($_POST['shirt_size']) || !isset($_POST['email']) || empty($_POST['first_name']) || empty($_POST['last_name']) || empty($_POST['email']) || empty($_POST['n_tickets']) || empty($_POST['shirt_size']))
            echo('Please fill the form');
        else if(!filter_var($_POST['email'], FILTER_VALIDATE_EMAIL))
            echo('Invalid email');
        else{
            echo('<div id="bill_container">');
            echo('<label>Hello '.$_POST['first_name'].' '.$_POST['last_name'].'</label><br>');
            echo('<label>Number of Tickets ordered: '.$_POST['n_tickets'].'</label><br>');
            echo('<label>T-Shirts (Size '.$_POST['shirt_size'].'): '.$_POST['n_tickets'].'</label><br>');
            echo('Your bill amount is Rs. '.($_POST['n_tickets']*1.125*500).'<br>');
            echo('A confirmation email has been sent to '.$_POST['email']);
            echo('</div>');
        }
    ?>
    </div>
</body>
</html> 