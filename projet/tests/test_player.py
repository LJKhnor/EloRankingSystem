import unittest

from projet.model.player import _Player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player1 = _Player("Player 1", 1500.00)
        self.player2 = _Player("Player 2", 1500.00)

    def test_compareRating(self):
        self.assertEqual(self.player1.compare_rating(self.player2), 0.5)
        self.assertEqual(self.player2.compare_rating(self.player1), 0.5)

        self.player2.rating = 1600
        self.assertEqual(self.player1.compare_rating(self.player2), 0.35993500019711494)

        self.player2.rating = 1400
        self.assertEqual(self.player1.compare_rating(self.player2), 0.6400649998028851)

        self.player2.rating = 1250
        self.assertEqual(self.player1.compare_rating(self.player2), 0.8083176725494586)

    def test_str(self):
        self.assertEqual(str(self.player1), "Player 1 (1500.0)")
        self.assertEqual(str(self.player2), "Player 2 (1500.0)")


if __name__ == '__main__':
    unittest.main()
