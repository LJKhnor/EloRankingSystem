drop table if exists user;
drop table if exists player;
drop table if exists deck;
drop table if exists league;
drop table if exists team;

drop table if exists match;

create table user (
    id integer primary key autoincrement,
    username text unique not null,
    email text unique not null,
    password text not null
);

create table player (
    id integer primary key autoincrement,
    name text
);

create table deck (
    id integer primary key autoincrement,
    name text
);

create table league (
    id integer primary key autoincrement,
    label text,
    type text,
    start_date timestamp,
    end_ate timestamp
);

create table team (
    id integer primary key autoincrement,
    name text
);

create table match (
    id integer primary key autoincrement,
    league_id integer,
    date timestamp
);