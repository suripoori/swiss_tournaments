#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

class DB:

    def __init__(self, db_con_str="dbname=tournament"):
        """
        Creates a database connection with the connection string provided
        :param str db_con_str: Contains the database connection string, with a default value when no argument is passed to the parameter
        """
        self.conn = psycopg2.connect(db_con_str)

    def cursor(self):
        """
        Returns the current cursor of the database
        """
        return self.conn.cursor();

    def execute(self, sql_query_string, data=None, and_close=False):
        """
        Executes SQL queries
        :param str sql_query_string: Contain the query string to be executed
        :param bool and_close: If true, closes the database connection after executing and commiting the SQL Query
        """
        cursor = self.cursor()
        cursor.execute(sql_query_string, data)
        if and_close:
            self.conn.commit()
            self.close()
        return {"conn": self.conn, "cursor": cursor if not and_close else None}

    def close(self):
        """
        Closes the current database connection
        """
        return self.conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    DB().execute("DELETE FROM match", data=None, and_close=True)


def deletePlayers():
    """Remove all the player records from the database."""
    DB().execute("DELETE FROM player", data=None, and_close=True)


def countPlayers():
    """Returns the number of players currently registered."""
    conn = DB().execute("SELECT count(*) FROM player")
    cursor = conn["cursor"].fetchone()
    conn["conn"].close()
    return cursor[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    try:
        DB().execute("""INSERT INTO PLAYER (name) VALUES (%s);""", (name,), True)
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
    return_list = []
    try:
        sql = "SELECT wins.id, wins.name, wins.wins, matches.matches " \
              "FROM wins LEFT JOIN matches ON wins.id = matches.id " \
              "ORDER BY wins.wins DESC;"
        # conn = DB().execute("SELECT id, name FROM PLAYER ORDER BY SCORE DESC")
        conn = DB().execute(sql)
        result = conn["cursor"].fetchall()
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
    try:
        DB().execute(" INSERT INTO MATCH (winner, loser) VALUES (%s, %s);", (winner, loser), True)
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
    sql = "SELECT count(winner) AS wins FROM player LEFT JOIN match ON match.winner = player.id " \
          "where player.id = %s;"
    try:
        conn = DB().execute(sql, (id,))
        result = conn["cursor"].fetchone()[0]
        return int(result)
    except Exception as e:
        print("Could not get the score for the specified player id")
        raise e


def getPlayers():
    """
    :return: Dictionary of ids and players
    """
    return_dict = {}
    try:
        conn = DB().execute(" SELECT id, name FROM PLAYER")
        result = conn["cursor"].fetchall()
        for res in result:
            return_dict[res[0]] = res[1]
        return return_dict
    except Exception as e:
        print("Could not get all the players")
        raise e