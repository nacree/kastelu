<h1>Mökki-dataa</h1>

<pre>

<?php
$file = '/home/mokki/data.db';

if (file_exists($file)) {
  $db = new SQLite3($file);

  $results = $db->query("SELECT * from data order by timestamp desc limit 1");
  while ($row = $results->fetchArray()) {
  //    print $row[0] . " " .$row[1] . ": " . $row[2] . "<br />\n";
//    print_r($row);
    foreach ($row as $key => $value) {
      if (!is_numeric($key)) {
        printf("<b>%-12s</b>: %s\n", $key, $value);
      }
    }
  }
}
?>

</pre>

<img src="/data/mokki_temp.png" alt="." />
<img src="/data/mokki_wind.png" alt="." />
<img src="/data/mokki_rain.png" alt="." />
<img src="/data/mokki_humi.png" alt="." />
<img src="/data/mokki_pres.png" alt="." />
