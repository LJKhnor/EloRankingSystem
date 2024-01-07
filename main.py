from elo import *

i = Implementation()

players = ["Joachim","Julien Lejeune","Julien Laurent","Christopher","Gilles","Olivier","Kader"]
decks = ["test1","test2","test3","truelove"]

i.addPlayers(players)
i.addDecks(decks)

# print("players list :", players)
# print(i.getPlayers(players))
# print(i.getRatingList())
# print(i.getPlayer("Joachim"))
# print(i.getPlayerRating("Joachim"))


"""
This bunch of data represent the match in the Csv files "MTG-scores" for the period from 28/12/2023 to 03/01/2024
"""
i.recordMatch("Joachim", "test1", "Julien Lejeune", "test3", winner="Joachim")
i.recordMatch("Joachim", "test1", "Christopher", "test2", winner="Joachim")
i.recordMatch("Julien Lejeune", "test2", "Gilles", "truelove", winner="Gilles")
i.recordMatch("Joachim", "truelove", "Gilles", "test1", winner="Joachim")
# i.recordMatch("Julien Lejeune", "Christopher", winner="Julien Lejeune")
# i.recordMatch("Joachim", "Christopher", winner="Christopher")


print(i.getPlayersRatingList())
print(i.getDecksRatingList())

""" 
This piece of code specify wich of our class is the main project class.
More information on https://docs.python.org/3/library/__main__.html
"""
# if __name__ == "__main__":
#     main()