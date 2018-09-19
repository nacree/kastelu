<!DOCTYPE html>
<html>
<head>
<title>Mökkisivu</title>
<style>
hr {
    border: 1px solid lightblue;
}
body {
    background-color: #F3F4F5;
}
a {
    color: black;
}
</style>
</head>
<body>

<a href="http://mokki.toniliski.fi/"><h1>Mökkisivu</h1></a>

<pre>

<?php
$file = '/home/mokki/data.db';

if (file_exists($file)) {
  $db = new SQLite3($file);

  $results = $db->query("SELECT * from data order by timestamp desc limit 1");
  while ($row = $results->fetchArray()) {
    foreach ($row as $key => $value) {
      if (!is_numeric($key)) {
        $y = '';
        if ($key == 'temperature')    { $y = ' &deg;C'; }
        else if ($key == 'pressure')  { $y = ' hPa'; }
        else if ($key == 'rain_a')    { $y = ' mm'; }
        else if ($key == 'rain_i')    { $y = ' mm'; }
        else if ($key == 'wind_s')    { $y = ' m/s'; }
        else if ($key == 'wind_d')    { $y = ' &deg;'; }
        else if ($key == 'wind_gust') { $y = ' m/s'; }
        else if ($key == 'humidity')  { $y = ' %'; }
        else if ($key == 'hail_a')    { $y = ' mm'; }

        if ($key == 'timestamp') {
          $last = $value;
        } else {
          printf("<b>%-12s</b>: %s%s\n", $key, $value, $y);
        }
      }
    }
  }

  $results = $db->query("SELECT max(temperature),min(temperature),avg(temperature) FROM data WHERE timestamp>datetime('now','-24 hours') and temperature > 0");
  $data = $results->fetchArray();
  printf("\n");
  printf("<b>%-12s</b>: %.1f &deg;C\n", "max (24h)", $data[0]);
  printf("<b>%-12s</b>: %.1f &deg;C\n", "min (24h)", $data[1]);
  printf("<b>%-12s</b>: %.1f &deg;C\n", "avg (24h)", $data[2]);


  printf("\n<b>%-12s</b>: %s\n", "last update", $last);

  $results = $db->query("SELECT * from stats");
  $row = $results->fetchArray();
  printf("<b>%-12s</b>: %s\n", "uptime", $row['valueText']);
}
?>

</pre>

<img src="/data/mokki_temp.png" alt="." />
<img src="/data/mokki_wind.png" alt="." />
<img src="/data/mokki_rain.png" alt="." />
<img src="/data/mokki_humi.png" alt="." />
<img src="/data/mokki_pres.png" alt="." />

</body>
</html>
