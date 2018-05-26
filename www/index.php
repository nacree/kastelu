<!DOCTYPE html>
<html>
<head>
<title>nacre.hopto.org</title>
<style>
hr {
    border: 1px solid lightblue;
}
</style>
</head>
<body>

<h1>nacre.hopto.org</h1>
<hr />

<p style="font-size: 16px; font-family: consolas,courier new;">
<?php
include 'data/stats.php';

print "Current: <b>". round($last[1],2) ." &deg;C</b><br /><br />\n";
print "Avg 24h: <b>". round($avg[1], 2) ." &deg;C</b><br />\n";
print "Min 24h: <b>". round($min[1], 2) ." &deg;C</b><br />\n";
print "Max 24h: <b>". round($max[1], 2) ." &deg;C</b><br />\n";
?>
</p>
<hr />

<img src="data/kuvaaja.png" />&nbsp;

<img src="data/kuva.jpg" /><br />
<p style="font-size: 12px;">
Last measurement: <?= $last[0] ?>, graph generated: <?= $avg[0] ?><br /><br />

<?php
$db = new SQLite3('/home/nacre/kastelu/temp.db');

$results = $db->query("SELECT * from log where timestamp>datetime('now','-21 hours') order by timestamp asc limit 5");
while ($row = $results->fetchArray()) {
    print $row[0] . " " .$row[1] . ": " . $row[2] . "<br />\n";
}
?>

</p>

</body>
</html>
