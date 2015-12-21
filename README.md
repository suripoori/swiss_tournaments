# swiss_tournaments
This project creates a PostgreSQL backed database and obtains a swiss tournament pairing for all the players based on their scores

The database contains two tables "player" and "match". This is defined in the tournament.sql file.
- The "player" table contains all the player's names in the "name" column, and a serial primary key in the "id" column.
- The "match" table contains a mapping of all the matches between players. 
  > The integer "winner" will refer to the winning player's id. 
  > The integer "loser" will refer to the losing player's id.
  > Apart from these, there is a serial primary key in the "id" column which identifies each match.

Views have been utilized to keep track of a player's wins and number of matches. 
- The "wins" view contains three columns - Player's "id", Player's "name" and "wins". A count of the number of wins of a player is kept.
- The "matches" view contains three columns - "id", "name" and "matches". A count of the number of matches of each player is kept.

The tournament.py file contains a Python based library to access the database. 
Any client program built will use this library for the following functions:
- Delete all the matches from the tournament.
- Delete all the players from the tournament.
- Count the number of players in the tournament.
- Register a player to play in the tournament.
- Report a match between two players with the winner and loser player ids.
- Obtain all the player's standings in the tournament.
- Generate a Swiss pairing for all the players based on their scores. 

The tournament_test.py contains functions to do some basic unit tests on the functions provided in the tournament.py file.

To run this project on a VM, you'll need the following:
- A Vagrant VM which has:
  > Python 3.x
  > PostgreSQL database management system.
  > psql commandline interface.

Instructions to run:
1. Use the "vagrant up" command to start the virtual machine after navigating to the path where the Vagrant VM is present.
2. Use the "vagrant ssh" command to connect to the virtual machine after it is started.
3. The .py files need to be copied over into any location within the directory containing the Vagrantfile. 
   This directory will be automatically mounted under /vagrant in the VM. 
5. Create the database by running the contents of the tournament.sql file in psql command line.
6. Use the functions in tournament.py to interact with the database.

Alternatively, you can also just install and configure Python 3.x and PostgreSQL on the local system and skip steps 1,2 and 3. 

