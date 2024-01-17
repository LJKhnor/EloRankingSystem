import unittest
from projet.elo.elo import Implementation

class TestImplementation(unittest.TestCase):

    def setUp(self):
        self.impl = Implementation()

    def test_getPlayerList(self):
        self.assertEqual(len(self.impl.players), 0)
        self.impl.addPlayer("Player 1")
        self.assertEqual(len(self.impl.players), 1)
        self.impl.addPlayer("Player 2")
        self.assertEqual(len(self.impl.players), 2)

    def test_getDeckList(self):
        self.assertEqual(len(self.impl.decks), 0)
        self.impl.addDeck("Deck 1")
        self.assertEqual(len(self.impl.decks), 1)
        self.impl.addDeck("Deck 2")
        self.assertEqual(len(self.impl.decks), 2)

    def test_getPlayer(self):
        self.impl.addPlayer("Player 1")
        self.assertEqual(self.impl.getPlayer("Player 1").name, "Player 1")
        self.assertIsNone(self.impl.getPlayer("Player 2"))

    def test_getDeck(self):
        self.impl.addDeck("Deck 1")
        self.assertEqual(self.impl.getDeck("Deck 1").name, "Deck 1")
        self.assertIsNone(self.impl.getDeck("Deck 2"))

    def test_getPlayers(self):
        self.impl.addPlayer("Player 1")
        self.impl.addPlayer("Player 2")
        self.assertEqual(self.impl.getPlayers(["Player 1", "Player 2"]), "Player 1 ,Player 2")

    def test_getDecks(self):
        self.impl.addDeck("Deck 1")
        self.impl.addDeck("Deck 2")
        self.assertEqual(self.impl.getDecks(["Deck 1", "Deck 2"]), "Deck 1 ,Deck 2")

    def test_contains(self):
        self.impl.addPlayer("Player 1")
        self.assertTrue(self.impl.contains("Player 1"))
        self.assertFalse(self.impl.contains("Player 2"))

    def test_addPlayer(self):
        self.impl.addPlayer("Player 1")
        self.assertEqual(len(self.impl.players), 1)
        self.assertEqual(self.impl.players[0].name, "Player 1")
        self.assertEqual(self.impl.players[0].rating, 1000)
        self.impl.addPlayer("Player 2", rating=1500)
        self.assertEqual(len(self.impl.players), 2)
        self.assertEqual(self.impl.players[1].name, "Player 2")
        self.assertEqual(self.impl.players[1].rating, 1500)

    def test_addDeck(self):
        self.impl.addDeck("Deck 1")
        self.assertEqual(len(self.impl.decks), 1)
        self.assertEqual(self.impl.decks[0].name, "Deck 1")
        self.assertEqual(self.impl.decks[0].rating, 1000)
        self.impl.addDeck("Deck 2", rating=1500)
        self.assertEqual(len(self.impl.decks), 2)
        self.assertEqual(self.impl.decks[1].name, "Deck 2")
        self.assertEqual(self.impl.decks[1].rating, 1500)

    def test_addPlayers(self):
        self.impl.addPlayers(["Player 1", "Player 2"])
        self.assertEqual(len(self.impl.players), 2)
        self.assertEqual(self.impl.players[0].name, "Player 1")
        self.assertEqual(self.impl.players[0].rating, 1000)
        self.assertEqual(self.impl.players[1].name, "Player 2")
        self.assertEqual(self.impl.players[1].rating, 1000)
        self.impl.addPlayers(["Player 3", "Player 4"], rating=1500)
        self.assertEqual(len(self.impl.players), 4)
        self.assertEqual(self.impl.players[2].name, "Player 3")
        self.assertEqual(self.impl.players[2].rating, 1500)
        self.assertEqual(self.impl.players[3].name, "Player 4")
        self.assertEqual(self.impl.players[3].rating, 1500)

    def test_addDecks(self):
        self.impl.addDecks(["Deck 1", "Deck 2"])
        self.assertEqual(len(self.impl.decks), 2)
        self.assertEqual(self.impl.decks[0].name, "Deck 1")
        self.assertEqual(self.impl.decks[0].rating, 1000)
        self.assertEqual(self.impl.decks[1].name, "Deck 2")
        self.assertEqual(self.impl.decks[1].rating, 1000)
        self.impl.addDecks(["Deck 3", "Deck 4"], rating=1500)
        self.assertEqual(len(self.impl.decks), 4)
        self.assertEqual(self.impl.decks[2].name, "Deck 3")
        self.assertEqual(self.impl.decks[2].rating, 1500)
        self.assertEqual(self.impl.decks[3].name, "Deck 4")
        self.assertEqual(self.impl.decks[3].rating, 1500)

    def test_removePlayer(self):
        self.impl.addPlayers(["Player 1", "Player 2"])
        self.assertEqual(len(self.impl.players), 2)
        self.impl.removePlayer("Player 1")
        self.assertEqual(len(self.impl.players), 1)
        self.assertEqual(self.impl.players[0].name, "Player 2")
        self.impl.removePlayer("Player 2")
        self.assertEqual(len(self.impl.players), 0)

    def test_removeDeck(self):
        self.impl.addDecks(["Deck 1", "Deck 2"])
        self.assertEqual(len(self.impl.decks), 2)
        self.impl.removeDeck("Deck 1")
        self.assertEqual(len(self.impl.decks), 1)
        self.assertEqual(self.impl.decks[0].name, "Deck 2")
        self.impl.removeDeck("Deck 2")
        self.assertEqual(len(self.impl.decks), 0)

    def test_recordMatch(self):
        self.impl.addPlayers(["Player 1", "Player 2"])
        self.impl.addDecks(["Deck 1", "Deck 2"])
        self.impl.recordMatch("Player 1", "Deck 1", "Player 2", "Deck 2", winner="Player 1")
        self.assertEqual(self.impl.getPlayer("Player 1").rating, 1042.0)
        self.assertEqual(self.impl.getPlayer("Player 2").rating, 958.0)
        self.assertEqual(self.impl.getDeck("Deck 1").rating, 1042.0)
        self.assertEqual(self.impl.getDeck("Deck 2").rating, 958.0)
        self.impl.recordMatch("Player 1", "Deck 2", "Player 2", "Deck 1", winner="Player 2")
        self.assertEqual(self.impl.getPlayer("Player 1").rating, 990.0389337445214)
        self.assertEqual(self.impl.getPlayer("Player 2").rating, 1009.9610662554786)
        self.assertEqual(self.impl.getDeck("Deck 1").rating, 1074.0389337445215)
        self.assertEqual(self.impl.getDeck("Deck 2").rating, 925.9610662554786)
        self.impl.recordMatch("Player 1", "Deck 1", "Player 2", "Deck 2", draw=True)
        self.assertEqual(self.impl.getPlayer("Player 1").rating, 992.4445990466214)
        self.assertEqual(self.impl.getPlayer("Player 2").rating, 1007.5554009533786)
        self.assertEqual(self.impl.getDeck("Deck 1").rating, 1057.1489407522918)
        self.assertEqual(self.impl.getDeck("Deck 2").rating, 942.8510592477083)

    def test_getPlayerRating(self):
        self.impl.addPlayers(["Player 1", "Player 2"])
        self.impl.addDecks(["Deck 1", "Deck 2"])
        self.assertEqual(self.impl.getPlayerRating("Player 1"), 1000)
        self.assertEqual(self.impl.getPlayerRating("Player 2"), 1000)
        self.impl.recordMatch("Player 1", "Deck 1", "Player 2", "Deck 2", winner="Player 1")
        self.assertEqual(self.impl.getPlayerRating("Player 1"), 1042.0)
        self.assertEqual(self.impl.getPlayerRating("Player 2"), 958.0)

    def test_getDeckRating(self):
        self.impl.addPlayers(["Player 1", "Player 2"])
        self.impl.addDecks(["Deck 1", "Deck 2"])
        self.assertEqual(self.impl.getDeckRating("Deck 1"), 1000)
        self.assertEqual(self.impl.getDeckRating("Deck 2"), 1000)
        self.impl.recordMatch("Player 1", "Deck 1", "Player 2", "Deck 2", winner="Player 1")
        self.assertEqual(self.impl.getDeckRating("Deck 1"), 1042.0)
        self.assertEqual(self.impl.getDeckRating("Deck 2"), 958.0)

