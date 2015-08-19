-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

\c tournament;

CREATE TABLE PLAYERS (
  id   SERIAL PRIMARY KEY,
  name VARCHAR(255)
);

CREATE TABLE MATCHES (
  id      SERIAL PRIMARY KEY,
  winner INTEGER REFERENCES PLAYERS (id),
  loser  INTEGER REFERENCES PLAYERS (id)
);

CREATE OR REPLACE VIEW STANDINGS AS
  SELECT
    p.id as id,
    p.name as name,
    (SELECT count(id) FROM matches WHERE winner = p.id)
      AS wins,
    ((SELECT count(id) FROM matches WHERE winner = p.id) + (SELECT count(id) FROM matches WHERE loser = p.id))
      AS matches
  FROM players p
    LEFT OUTER JOIN matches m1 ON m1.winner = p.id
    LEFT OUTER JOIN matches m2 ON m2.loser = p.id
  GROUP BY p.id
  ORDER BY wins DESC, p.id ASC;


CREATE OR REPLACE VIEW ZERO_BYES AS
  SELECT *
  FROM STANDINGS s
  WHERE NOT exists(
      SELECT *
      FROM matches m
      WHERE m.winner = s.id
            AND m.loser IS NULL
  )
  ORDER BY s.wins ASC, s.id DESC;
