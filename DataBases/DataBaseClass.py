import sqlite3
from string import ascii_letters
from random import choice, randint
from datetime import datetime
from datetime import timedelta
from re import findall

class Database:
    def __init__(self, filename):
        self.data = sqlite3.connect(filename)
        self.data_navigatior = self.data.cursor()

    def trycreatetable(self, tablecolumns):
        try:
            self.data.execute(f"""CREATE TABLE {self.tablename} ({tablecolumns});""")
            return True
        except:
            return False

    def addentery(self, *querys):
        querys = list(map(str, querys))
        querys = self.addquote(querys)
        self.data_navigatior.execute(f"""INSERT INTO {self.tablename} VALUES({', '.join(querys)});""")
        self.data.commit()

    def readallenterys(self):
        self.data_navigatior.execute(f"""SELECT * FROM {self.tablename};""")
        allrequests = self.data_navigatior.fetchall()
        return allrequests

    def checkforentery(self, **querys):
        WhereStatment = self.createquerysql(querys)
        self.data_navigatior.execute(f"""SELECT * FROM {self.tablename} WHERE {WhereStatment};""") #  AND game={str(game)};
        request = self.data_navigatior.fetchall()
        if len(request):
            return request
        else:
            return [[]]

    def removeentery(self, **querys):
        WhereStatment = self.createquerysql(querys)
        self.data_navigatior.execute(f"""DELETE FROM {self.tablename} WHERE {WhereStatment};""")
        self.data.commit()

    def createquerysql(self, queryitems, connector = ' AND '):
        query = ''
        for keyword, keyvalue in queryitems.items():
            query += str(keyword) + '=' + str(keyvalue) + connector
        return query[:-len(connector)]

    def cleartable(self):
        self.data_navigatior.execute(f"""DELETE FROM {self.tablename};""")
        self.data.commit()

    def randomString(self, charactertype=0, Length=24):
        if charactertype:
            return ''.join(choice(ascii_letters) for i in range(Length))
        else:
            return randint(0, 100000000000)

    def getdatetime(self, datetime):
        self.data_navigatior.execute(f"""SELECT {datetime}""")
        return self.data_navigatior.fetchall()[0][0]

    def addquote(self, querylist):
        for str in range(len(querylist)):
            try:
                int(querylist[str])
            except:
                querylist[str] = f"'{querylist[str]}'"
        return querylist
