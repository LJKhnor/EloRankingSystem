import unittest

from projet.model.deck import _Deck


@unittest.skip("Need to be fixed")
class TestDeck(unittest.TestCase):

    def setUp(self):
        self.deck1 = _Deck("deck 1", 1500.00)
        self.deck2 = _Deck("deck 2", 1500.00)

    def test_compareRating(self):
        self.assertEqual(self.deck1.compare_rating(self.deck2), 0.5)
        self.assertEqual(self.deck2.compare_rating(self.deck1), 0.5)

        self.deck2.rating = 1600
        self.assertEqual(self.deck1.compare_rating(self.deck2), 0.35993500019711494)

        self.deck2.rating = 1400
        self.assertEqual(self.deck1.compare_rating(self.deck2), 0.6400649998028851)

        self.deck2.rating = 1250
        self.assertEqual(self.deck1.compare_rating(self.deck2), 0.8083176725494586)

    def test_str(self):
        self.assertEqual(str(self.deck1), "deck 1 (1500.0)")
        self.assertEqual(str(self.deck2), "deck 2 (1500.0)")

if __name__ == '__main__':
    unittest.main()
