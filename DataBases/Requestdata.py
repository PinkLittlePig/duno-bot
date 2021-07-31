import sqlite3
from DataBases.DataBaseClass import Database
from botclass import botgetclass
from datetime import datetime
from datetime import timedelta
from re import findall
import asyncio

class RequestedDatabase(Database):
    """Stores information on games that have been requested to play with another person"""

    def __init__(self, tablename='gamerequests'):
        super().__init__(filename='GameData.db')
        self.bot = botgetclass.bot
        self.tablename = tablename
        self.trycreatetable('RequestMessageId integer PRIMARY KEY, playerone integer, game integer, bet integer, createtime TEXT, accesskey integer')
        #uses 2d list one for accepted users and none accepted
        self.requestedgameopponents = {}
        self.requestmessageobj = {}
        self.lasttime = datetime.now()
        self.oldtimer = 1

    def fullremove(self, **removeq):
        if (entery := self.checkforentery(**removeq)[0]):
            self.removeentery(RequestMessageId=entery[0])
            self.requestedgameopponents.pop(entery[5])
            self.requestmessageobj.pop(entery[5])
            return entery
        print(entery)

    async def addrequest(self, MessageId, game, bet, playerone, Opponents, messageobj):
        if datetime.now() > self.lasttime + timedelta(minutes=self.oldtimer):
            await self.checkforold(self.oldtimer)
            self.lasttime = datetime.now()
        accesskey = self.randomString()
        self.requestmessageobj[accesskey] = messageobj
        self.requestedgameopponents[accesskey] = [[playerone], [*Opponents]]
        self.addentery(MessageId, playerone, game, bet, self.getdatetime("""DATETIME('now', 'localtime')"""), accesskey)

    def addacceptingplayer(self, newplayer, opponentskey):
        opponentlist = self.requestedgameopponents[opponentskey]
        if newplayer in opponentlist[1]:
            opponentlist[0].append(opponentlist[1].pop(opponentlist[1].index(newplayer)))
            if not(len(opponentlist[1])):
                return True
        return False

    async def checkforold(self, inactivetime):
        enterys = self.readallenterys()
        currenttime = datetime.now()
        for row in enterys:
            rowtime = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
            if (rowtime + timedelta(minutes=inactivetime)) < currenttime:
                userrequested = self.bot.get_user(row[1])
                await userrequested.send(f"A game request has been canceled")
                await self.requestmessageobj[row[0]].clear_reaction(u"\u2705")
                self.fullremove(playerone=row[0])
