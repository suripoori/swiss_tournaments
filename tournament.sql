-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;
\c tournament
CREATE TABLE player(id serial primary key, name varchar(40) not null, score integer, matches integer);
CREATE TABLE match(id serial primary key,
winner serial references player(id),
loser serial references player(id));

