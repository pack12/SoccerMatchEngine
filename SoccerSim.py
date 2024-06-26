from Game import Game
from Player import Player, PlayerData
def main():
    game = Game()

    game_players = [Player("Andre", "Onana", False, 67, "Manchester United",dribbling=5)
        ,Player("Luke","Shaw",False,2,"Manchester United"),
    Player("Nemenja", "Matic", False,24,"Manchester United"),
     Player("Lisandro", "Martinez", False,35,"Manchester United"),
     Player("Aaron", "Wan-Bissaka", False,57,"Manchester United"),
     Player("Casemiro","",False,15, "Manchester United"),
     Player("Kobbie","Mainoo",False,37, "Manchester United"), # Originally 37
     Player("Alejandro", "Garnacho", False,60,"Manchester United"),
     Player("Bruno", "Fernandes",False,27,"Manchester United"), # Originally 27
     Player("Marcus","Rashford", False,5,"Manchester United"),
     Player("Rasmus", "Hojlund",False,28,"Manchester United",kickOff=False,passing=10),

    Player("Ederson","Morares",False,68,"Manchester City",speed=12)
        ,Player("Nathan", "Ake", False,65,"Manchester City",speed=13,workRate=5),
     Player("Josko", "Gvardiol",False,32,"Manchester City",speed=13), # Originally 32
     Player("Rueben", "Dias", False, 43, "Manchester City",speed=12), # Originally 43
     Player("Kyle", "Walker", False,10, "Manchester City",speed=20,workRate=4),
     Player("Rodri", "", False, 42, "Manchester City",speed=13),
     Player("Kevin", "De Bruyne", False,30,"Manchester City",speed=13),
     Player("Julien", "Alvarez", False, 52, "Manchester City",speed=18),
     Player("Phil", "Foden", False, 63, "Manchester City,",speed=18),
     Player("Bernardo", "Silva", False,8, "Manchester City",speed=14),
    Player("Erling", "Haaland", True,28,"Manchester City",kickOff=True, speed=17)]


    playerData = PlayerData(game_players)

    game.run(playerData)
main()
