# sqlite3

create table temps(timestamp datetime primary key default current_timestamp, temperature float);

create table log(timestamp datetime primare key default current_timestamp, type text, message text);
