from Games.Battleship import BattleShipGame
from Games.TicTacToe import TicTacToe
from Games.uno import UnoGame

class GameUtilitys:
    keylegend = {'TicTacToe':1, 'uno':2}

    @staticmethod
    def getgameobject(key):
        gamelegend = {0:BattleShipGame, 1:TicTacToe, 2:UnoGame}
        return gamelegend[key]

    @staticmethod
    def checkplayercountwithcall(message, players):
        #gets game class checks is min and max player and makes sure the playercount passed is good
        message = message.split(' ', 1)
        key = GameUtilitys.keylegend[message[0][1:]]
        return GameUtilitys.checkplayercount(key, players)

    @staticmethod
    def checkplayercount(gamekey, players):
        #gets game class checks is min and max player and makes sure the playercount passed is good
        gameclass = GameUtilitys.getgameobject(gamekey)
        if gameclass.maxplayers < players or gameclass.minplayers > players:
            return False
        return True
