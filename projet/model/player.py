class _Player:
    """
    A class to represent a player in the Elo Rating System
    """

    def __init__(self, name, rating):
        """
        Runs at initialization of class object.
        @param name - player name
        @param rating - player rating
        """
        self.name = name
        self.rating = rating

    def compare_rating(self, opponent):
        """
        Compares the two ratings of the player and his/her opponent.
        @param opponent - the player to compare against.
        @returns - The expected score between the two players.
        """
        return (1 + 10 ** ((opponent.rating - self.rating) / 400.0)) ** -1

    def __str__(self):
        return "{} ({})".format(self.name, round(self.rating, 2))