import sqlite3
from random import randint
from DataBases.DataBaseClass import Database
from Games import GameUtil
from datetime import datetime
from Refs.Queref import Qref
from botclass import botgetclass
bot = botgetclass.bot
import discord

class CurrentGameDatabase(Database):
    """Stores games that are ongoing and the values associated with games"""

    def __init__(self, tablename='currentgamedata'):
        super().__init__(filename='GameData.db')
        self.tablename = tablename
        self.trycreatetable('keyaccess integer PRIMARY KEY, bet integer, createtime TEXT')
        self.currentgameobjects = {}
        self.gameplayers = {}

    def getgameinfo(self, key):
        return self.currentgameobjects[key]

    async def addgame(self, players, game, bet):
        playerobjects = [await bot.fetch_user(player) for player in players]
        if (queplayers := [player for player in players if player in self.gameplayers]):
            Qref.Quedata.addtoque([play for play in players if play not in queplayers], queplayers, game, bet)
            for player in playerobjects:
                await player.send('A requested game has been accepted but not all players are ready and the game has been qued')
            return
        key = self.randomString()
        for player in playerobjects:
            self.gameplayers[int(player.id)] = key
            await player.send('A game has started')
        gameclass = GameUtil.GameUtilitys.getgameobject(game)
        gameclass = gameclass(players, playerobjects)
        await gameclass.playfirst()
        self.currentgameobjects[key] = gameclass
        querys = [key, bet, self.getdatetime("""DATETIME('now', 'localtime')""")]
        self.addentery(*querys)
        return [[]]

    def DeleteGame(self, key):
        self.deletegameobj(key)
        self.removeentery(keyaccess=key)

    def deletegameobj(self, key):
        classobj = self.currentgameobjects.pop(key)
        del classobj

    async def deleteplayer(self, UserObject):
        self.gameplayers.pop(UserObject.id)
        if UserObject.id in Qref.Quedata.quedplayers:
            if (gameinfo := Qref.Quedata.readyplayer(UserObject.id)):
                await self.addgame(*gameinfo)
