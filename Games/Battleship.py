import string
from Games.GameBaseClass import Game
class BattleShipGame(Game):
    def __init__(self, playerids, boardsize = [10, 10]):
        super().__init__(playerids)
        self.boardsize = boardsize
        self.board = self.MakeBoard()

    def MakeBoard(self):
        board = []
        board.append([' '] + list(string.ascii_lowercase[:self.boardsize[0]]))
        for rownumber in range(1,11):
            row = [str(rownumber)]
            for rowitem in range(1,11):
                row.append('o')
            board.append(row)
        return board


if __name__ == '__main__':
    a = BattleShipGame()
