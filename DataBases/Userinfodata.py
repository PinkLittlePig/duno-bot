from DataBases.DataBaseClass import Database
from datetime import datetime

class UserInfoDatabase(Database):
    """Stores information on users including currency, user ids, and items"""

    def __init__(self, tablename='UserInformation'):
        super().__init__(filename='UserInfo.db')
        self.tablename = tablename
        self.trycreatetable('user integer PRIMARY KEY, currency integer, itemkey integer, totalgamesplayed integer, wins integer, dailystreak integer, lastdaily TEXT')
        self.useritems = {}

    def cratestartinfo(self, id):
        return [id, 500, self.randomString(), 0, 0, 0, self.getdatetime("""DATETIME('now', 'localtime', '-1 day')""")]

    def updateuser(self, userid, **userchanges):
        changestatment = self.createquerysql(userchanges, connector=', ')
        self.data_navigatior.execute(f"""UPDATE {self.tablename} Set {changestatment} Where user={userid}""")
        self.data.commit()

    def checkadduser(self, userids):
        checkedandadded = []
        for id in userids:
            if not(founduser := self.checkforentery(user=id)[0]):
                itemkey = self.randomString()
                self.useritems[itemkey] = []
                new = self.cratestartinfo(id)
                self.addentery(*new)
                checkedandadded.append(new)
                continue
            checkedandadded.append(founduser)
        return checkedandadded

    def getitems(self, key):
        return self.useritems[key]
