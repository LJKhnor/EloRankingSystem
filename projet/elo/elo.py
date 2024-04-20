# pylint: disable=missing-function-docstring,unused-argument,too-many-arguments,line-to-long
"""
Created 06-01-2024
All of the classes for EloPy. The users should only interact with the Implementation class.
@author - Lejeune Joachim, Rosier Gilles originally create by Hank Hang Kai Sheehan
"""

from flask import Flask

from ..model.deck import _Deck
from ..model.player import _Player

app = Flask(__name__)
LOG = app.logger


class Implementation:
    """
    A class that represents an implementation of the Elo Rating System
    """

    def __init__(self, base_rating=1000):
        """
        Runs at initialization of class object.
        @param base_rating - The rating a new player would have
        """
        self.base_rating = base_rating
        self.players = []
        self.decks = []

    def __get_player_list(self):
        """
        Returns this implementation's player list.
        @return - the list of all player objects in the implementation.
        """
        return self.players

    def __get_deck_list(self):
        """
        Returns this implementation's decks list.
        @return - the list of all deck objects in the implementation.
        """
        return self.decks

    def get_player(self, name):
        """
        Returns the player in the implementation with the given name.
        @param name - name of the player to return.
        @return - the player with the given name.
        """
        for player in self.players:
            if player.name == name:
                return player
        return None

    def get_deck(self, name):
        """
        Returns the deck in the implementation with the given name.
        @param name - name of the deck to return.
        @return - the deck with the given name.
        """
        for deck in self.decks:
            if deck.name == name:
                return deck
        return None

    def get_players(self, players):
        """
        Return all the players in the list
        """
        return " ,".join(players)

    def get_decks(self, decks):
        """
        Return all the decks in the list
        """
        return " ,".join(decks)

    def contains(self, name):
        """
        Returns true if this object contains a player with the given name.
        Otherwise returns false.
        @param name - name to check for.
        """
        for player in self.players:
            if player.name == name:
                return True
        return False

    def add_player(self, name, rating=None):
        """
        Adds a new player to the implementation.
        @param name - The name to identify a specific player.
        @param rating - The player's rating.
        """
        if rating == None:
            rating = self.base_rating

        self.players.append(_Player(name=name, rating=rating))

    def add_deck(self, name, rating=None):
        """
        Adds a new deck to the implementation.
        @param name - The name to identify a specific deck.
        @param rating - The decks's rating.
        """
        if rating == None:
            rating = self.base_rating

        self.decks.append(_Deck(name=name, rating=rating))

    def add_players(self, players, rating=None):
        """
        Add a list of players to the implementation class
        @param players - the players list
        @param rating - the global rating for all players
        """
        for player in players:
            self.add_player(player, rating)

    def add_decks(self, decks, rating=None):
        """
        Add a list of decks to the implementation class
        @param decks - the decks list
        @param rating - the global rating for all decks
        """
        for deck in decks:
            self.add_deck(deck, rating)

    def remove_player(self, name):
        """
        Adds a new player to the implementation.
        @param name - The name to identify a specific player.
        """
        self.__get_player_list().remove(self.get_player(name))

    def remove_deck(self, name):
        """
        Remove a deck to the implementation.
        @param name - The name to identify a specific deck.
        """
        self.__get_deck_list().remove(self.get_deck(name))

    def process_elo_for_match(self, name1, deck_name1, name2, deck_name2, winner=None, draw=False):
        """
        Should be called after a game is played.
        @param name1 - name of the first player.
        @param name2 - name of the second player.
        """
        players = []
        decks = []

        for player in self.players:
            players.append(player.name)

        for deck in self.decks:
            decks.append(deck.name)

        if (name1 in players and name2 in players and deck_name1 in decks and deck_name2 in decks):

            player1 = self.get_player(name1)
            player2 = self.get_player(name2)
            deck1 = self.get_deck(deck_name1)
            deck2 = self.get_deck(deck_name2)

            expected1 = player1.compare_rating(player2)
            expected2 = player2.compare_rating(player1)
            deck_expected1 = deck1.compare_rating(deck2)
            deck_expected2 = deck2.compare_rating(deck1)

            rating1 = player1.rating
            rating2 = player2.rating
            deck_rating1 = deck1.rating
            deck_rating2 = deck2.rating

            if draw:
                score1 = 0.5
                score2 = 0.5
                deckScore1 = 0.5
                deckScore2 = 0.5
            elif winner == name1:
                score1 = 1.0
                score2 = 0.0
                deckScore1 = 1.0
                deckScore2 = 0.0
            elif winner == name2:
                score1 = 0.0
                score2 = 1.0
                deckScore1 = 0.0
                deckScore2 = 1.0
            else:
                raise Exception('One of the names must be the winner or draw must be True')

            newRating1 = rating1 + self.process_k(player1) * (score1 - expected1)
            newRating2 = rating2 + self.process_k(player2) * (score2 - expected2)
            newDeckRating1 = deck_rating1 + self.process_k(deck1) * (deckScore1 - deck_expected1)
            newDeckRating2 = deck_rating2 + self.process_k(deck2) * (deckScore2 - deck_expected2)

            if newRating1 < 0:
                newRating1 = 0
                newRating2 = rating2 - rating1

            if newRating2 < 0:
                newRating2 = 0
                newRating1 = rating1 - rating2

            if newDeckRating1 < 0:
                newDeckRating1 = 0
                newDeckRating2 = deck_rating2 - deck_rating1

            if newDeckRating2 < 0:
                newDeckRating2 = 0
                newDeckRating1 = newDeckRating1 - newDeckRating2

            player1.rating = newRating1
            player2.rating = newRating2

            deck1.rating = newDeckRating1
            deck2.rating = newDeckRating2

        else:
            raise Exception("One or more player you provide don't exist in this Elo league.")

    def process_k(self, player):
        """
        Return the k value for the new rating
        In real the k depends of the match number of the player, but here, the more you are powerful, the less you earn
        """
        rating = player.rating
        if rating < 1100:
            return 40
        elif 1100 < rating < 1300:
            return 20
        else:
            return 10

    def get_player_rating(self, name):
        """
        Returns the rating of the player with the given name.
        @param name - name of the player.
        @return - the rating of the player with the given name.
        """
        player = self.get_player(name)
        return player.rating

    def get_deck_rating(self, name):
        """
        Returns the rating of the deck with the given name.
        @param name - name of the deck.
        @return - the rating of the deck with the given name.
        """
        deck = self.get_deck(name)
        return deck.rating

    def get_players_rating_list(self):
        """
        Returns a list of tuples in the form of ({name},{rating})
        @return - the list of tuples
        """
        lst = []
        for player in self.__get_player_list():
            lst.append((player.name, round(player.rating, 2)))
        return sorted(lst, key=lambda player: player[1], reverse=True)

    def get_decks_rating_list(self):
        """
        Returns a list of tuples in the form of ({name},{rating})
        @return - the list of tuples
        """
        lst = []
        for deck in self.__get_deck_list():
            lst.append((deck.name, round(deck.rating, 2)))
        return sorted(lst, key=lambda deck: deck[1], reverse=True)
