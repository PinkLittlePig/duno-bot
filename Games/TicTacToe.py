from Games.GameBaseClass import Game
from math import floor

class TicTacToe(Game):
    """First test game"""

    maxplayers = 2
    minplayers = 2

    def __init__(self, players, playerobjects):
        super().__init__(players, playerobjects)
        self.boardsize = 0
        self.board = self.createboard()
        self.numberref = {0:'x', 1:'o'}

    async def playfirst(self):
        await self.userobjects[self.playerindex].send(self.createsendboard())

    async def handlenewmessage(self, message):
        if message.author.id == self.getplayerid():
            if sendback := self.playnextmove(self.userobjects[self.playerindex], message):
                if self.boardsize == 0:
                    await self.nowinend()
                    return
                if isinstance(sendback, str):
                    await self.userobjects[self.playerindex].send(sendback)
                    self.IncrasePlayerIndex()
                    await self.userobjects[self.playerindex].send(self.createsendboard())
                else:
                    await self.endgame(self.userobjects[self.playerindex])
            else:
                await self.userobjects[self.playerindex].send('Please send a number that is shown and not taken')

    def playnextmove(self, playerobject, message):
        try:
            message = int(message.content)
        except ValueError:
            return False
        if message < len(self.board) * len(self.board[0]) and message in self.board[floor(message/3)]:
            self.board[floor(message/3)][message%3] = self.numberref[self.playerindex]
            if winmarker := self.checkforwin([message%3, floor(message/3)]):
                return winmarker
            else:
                return True
        else:
            return False

    def checkforwin(self, positionchanged):
        if [self.numberref[self.playerindex]]*3 == self.board[positionchanged[1]]:
            return False
        if [self.numberref[self.playerindex]]*3 == list(list(zip(*self.board))[0]):
            return False
        diagnal = []
        for number in range(len(self.board)):
            diagnal.append(self.board[number][number])
        if diagnal == [self.numberref[self.playerindex]]*3:
            return False
        diagnal = []
        for number in range(len(self.board)):
            diagnal.append(self.board[len(self.board)-1-number][number])
        if diagnal == [self.numberref[self.playerindex]]*3:
            return False
        self.boardsize -= 1
        return 'Wait for your next turn'

    def createboard(self, lenwidth=3):
        self.boardsize = lenwidth**2
        boardlist = []
        for y in range(lenwidth):
            row = []
            for x in range(lenwidth):
                row.append((y*3)+x)
            boardlist.append(row)
        return boardlist

    def createsendboard(self, placeseporator='|'):
        sendboard = ''
        rownumber = 0
        for row in range((len(self.board)*2)-1):
            if not(row%2):
                sendboard += placeseporator.join([str(number) for number in self.board[rownumber]])
                rownumber += 1
            else:
                sendboard += '-'*((len(placeseporator)+1)*len(self.board[0])-1)
            sendboard += '\n'
        return sendboard





#1|2|3
#-----
#o|5|o
#-----
#7|8|x
