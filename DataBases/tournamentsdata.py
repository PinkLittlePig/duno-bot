#one data base each tournament is a tabel with dictionary keeping track of there propertys
#change table name of classs when operating on different tournaments
# For V3
from DataBases.DataBaseClass import Database
class tournamentdatabase(object):
    """docstring for ."""

    def __init__(self, arg):
        self.data = sqlite3.connect('AllTournamentData.db')
        self.data_navigatior = self.data.cursor()
        self.tablename
        self.tournamenttables = {}

    def addtournament(self, allplayers):
        self.tablename = self.randomString()
        self.trycreatetable("""""")
