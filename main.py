from Refs.databaserefs import dataref
from discord.channel import DMChannel as dmchannelclass
from Games import GameUtil
from botclass import botgetclass
from re import findall
import functools
from datetime import datetime
from datetime import timedelta
from Refs.Queref import Qref
import os

bot = botgetclass.bot

#Makes instance of data base classes and clears the current games and requested games tables
RequestDataBase = dataref.RequestDataBase
CurrentGames = dataref.CurrentGames
Userinfodata = dataref.Userinfodata
MessageInfo = dataref.Messageinfo
RequestDataBase.cleartable()
CurrentGames.cleartable()
Qref.Quedata.cleartable()

def checkavalibility(func):
    @functools.wraps(func)
    async def check(Context, bet, ats):
        Opponents = [mention.id for mention in Context.message.mentions]
        playersinfo = Userinfodata.checkadduser(Opponents + [Context.author.id])
        if len(RequestDataBase.checkforentery(playerone=int(Context.author.id))) < 6:
            if GameUtil.GameUtilitys.checkplayercountwithcall(Context.message.content, len(Opponents) + 1):
                for player in playersinfo:
                    if player[0] in Qref.Quedata.quedplayers:
                        if len(Qref.Quedata.quedplayers[player[0]]) > 5:
                            await Context.send('A player you invited has the max amount of games qued')
                            return
                    if int(bet) > player[1] and 0 >= int(bet):
                        await Context.send('You dont have the right amount of money')
                        return
                return await func(Context, bet, ats)
            else:
                await Context.send('Too many players')
        else:
            await Context.send('you have to many requests')
    return check

@bot.command(name='battleship', help='Plays battle ship with @ed user')
@checkavalibility
async def PlayBattleShip(Context, bet, ats):
    await Context.message.add_reaction(u"\u2705")
    await RequestDataBase.addrequest(Context.message.id, 0, bet, Opponents, Context.message)

@bot.command(name='TicTacToe', help='Plays TicTacToe with @ed user')
@checkavalibility
async def TicTacToe(Context, bet, ats):
    await Context.message.add_reaction(u"\u2705")
    Opponents = [mention.id for mention in Context.message.mentions]
    MessageInfo.SendableMessages[Context.message.id] = RequestReaction
    await RequestDataBase.addrequest(Context.message.id, 1, bet, Context.author.id, Opponents, Context.message)

@bot.command(name='uno', help='Plays battle ship with @ed user')
@checkavalibility
async def uno(Context, bet, ats):
    await Context.message.add_reaction(u"\u2705")
    Opponents = [mention.id for mention in Context.message.mentions]
    MessageInfo.SendableMessages[Context.message.id] = RequestReaction
    await RequestDataBase.addrequest(Context.message.id, 2, bet, Context.author.id, Opponents, Context.message)

@bot.command(name='tournament', help='Creates a tournament with all players that react')
async def CreateTournament(Context, game, timetillstart, maxplayers, enteryfree, prizepool):
    pass

@bot.command(name='bal', help='Get balance of player')
async def checkbal(Context):
    #checks for player gets their table row and send back the currency column
    if (user := Userinfodata.checkforentery(user=Context.author.id)[0]):
        await Context.send(user[1])

@bot.command(name='daily', help='Adds daily money to account')
async def collectdaily(context):
    dailyWaitTime = 24
    user = Userinfodata.checkadduser([context.author.id])[0]
    if datetime.now() > (datetime.strptime(user[6], '%Y-%m-%d %H:%M:%S') + timedelta(hours=dailyWaitTime)):
        Userinfodata.updateuser(user[0], currency=(user[1]+(100+(100*user[5]))), dailystreak=(user[5]+1), lastdaily="""DATETIME('now', 'localtime')""")
        await context.send(f"Your new balance is {str(user[1]+(100+(100*user[5])))} you gained {str(100+(100*user[5]))} with a streak of {user[5] + 1} days")
        return
    elif datetime.now() > (datetime.strptime(user[6], '%Y-%m-%d %H:%M:%S') + timedelta(hours=(dailyWaitTime*2))):
        Userinfodata.updateuser(user[0], currency=user[1]+100, dailystreak=1, lastdaily="""DATETIME('now', 'localtime')""")
        await context.send(f"Your new balance is {str(user[1]+100)} you gained {str(100+(100*user[5]))} and you lost your daily streak")
        return
    await context.send(f"Please wait {str(datetime.strptime(user[6], '%Y-%m-%d %H:%M:%S') + timedelta(hours=dailyWaitTime) - datetime.now())[:-7]} hours")

@bot.command(name='pay', help='Pay another user money')
async def PayUser(Context, amount, recipient):
    amount = int(amount)
    users = Userinfodata.checkadduser([Context.author.id, Context.message.mentions[0].id])
    giver = users[0]
    reciver = users[1]
    if giver[1] >= amount and 0 < amount:
        Userinfodata.updateuser(giver[0], currency=(giver[1]-amount))
        Userinfodata.updateuser(reciver[0], currency=(reciver[1]+amount))
        await Context.send('Transaction Commplete')
        return
    await Context.send('You do not have enough money')

@bot.command(name='cancelrequests', help='Ends all users game request')
async def CancelAllRequests(Context):
    RequestDataBase.fullremove(playerone=Context.author.id)
    await Context.send('All requested games canceled')

@bot.command(name='cancelgame', help='Cancels current game and can be used in dm')
async def CancelCurrentGame(Context):
    if Context.author.id in CurrentGames.gameplayers:
        key = CurrentGames.gameplayers[Context.author.id]
        await CurrentGames.currentgameobjects[key].endgameshort(Context.author)
        return
    await Context.send('You are not in a game')

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return
    await MessageInfo.CheckMessage(reaction.message.id, reaction, user)

async def RequestReaction(reaction, user):
    #Changes request into game switching the information in the DataBases
    if (requestinfo := RequestDataBase.checkforentery(RequestMessageId=int(reaction.message.id))[0]):
        if RequestDataBase.addacceptingplayer(int(user.id), requestinfo[5]):
            await CurrentGames.addgame(RequestDataBase.requestedgameopponents[requestinfo[5]][0], requestinfo[2], requestinfo[3])
            #Does request checkforentery twice once in full remove
            RequestDataBase.fullremove(RequestMessageId=int(reaction.message.id))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if type(message.channel) == dmchannelclass:
        key = CurrentGames.gameplayers[message.author.id]
        await CurrentGames.currentgameobjects[key].handlenewmessage(message)
    await bot.process_commands(message)

def CheckForPlayer(playerid):
    #checks if palyer is in a game or has a request if they are or do it returns False
    if playerid in CurrentGames.gameplayers.keys():
        return False
    return True

def MakeAllNumbers(string):
    return int(''.join(findall('\d+', string)))

def checkmessage(message):
    pass

bot.run(os.environ.get('DiscordApiKey'))
