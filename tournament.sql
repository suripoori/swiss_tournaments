-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;
\c tournament
CREATE TABLE player(id serial primary key, name varchar(40) not null);
CREATE TABLE match(id serial primary key,
winner serial references player(id),
loser serial references player(id));
CREATE VIEW wins AS SELECT player.id, player.name, COUNT(winner) AS wins FROM player LEFT JOIN match ON match.winner = player.id GROUP BY player.id;
CREATE VIEW matches AS SELECT player.id, player.name, COUNT(winner) AS matches FROM player LEFT JOIN match ON match.winner = player.id OR match.loser = player.id GROUP BY player.id;
