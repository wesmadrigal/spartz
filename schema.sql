drop table if exists geodata;

create table geodata ( 
        _id integer,
        fbid long,
        name varchar,
        latitude float,
        longitude float,
        continent varchar,
        country varchar,
        province varchar,
        city varchar
);
