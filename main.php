<?php $homepage = file_get_contents('http://127.0.0.1:5000/'.$_GET['algo'].'/'.$_GET['keyword']); ?> 
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.0/css/bulma.min.css" /> </head>
    <body>
        <div class="sidenav">
			<p style="text-align:center;font-size:30px;color:white">SpamID<p>
			<br>
			<form action="/main.php">
				<input type="text" name="keyword"><br> 
  				<input type="radio" name="algo" value="k" checked> KMP<br>
  				<input type="radio" name="algo" value="b"> Boyer-Moore<br>
  				<input type="radio" name="algo" value="r"> Regex<br>
				<input type="submit"> 
			</form>
        </div>
		<div class="content">
        <div class="grid js-masonry" data-masonry-options='{ "itemSelector": ".grid-item", "columnWidth": 105 }'>
			<?php
				foreach(json_decode($homepage) as $s){
					echo '<div class="grid-item"><b>@'.$s[1].'</b><br>'.$s[0].'</div>';
				}		
			?>	
		</div>
		</div>
    </body>
    <script src="masonry.pkgd.min.js"></script>

</html>
<style>
    .input-spacer {
        margin-top: 15px;
    }
    .sidenav {
        width: 350px;
        height: 100%;
        background-color: #a5e5ff;
        position: fixed;
		padding: 0 30px;
    }
    .content {
        background-color: #e5efff;
        margin-left: 350px; /* Same as the width of the sidenav */
        padding: 0px 0px 0px 33px;
        height: 100%;
        
    }
    .grid-item {
        border-radius: 10px;
        padding: 10px;
        background-color: white;
        width: 28%;
        min-height: 50px;
        padding: 5px;
        word-wrap: break-word;
        margin: 10px 0 10px 0;
        border: 1px solid black;
    }
	input{
		margin: 0 auto;
	}
	body, html{
		background-color: #e5efff;
	}
</style>
