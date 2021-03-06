#sqlite3

create table data(
  timestamp datetime primary key default current_timestamp,
  temperature   float,
  humidity      float,
  pressure      float,
  wind_s        float,
  wind_d        integer,
  rain_i        float,
  rain_a        float,
  rain_d        float,
  hail_a        float,
  wind_gust     float
);

create table log(timestamp datetime primare key default current_timestamp, type text, message text);

create table stats(
  param        text primare key,
  valueText    text,
  valueInt     integer,
  timestamp    lastUpdate
);

