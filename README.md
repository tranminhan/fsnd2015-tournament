# Tournament Planner

This project is a Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.
The game tournament use the Swiss system for pairing up players in each round.

# How to run

There is no interface or main method in this project, instead, functionality is illustrated in test cases in `tournament_test.py`.

# Extra Functionality

- This project supports odd number of players. When this happens, one player received a bye.
A bye is represented a match between a player vs `None` or `Null`. See the test `testPairingsWithOddNumberOfPlayers`.
In order to assign a bye to a player, the project looks for the weakest player that does not receive any bye yet, see the view `ZERO_BYES`.

- The project simulates the result for tournaments of `N` players. See `testSimulateGames`.

