#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    connection = psycopg2.connect("dbname=tournament")
    cursor = connection.cursor()

    return connection, cursor


def deleteMatches():
    """Remove all the match records from the database."""
    connection, cursor = connect()

    cursor.execute('''
        delete from matches
    ''')

    connection.commit()
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection, cursor = connect()

    cursor.execute('''
        delete from players
    ''')

    connection.commit()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    connection, cursor = connect()

    cursor.execute('''
        select count(*) from players
    ''')
    count = cursor.fetchone()

    connection.close()
    return count[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    connection, cursor = connect()

    cursor.execute('insert into players(name) values(%s)', (name,))

    connection.commit()
    connection.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection, cursor = connect()

    cursor.execute('''
        select * from standings
    ''')

    standings = cursor.fetchall()

    connection.commit()
    connection.close()

    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection, cursor = connect()

    cursor.execute('insert into matches(winner, loser) values(%s, %s)', (winner, loser))

    connection.commit()
    connection.close()


def bye(player):
    """Records a bye

    Args:
      winner:  the id number of the player has a bye
    """
    reportMatch(player, None)

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    connection, cursor = connect()

    standings = playerStandings()
    if len(standings) % 2 == 1:
        # find the weakest player that has not received any bye yet.
        cursor.execute('''
            select * from ZERO_BYES
        ''')
        player = cursor.fetchone()
        standings.remove(player)

        # append that player and a bot to allow him a free-win
        standings.append(player)
        standings.append((None, 'Loser Bot', 0, 0))

    connection.close()

    return [
        (standings[i][0],
         standings[i][1],
         standings[i + 1][0],
         standings[i + 1][1]) for i in range(0, len(standings), 2)]
