from DataBases.Requestdata import RequestedDatabase
from DataBases.Currentgamedata import CurrentGameDatabase
from DataBases.Userinfodata import UserInfoDatabase
from DataBases.MessageInfo import MessagesPlace


class dataref:
    RequestDataBase = RequestedDatabase()
    CurrentGames = CurrentGameDatabase()
    Userinfodata = UserInfoDatabase()
    Messageinfo = MessagesPlace()
