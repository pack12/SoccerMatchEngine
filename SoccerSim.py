from Game import Game
from Player import Player, PlayerData
def main():
    game = Game()

    game_players = [Player("Luke","Shaw",False,2,"Manchester United"),
    Player("Nemenja", "Matic", False,24,"Manchester United"),
     Player("Lisandro", "Martinez", False,35,"Manchester United"),
     Player("Aaron", "Wan-Bissaka", False,57,"Manchester United"),
     Player("Casemiro","",False,15, "Manchester United"),
     Player("Kobbie","Mainoo",False,37, "Manchester United"), # Originally 37
     Player("Alejandro", "Garnacho", False,60,"Manchester United"),
     Player("Bruno", "Fernandes",False,27,"Manchester United"), # Originally 27
     Player("Marcus","Rashford", False,5,"Manchester United"),
     Player("Rasmus", "Hojlund",True,28,"Manchester United"),

    Player("Nathan", "Ake", False,65,"Manchester City"),
     Player("Josko", "Gvardiol",False,32,"Manchester City"), # Originally 32
     Player("Rueben", "Dias", False, 43, "Manchester City"), # Originally 43
     Player("Kyle", "Walker", False,10, "Manchester City"),
     Player("Rodri", "", False, 42, "Manchester City"),
     Player("Kevin", "De Bruyne", False,30,"Manchester City"),
     Player("Julien", "Alvarez", False, 52, "Manchester City"),
     Player("Phil", "Foden", False, 63, "Manchester City"),
     Player("Bernardo", "Silva", False,8, "Manchester City"),
    Player("Erling", "Haaland", False,28,"Manchester City")]


    playerData = PlayerData(game_players)

    game.run(playerData)
main()
