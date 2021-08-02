class GameState():
    def __init__(self):
        # 8x8 board 2d list, 2 characters for each element
        # 1st character is color
        # 2nd character is type of the piece
        # "--" represents an empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.moveFunctions = {'p': self.getPawnMoves, 'B': self.getBishopMoves, 'R': self.getRookMoves,
                              'K': self.getKingMoves, 'Q': self.getQueenMoves, 'N': self.getKnightMoves}
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #we can undo later
        self.whiteToMove = not self.whiteToMove #swap turn

    def Undo(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getAllValidMoves()

    def getAllValidMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len((self.board[r]))):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  #calls function for each pieces
        return moves

    def getPawnMoves(self, r, c, moves):
        pass

    def getRookMoves(self, r, c, moves):
        pass

    def getBishopMoves(self, r, c, moves):
        pass

    def getKingMoves(self, r, c, moves):
        pass

    def getQueenMoves(self, r, c, moves):
        pass

    def getKnightMoves(self, r, c, moves):
        pass

class Move:
    # maps key to value
    # key : value
    rankstoRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowstoRanks = {v: k for k, v in rankstoRows.items()}
    filestoCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colstoFiles = {v: k for k, v in filestoCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.MoveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
        print(self.MoveID)
    '''
    Overriding the oquals method'''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.MoveID == other.MoveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colstoFiles[c] + self.rowstoRanks[r]