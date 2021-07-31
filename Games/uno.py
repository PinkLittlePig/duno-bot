from Games.GameBaseClass import Game
from Images import GameImageGen
import random
from os import remove

class UnoGame(Game):
    """docstring for ."""

    maxplayers = 10
    minplayers = 2

    def __init__(self, players, playerobjects):
        super().__init__(players, playerobjects)
        self.deck = self.CreateDeck()
        self.lastcard = self.GetRandomCard()
        while int(self.lastcard[1:]) > 9:
            self.lastcard = self.GetRandomCard()
        self.playerscard = self.GivePlayersCards()
        self.cardfunctions = {'10':self.SkipCard, '11':self.ReverseCard, '12':self.PickUpTwoCard, '13':{'0':self.ChangeColor, '2':self.ChangeColorFour}}
        self.cardcolours = {'0':(237, 21, 21), '1':(247, 244, 20), '2':(2, 242, 66), '3':(21, 105, 237)}
        self.secondaryFunction = 0
        self.secondaryFunctions = {0:self.MainSendback, 1:self.PickUpSecond, 2:self.ChangeColourSecond, 3:self.ChangeColourFourSecond, 4:self.UnoSecond}
        self.tempcard = '000'

    async def playfirst(self):
        EmbededMes, ImgFile, ImgFileName = self.GetNextPlayerSeandable()
        await self.userobjects[self.playerindex].send(file=ImgFile, embed=EmbededMes)
        remove(f'Images/TempPics/{ImgFileName}.png')

    async def handlenewmessage(self, message):
        print(self.playerscard)
        if message.author.id == self.getplayerid() and self.secondaryFunction != 4:
            if self.RepresentsInt(message.content):
                await self.secondaryFunctions[self.secondaryFunction](message.content)
                return
            else:
                await self.userobjects[self.playerindex].send('Please send a valid number')
        if self.secondaryFunction == 4:
            await self.secondaryFunctions[self.secondaryFunction](message.content, message.author.id)
            return

    async def MainSendback(self, message):
        playercards = self.playerscard[self.getplayerid()]
        playableIndexes = self.GetPlayableCards(playercards)
        if int(message) <= len(playableIndexes) and int(message) > 0:
            if len(playercards) - 1 <= 1:
                self.tempcard = playercards[playableIndexes[int(message)-1]]
                await self.CheckWin()
                return
            await self.checkCardFunction(playercards[playableIndexes[int(message)-1]])
        elif int(message) == len(playableIndexes)+1:
            await self.PickUpCard()
        else:
            await self.userobjects[self.playerindex].send('Please send a valid number')

    async def PickUpSecond(self, message):
        if int(message) == 0:
            self.secondaryFunction = 0
            self.IncrasePlayerIndex()
            await self.SendNext()
        elif int(message) == 1:
            self.secondaryFunction = 0
            await self.checkCardFunction(self.playerscard[self.getplayerid()][-1])
        else:
            await self.userobjects[self.playerindex].send('Please send a valid number')

    async def ChangeColourSecond(self, message):
        if int(message) > 0 and int(message) < 5:
            self.secondaryFunction = 0
            self.lastcard = f'{int(message)-1}14'
            self.IncrasePlayerIndex()
            await self.SendNext()
        else:
            await self.userobjects[self.playerindex].send('Please send a valid number')

    async def ChangeColourFourSecond(self, message):
        if int(message) > 0 and int(message) < 5:
            self.secondaryFunction = 0
            self.lastcard = f'{int(message)-1}15'
            self.IncrasePlayerIndex()
            self.AddCards(amount=4)
            await self.userobjects[self.playerindex].send('You have picked up four and lost your turn')
            self.IncrasePlayerIndex()
            await self.SendNext()
        else:
            await self.userobjects[self.playerindex].send('Please send a valid number')

    async def UnoSecond(self, message, userid):
        if message == 'uno':
            self.secondaryFunction = 0
            if userid == self.getplayerid():
                for user in self.userobjects:
                    if user.id != self.getplayerid():
                        await user.send(f'{self.userobjects[self.playerindex].name} sent uno first.')
                    else:
                        await user.send('You sent uno first and dont have to pick up two cards')
            else:
                self.AddCards(amount=2)
                for user in self.userobjects:
                    if user.id != self.getplayerid():
                        await user.send(f'{self.userobjects[self.playerids.index(userid)].name} sent uno first and {self.userobjects[self.playerindex].name} picked up two cards.')
                    else:
                        await user.send(f'{self.userobjects[self.playerids.index(userid)].name} sent uno first and you picked up two cards')
            await self.checkCardFunction(self.tempcard)

    async def PickUpCard(self):
        PickUp = self.AddCards()[0]
        if len(self.GetPlayableCards([PickUp])):
            self.secondaryFunction = 1
            CardFile = GameImageGen.SaveSingleCard(PickUp)
            embededSend, ImageFile = self.CreateEmbeded('This is the card you picked up would you like to play it?', 'Send 1 if you would like to play and 0 if not', self.cardcolours[PickUp[0]], CardFile, {})
            await self.userobjects[self.playerindex].send(file=ImageFile, embed=embededSend)
            remove(f'Images/TempPics/{CardFile}.png')
            return
        CardFile = GameImageGen.SaveSingleCard(PickUp)
        embededSend, ImageFile = self.CreateEmbeded('This is the card you picked up!', '', self.cardcolours[PickUp[0]], CardFile, {})
        await self.userobjects[self.playerindex].send(file=ImageFile, embed=embededSend)
        remove(f'Images/TempPics/{CardFile}.png')
        self.IncrasePlayerIndex()
        await self.SendNext()

    async def checkCardFunction(self, cardNumber):
        if cardNumber[1:] == '13':
            await self.cardfunctions[cardNumber[1:]][cardNumber[0]](cardNumber)
        elif cardNumber[1:] in self.cardfunctions:
            await self.cardfunctions[cardNumber[1:]](cardNumber)
        else:
            await self.RegularCard(cardNumber)

    async def RegularCard(self, cardNumber):
        self.PlayCard(cardNumber)
        self.IncrasePlayerIndex()
        await self.SendNext()

    async def SkipCard(self, cardNumber):
        self.PlayCard(cardNumber)
        self.IncrasePlayerIndex()
        await self.userobjects[self.playerindex].send('Your turn has been skiped')
        self.IncrasePlayerIndex()
        await self.SendNext()

    async def ReverseCard(self, cardNumber):
        self.PlayCard(cardNumber)
        if len(self.playerids) == 2:
            self.IncrasePlayerIndex()
            await self.userobjects[self.playerindex].send('Your turn has been skiped')
            self.IncrasePlayerIndex()
            await self.SendNext()
        else:
            self.playerids = (leftLen := self.playerids[self.playerindex+1:][::-1]) + [self.playerids[self.playerindex]] + self.playerids[:self.playerindex][::-1]
            self.userobjects = self.userobjects[self.playerindex+1:][::-1] + [self.userobjects[self.playerindex]] + self.userobjects[:self.playerindex][::-1]
            self.playerindex = len(leftLen)
            self.IncrasePlayerIndex()
            await self.SendNext()

    async def PickUpTwoCard(self, cardNumber):
        self.PlayCard(cardNumber)
        self.IncrasePlayerIndex()
        self.AddCards(amount=2)
        await self.userobjects[self.playerindex].send('You picked up two and had your turn skiped')
        self.IncrasePlayerIndex()
        await self.SendNext()

    async def ChangeColor(self, cardNumber):
        self.PlayCard(cardNumber)
        self.secondaryFunction = 2
        await self.userobjects[self.playerindex].send('Send back the coresponding number for the colour you would like to change to\n1 - Red, 2 - Yellow, 3 - Green, 4 - Blue')

    async def ChangeColorFour(self, cardNumber):
        self.PlayCard(cardNumber)
        self.secondaryFunction = 3
        await self.userobjects[self.playerindex].send('Send back the coresponding number for the colour you would like to change to\n1 - Red, 2 - Yellow, 3 - Green, 4 - Blue')

    async def SendNext(self):
        EmbededMes, ImgFile, ImgFileName = self.GetNextPlayerSeandable()
        await self.userobjects[self.playerindex].send(file=ImgFile, embed=EmbededMes)
        remove(f'Images/TempPics/{ImgFileName}.png')

    async def CheckWin(self):
        if (CardAmount := len(self.playerscard[self.getplayerid()])-1) == 1:
            await self.unocall()
            return True
        elif not(CardAmount):
            await self.endgame(self.userobjects[self.playerindex])
            return True
        else:
            return False

    async def unocall(self):
        self.secondaryFunction = 4
        for user in self.userobjects:
            if user.id != self.getplayerid():
                await user.send(f'Send back "uno" before {self.userobjects[self.playerindex].name}')
            else:
                await user.send(f'Send back "uno" before everyone')

    def CreateDeck(self):
        # First number in color second is type of card
        # 013 = change color,  213 = +4
        #0 = red, 1 = yellow, 2 = green, 3 = blue
        deck = {}
        deck['013'] = 4
        deck['213'] = 4
        for color in range(4):
            deck[str(color) + '0'] = 1
            for card in range(1, 13):
                deck[str(color) + str(card)] = 2
        return deck

    def AddCards(self, amount=1):
        CardsAdded = [self.GetRandomCard() for i in range(amount)]
        self.playerscard[self.playerids[self.playerindex]] += CardsAdded
        return CardsAdded

    def GetRandomCard(self):
        cardNumber = random.choice(list(self.deck.keys()))
        self.deck[cardNumber] -= 1
        if self.deck[cardNumber] == 0:
            self.deck.pop(cardNumber)
            if len(list(self.deck.keys())) == 0:
                self.deck = self.CreateDeck()
        return cardNumber

    def GivePlayersCards(self, numbofcards=3):
        playercards = {}
        for player in self.playerids:
            playercards[player] = [self.GetRandomCard() for i in range(numbofcards)]
        return playercards

    def PlayCard(self, card):
        self.playerscard[self.getplayerid()].remove(card)
        self.lastcard = card

    def GetPlayableCards(self, playablecards):
        playableIndexes = []
        for card in range(len(playablecards)):
            if playablecards[card][0] == self.lastcard[0] or playablecards[card][1:] == self.lastcard[1:] or playablecards[card][1:] == '13':
                playableIndexes.append(card)
                continue
        return playableIndexes

    def GetNextPlayerSeandable(self):
        playercards = self.playerscard[self.getplayerid()]
        playableIndexes = self.GetPlayableCards(playercards)
        ImgFileName = GameImageGen.CreateUnoSendable(playercards, playableIndexes, self.lastcard)
        playerlist = ', '.join([user.name for user in self.userobjects])
        dictsend = self.GetPlayerCardAmounts()
        dictsend['The Game Order Is'] = playerlist
        Embded, ImageFile = self.CreateEmbeded('Its your turn! Send back the number under the action you would like to Take!', 'Below are the amount of cards other players have and the game order', self.cardcolours[self.lastcard[0]], ImgFileName, dictsend)
        return Embded, ImageFile, ImgFileName

    def GetPlayerCardAmounts(self):
        CardAmounts = {}
        for player in self.userobjects:
            if player.id != self.playerids[self.playerindex]:
                CardAmounts[player.name] = len(self.playerscard[player.id])
        return CardAmounts
