<!DOCTYPE html>
<html>
<head>
<title>nacre.hopto.org</title>
</head>
<body>

<h1>nacre.hopto.org</h1>
<hr />

<p style="font-size: 18px; font-family: consolas,courier new;">
<?php
include 'data/stats.php';

print "Current: <b>". round($last[1],2) ."</b> (". $last[0] .")<br />\n";
print "Avg 24h: <b>". round($avg[1], 2) ."</b> (". $avg[0]  .")<br />\n";
?>
</p>

<img src="data/kuvaaja.png" /><br /><br />

</body>
</html>
