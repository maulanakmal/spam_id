<?php

$consumerKey = 'e3Qzanw0bnvTbunxOLr6GM2vi';
$consumerSecret = 'IrBFKeNwfup4SRJDRtxwKsHJMRg5sppk6GD85GnWEKQ6b2Vfnk';
$accessToken = '1974502530-UIWm0t1pIzQMbmYgacEbrAf3TYKe1iMKn8op5hJ';
$accessTokenSecret = 'KSCFR1kdXeESS4GrOfC37obNplr2wLRbmmhcBBgP69rnu';

require "twitteroauth/autoload.php";
use Abraham\TwitterOAuth\TwitterOAuth;

$conn = new TwitterOAuth($consumerKey, $consumerSecret, $accessToken, $accessTokenSecret);

$statuses = $conn->get("statuses/home_timeline", ["count" => 25, "exclude_replies" => true]);

foreach ($statuses as $status) {
	print_r($status->text);
	echo "<br><br>";
}

?>
