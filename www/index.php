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

<img src="data/kuva.jpg" /><br /><br />

<?php
$db = new SQLite3('/home/nacre/kastelu/temp.db');

$results = $db->query('SELECT * from log order by timestamp desc limit 10');
while ($row = $results->fetchArray()) {
    print $row[0] . " " .$row[1] . ": " . $row[2] . "<br />\n";
}
?>

</body>
</html>
