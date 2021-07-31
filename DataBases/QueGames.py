import sqlite3
from DataBases.DataBaseClass import Database

class QueDataInfo(Database):
    """docstring for ."""

    def __init__(self, tablename='quedata'):
        super().__init__(filename='GameData.db')
        self.tablename = tablename
        self.trycreatetable('keyaccess integer PRIMARY KEY, game integer, bet integer')
        self.quedplayers = {}
        self.quedgames = {}

    def addtoque(self, readyplayers, toqueplayers, bet, game):
        key = self.randomString()
        self.quedgames[key] = [[*readyplayers], [*toqueplayers]]
        for player in toqueplayers:
            if player in self.quedplayers:
                self.quedplayers[player].append(key)
            else:
                self.quedplayers[player] = [key]
        self.addentery(key, bet, game)

    def readyplayer(self, player):
        gamekey = self.quedplayers[player][0]
        gamelist = self.quedgames[gamekey]
        gamelist[0].append(gamelist[1].pop(gamelist[1].index(player)))
        if not(len(gamelist[1])):
            gameinfo = self.checkforentery(keyaccess=gamekey)[0]
            self.removeentery(keyaccess=gamekey)
            del self.quedgames[gamekey]
            self.quedplayers[player].pop()
            if not(len(self.quedplayers[player])):
                del self.quedplayers[player]
            return [gamelist[0], gameinfo[1], gameinfo[2]]
        return []
