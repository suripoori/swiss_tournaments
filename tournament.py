#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    conn = psycopg2.connect("dbname=tournament")
    return conn


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(" DELETE FROM MATCH; ")
        conn.commit()
    except Exception as e:
        print("Delete matches could not be completed")


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(" DELETE FROM MATCH; ")
        cur.execute(" DELETE FROM PLAYER; ")
        conn.commit()
    except Exception as e:
        print("Delete matches could not be completed")
        raise e


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM PLAYER; ")
        result = cur.fetchone()[0]
        return int(result)
    except Exception as e:
        print("Could not count the number of players")
        raise e


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""INSERT INTO PLAYER (name, score, matches) VALUES (%s, %s, %s);""", (bleach.clean(name), 0, 0))
        conn.commit()
    except Exception as e:
        print("Could not register a player {} into the tournament".format(name))
        raise e


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
    conn = connect()
    cur = conn.cursor()
    return_list = []
    try:
        cur.execute("SELECT id, name, score, matches FROM PLAYER ORDER BY SCORE DESC")
        result = cur.fetchall()
        for res in result:
            return_list.append((res[0], res[1], res[2], res[3]))
        return return_list
    except Exception as e:
        print("Could not get all the players standings")
        raise e


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(" INSERT INTO MATCH (winner, loser) VALUES ('{}', '{}');".format(winner, loser))
        score = getScore(winner)
        score += 1
        winner_matches = getMatches(winner)
        loser_matches = getMatches(loser)
        winner_matches += 1
        loser_matches += 1
        cur.execute(" UPDATE PLAYER SET score = {}, matches = {} WHERE id = {};".format(score, winner_matches, winner))
        cur.execute(" UPDATE PLAYER SET matches = {} WHERE id = {};".format(loser_matches, loser))
        conn.commit()
    except Exception as e:
        print("Could not write into MATCH table or update player table")
        raise e
 
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
    output = []
    standings = playerStandings()
    i = 0
    while(i < len(standings)-1):
        output.append((standings[i][0], standings[i][1], standings[i+1][0], standings[i+1][1]))
        i += 2
    return output


def getScore(id):
    """
    Returns the score of the player
    :param id: ID of the player
    :return: integer score
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(" SELECT score FROM PLAYER WHERE id = {}".format(id))
        result = cur.fetchone()[0]
        return int(result)
    except Exception as e:
        print("Could not get the score for the specified player id")
        raise e

def getPlayers():
    """
    :return: Dictionary of ids and players
    """
    return_dict = {}
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(" SELECT id, name FROM PLAYER")
        result = cur.fetchall()
        for res in result:
            return_dict[res[0]] = res[1]
        return return_dict
    except Exception as e:
        print("Could not get all the players")
        raise e


def getMatches(id):
    """
    Returns the number of matches of the player
    :param id: ID of the player
    :return: integer number of matches
    """
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(" SELECT matches FROM PLAYER WHERE id = {}".format(id))
        result = cur.fetchone()[0]
        return int(result)
    except Exception as e:
        print("Could not get the matches for the specified player id")
        raise e