from botclass import botgetclass
import Refs.databaserefs as df
from discord import File
from discord import Embed
from discord import Colour

class Game():
    """Base class for all games"""

    def __init__(self, playerids, playerobjects):
        self.playerids = playerids
        self.userobjects = playerobjects
        self.bot = botgetclass.bot
        self.playerindex = 0

    async def endgame(self, winner):
        key = df.dataref.CurrentGames.gameplayers[winner.id]
        gamedataentery = df.dataref.CurrentGames.checkforentery(keyaccess=key)[0]
        df.dataref.CurrentGames.DeleteGame(key)
        for player in self.userobjects:
            playerdata = df.dataref.Userinfodata.checkforentery(user=player.id)[0]
            if player.id != winner.id:
                await player.send(f'The game is over the winner is {winner.name}')
                df.dataref.Userinfodata.updateuser(player.id, currency=playerdata[1]-gamedataentery[1], totalgamesplayed=playerdata[3]+1)
            else:
                df.dataref.Userinfodata.updateuser(player.id, currency=playerdata[1]+(gamedataentery[1]*(len(self.userobjects)-1)), totalgamesplayed=playerdata[3]+1, wins=playerdata[4]+1)
                await winner.send('You have Won the game')
            await df.dataref.CurrentGames.deleteplayer(player)

    def RepresentsInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    async def endgameshort(self, Ender):
        key = df.dataref.CurrentGames.gameplayers[self.playerids[0]]
        gamedataentery = df.dataref.CurrentGames.checkforentery(keyaccess=key)[0]
        for user in self.userobjects:
            playerdata = df.dataref.Userinfodata.checkforentery(user=user.id)[0]
            if user != Ender:
                df.dataref.Userinfodata.updateuser(user.id, currency=(added := playerdata[1]+(gamedataentery[1]/(len(self.playerids)-1))))
                await user.send(f'Your current game has been canceled by {Ender.name} you gained {added-playerdata[1]}')
                await df.dataref.CurrentGames.deleteplayer(user)
                continue
            df.dataref.Userinfodata.updateuser(user.id, currency=(lost := playerdata[1]-gamedataentery[1]))
            await user.send(f'You canceled your current game and you lost {gamedataentery[1]}')
            await df.dataref.CurrentGames.deleteplayer(user)

        df.dataref.CurrentGames.DeleteGame(key)

    async def nowinend(self):
        key = df.dataref.CurrentGames.gameplayers[self.playerids[0]]
        df.dataref.CurrentGames.DeleteGame(key)
        for user in self.userobjects:
            await user.send('No winner')
            await df.dataref.CurrentGames.deleteplayer(user)

    def getplayerid(self):
        return self.playerids[self.playerindex]

    def IncrasePlayerIndex(self, amount=1):
        if self.playerindex + amount < len(self.playerids):
            self.playerindex += amount
        else:
            self.playerindex = (amount - ((len(self.playerids)-1)-self.playerindex)) - 1

    def CreateEmbeded(self, embTitle, Desc, color, ImgName, Feilds):
        EmbededMes = Embed(
        title = embTitle,
        description = Desc,
        colour = Colour.from_rgb(*color)
        )
        Img = File(f'Images/TempPics/{ImgName}.png', filename='image.png')
        EmbededMes.set_image(url="attachment://image.png")
        for title, value in Feilds.items():
            EmbededMes.add_field(name=title, value=value)
        return EmbededMes, Img
