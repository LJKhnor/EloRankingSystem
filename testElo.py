from elo import *


def main():
    i = Implementation()

    players = ["Joachim", "Julien Lejeune", "Julien Laurent", "Christopher", "Gilles", "Olivier", "Kader"]

    i.addPlayers(players)

    """
    This bunch of data represent the games in the Csv files "MTG-scores" for the period of 28/12/2023 to 03/01/2024
    """
    i.recordMatch("Joachim", "Julien Lejeune", winner="Joachim")
    i.recordMatch("Joachim", "Christopher", winner="Joachim")
    i.recordMatch("Julien Lejeune", "Gilles", winner="Gilles")
    i.recordMatch("Joachim", "Gilles", winner="Joachim")
    i.recordMatch("Julien Lejeune", "Christopher", winner="Julien Lejeune")
    i.recordMatch("Joachim", "Christopher", winner="Christopher")

    i.recordMatch("Julien Lejeune", "Gilles", winner="Julien Lejeune")
    i.recordMatch("Christopher", "Joachim", winner="Joachim")
    i.recordMatch("Julien Lejeune", "Joachim", winner="Julien Lejeune")
    i.recordMatch("Christopher", "Gilles", winner="Christopher")
    i.recordMatch("Christopher", "Julien Lejeune", winner="Julien Lejeune")
    i.recordMatch("Gilles", "Joachim", winner="Gilles")
    i.recordMatch("Gilles", "Julien Lejeune", winner="Julien Lejeune")
    i.recordMatch("Gilles", "Julien Lejeune", winner="Julien Lejeune")
    i.recordMatch("Julien Lejeune", "Joachim", winner="Julien Lejeune")
    # jusqu'au 09-01-2024


    print(i.getRatingList())
