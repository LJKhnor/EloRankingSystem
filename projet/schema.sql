drop table if exists user;
drop table if exists player;
drop table if exists deck;
drop table if exists league;
drop table if exists team;

drop table if exists deck_league;
drop table if exists team_player;
drop table if exists team_league;
drop table if exists team_match;

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
    name text,
    player_id integer,
    foreign key (player_id) references player(id)
);

create table league (
    id integer primary key autoincrement,
    label text unique,
    type text,
    start_date timestamp,
    end_date timestamp
);

create table player_deck_league (
    player_1_id integer,
    player_2_id integer,
    deck_1_id integer,
    deck_2_id integer,
    league_id integer,
    date timestamp,
    winner_player_id integer,
    primary key (player_1_id, player_2_id, deck_1_id, deck_2_id, league_id, date, winner_player_id),
    foreign key (player_1_id) references player(id),
    foreign key (player_2_id) references player(id),
    foreign key (deck_1_id) references deck(id),
    foreign key (deck_2_id) references deck(id),
    foreign key (league_id) references league(id)
);

create table team (
    id integer primary key autoincrement,
    name text
);

create table match (
    id integer primary key autoincrement,
    league_id integer,
    date timestamp,
    foreign key (league_id) references league(id)
);

create table deck_league (
    deck_id integer,
    league_id integer,
    elo number,
    primary key (deck_id, league_id),
    foreign key (deck_id) references deck(id),
    foreign key (league_id) references league(id)
);

create table team_player (
    team_id integer,
    player_id integer,
    primary key (player_id, team_id),
    foreign key (player_id) references player(id),
    foreign key (team_id) references team_id
);

create table team_league (
    team_id integer,
    league_id integer,
    elo number,
    primary key (league_id, team_id),
    foreign key (league_id) references league(id),
    foreign key (team_id) references team(id)
);

create table team_match (
    team_id integer,
    match_id integer,
    elo_before integer,
    prevision integer,
    result text,
    primary key (team_id, match_id),
    foreign key (team_id) references team(id),
    foreign key (match_id) references match(id)
);