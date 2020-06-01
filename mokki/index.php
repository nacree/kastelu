<!DOCTYPE html>
<html>
<head>
<title>Mökkisivu</title>

<!-- Styles -->
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

/* data in columns */
.column1 {
  float: left;
  width: 35%;
  border-right: 1px dashed black;

}
.column2 {
  float: left;
  width: 55%;
  padding-left: 15px;
}

.row {
  width: 800px;
  border: 1px solid gray;
  padding: 15px;
  margin-bottom: 15px;
}

.row:after {
  content: "";
  display: table;
  clear: both;
}

#floattemp {
  position: absolute;
  float: left;
  top: 15px;
  left: 650px;
}

/* dynamic graph */
#chartdiv {
  width: 640px;
  height: 480px;
  background-color: white;
  margin-right: 5px;
  margin-bottom: 5px;
}

/* tooltip for copying IP */
.tooltip {
  position: relative;
  display: inline-block;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 140px;
  background-color: #555;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px;
  position: absolute;
  z-index: 1;
  bottom: 150%;
  left: 50%;
  margin-left: -75px;
  opacity: 0;
  transition: opacity 0.3s;
}

.tooltip .tooltiptext::after {
  content: "";
  position: absolute;
  top: 100%;
  left: 50%;
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: #555 transparent transparent transparent;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}

</style>

<!-- Resources -->
<script src="https://www.amcharts.com/lib/4/core.js"></script>
<script src="https://www.amcharts.com/lib/4/charts.js"></script>
<script src="https://www.amcharts.com/lib/4/themes/animated.js"></script>

<!-- script for copying IP -->
<script>
function myFunction() {

    // Create new element
    var el = document.createElement('textarea');
    // Set value (string to be copied)
    el.value = document.getElementById("myIp").innerHTML;
    // Set non-editable to avoid focus and move outside of view
    el.setAttribute('readonly', '');
    el.style = {position: 'absolute', left: '-9999px'};
    document.body.appendChild(el);
    // Select text inside element
    el.select();
    // Copy text to clipboard
    document.execCommand('copy');

    var tooltip = document.getElementById("myTooltip");
    tooltip.innerHTML = "Copied: " + el.value;

    // Remove temporary element
    document.body.removeChild(el);

}

function outFunc() {
  var tooltip = document.getElementById("myTooltip");
  tooltip.innerHTML = "Copy to clipboard";
}
</script>

<!-- Chart code -->
<script>
am4core.ready(function() {

// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end

var chart = am4core.create("chartdiv", am4charts.XYChart);


var data = [
<?php
$file = '/home/mokki/data.db';

$min_date = 0;
$max_date = 0;
$avg = 0;

if (file_exists($file)) {
  $db = new SQLite3($file);

  $i = 0;

  $results = $db->query("SELECT timestamp,temperature FROM data WHERE timestamp>datetime('now','-7 days','localtime') and temperature<>0 order by timestamp asc");
  while ($row = $results->fetchArray()) {
    if ($i > 0) { print ",\n"; }
    print "{date:new Date(\"" . $row['timestamp'] . "\"), value:" . $row['temperature'] . "}";


    if ($min_date == 0) { $min_date = $row['timestamp']; }
                          $max_date = $row['timestamp'];
    $avg += $row['temperature'];

    $i++;
  }

  $avg /= $i;
  $avg = round($avg,2);
}


?>
]

chart.data = data;

// Create axes
var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
dateAxis.renderer.minGridDistance = 60;

var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

// Create series
var series = chart.series.push(new am4charts.LineSeries());
series.dataFields.valueY = "value";
series.dataFields.dateX = "date";
series.tooltipText = "{value} °C"

series.tooltip.pointerOrientation = "vertical";

chart.cursor = new am4charts.XYCursor();
chart.cursor.snapToSeries = series;
chart.cursor.xAxis = dateAxis;

//chart.scrollbarY = new am4core.Scrollbar();
chart.scrollbarX = new am4core.Scrollbar();

dateAxis.showOnInit = false;
// ...
chart.events.on("ready", function () {
  dateAxis.zoomToDates(
    new Date().setDate(new Date().getDate()-1),
    new Date(),
    false,
    true // this makes zoom instant
  );
});

function createTrendLine(data) {
  var trend = chart.series.push(new am4charts.LineSeries());
  trend.dataFields.valueY = "value";
  trend.dataFields.dateX = "date";
  trend.strokeWidth = 1
  trend.stroke = trend.fill = am4core.color("#c00");
  trend.data = data;

  var bullet = trend.bullets.push(new am4charts.CircleBullet());
  bullet.tooltipText = "{date}\n[bold font-size: 17px]average: {valueY}[/] °C";
  bullet.strokeWidth = 1;
  bullet.stroke = am4core.color("#fff")
  bullet.circle.fill = trend.stroke;

  var hoverState = bullet.states.create("hover");
  hoverState.properties.scale = 1.7;

  return trend;
};

createTrendLine([
  { "date": new Date("<?=$min_date?>"), "value": <?=$avg?> },
  { "date": new Date("<?=$max_date?>"), "value": <?=$avg?> }
]);

}); // end am4core.ready()
</script>

</head>
<body>

<a href="http://mokki.toniliski.fi/"><h1>Mökkisivu</h1></a>

<div class="row">
<div class="column1">
<pre>

<?php

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
        } else if ($key == 'temperature') {
          printf("<span style=\"background-color: lightblue\"><b>%-12s</b>: %s%s</span>\n", $key, $value, $y);
          $temperature = $value;
        } else {
          printf("<b>%-12s</b>: %s%s\n", $key, $value, $y);
        }
      }
    }
  }

  printf("\n<b>Temperature (min-avg-max, &deg;C):</b>\n");
  $results = $db->query("SELECT max(temperature),min(temperature),avg(temperature) FROM data WHERE timestamp>datetime('now','-24 hours','localtime') and temperature <> 0");
  $data = $results->fetchArray();
  printf("<b>%-12s</b>: %4.1f - %4.1f - %4.1f\n", "24h", $data[1], $data[2], $data[0]);

  $results = $db->query("SELECT max(temperature),min(temperature),avg(temperature) FROM data WHERE timestamp>datetime('now','-7 days','localtime') and temperature <> 0");
  $data = $results->fetchArray();
  printf("<b>%-12s</b>: %4.1f - %4.1f - %4.1f\n", "7d", $data[1], $data[2], $data[0]);

  $results = $db->query("SELECT max(temperature),min(temperature),avg(temperature) FROM data WHERE timestamp>datetime('now','-30 days','localtime') and temperature <> 0");
  $data = $results->fetchArray();
  printf("<b>%-12s</b>: %4.1f - %4.1f - %4.1f\n", "30d", $data[1], $data[2], $data[0]);

?>

</pre>
</div>
<div class="column2">
<pre>

<?php

  printf("<b>%-12s</b>: %s\n", "last update", $last);

  $results = $db->query("SELECT * from stats");
  $row = $results->fetchArray();
  printf("<b>%-12s</b>: %s\n", "uptime", $row['valueText']);


  $file = '/var/www/api.toniliski.fi/input/data.db';

  if (file_exists($file)) {
    $db = new SQLite3($file);

    $last = '';

    $results = $db->query("SELECT value,DATETIME(timestamp,'+2 hours','localtime') from data where uid=2 order by timestamp desc limit 1");
    if ($row = $results->fetchArray()) {
        $lastmod = "";
        $filename = "data/cam.jpg";
        if (file_exists($filename)) {
            $lastmod = date("Y-m-d H:i:s", filemtime($filename));
        }
        printf("\n<b>%-13s</b>: %3.1f%s <br />\n<a href=\"/%s\">Kuva</a>                (%s)\n", "Saunamökki", $row[0], "&deg;C", $filename, $lastmod);
    }
  }

  printf("IP: <span id=\"myIp\">%-15s</span> (" . date("Y-m-d H:i:s", filemtime("/home/mokki/ip.txt")) . ")", trim(file_get_contents("/home/mokki/ip.txt")));

}
?>

</pre>

<div class="tooltip">
<button onclick="myFunction()" onmouseout="outFunc()">
  <span class="tooltiptext" id="myTooltip">Copy IP to clipboard</span>
  Copy IP
</button>
</div>


</div>
</div>

<div id="chartdiv"></div>

<div id="floattemp">
  <span style="background-color: lightblue; font-size: 3em;"><?php printf("%+.01f", $temperature);?> °C</span>
</div>

<img src="/data/mokki_temp.png" alt="." />
<img src="/data/mokki_wind.png" alt="." />
<img src="/data/mokki_rain.png" alt="." />
<img src="/data/mokki_humi.png" alt="." />
<img src="/data/mokki_pres.png" alt="." />

</body>
</html>
