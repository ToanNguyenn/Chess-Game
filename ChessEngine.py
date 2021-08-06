class GameState:
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
        self.whiteKingLocation = [7, 4]
        self.blackKingLocation = [0, 4]
        self.checkMate = False
        self.stateMate = False # King has no valid move but not in check
        self.enpassantPossible = ()

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #we can undo later
        self.whiteToMove = not self.whiteToMove #swap turn

        if move.pieceMoved == "wK": #tracking king location
            self.whiteKingLocation = (move.endRow,move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow,move.endCol)

        #Pawn promotion to Queen
        if move.isPawnpromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"

        #En passant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--" # xóa vị trí tốt bị bắt qua đường
            print("sdgfbgdfgdtfghftghdfb")

        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()

    def Undo(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

        #update King position
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.startRow, move.startCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.startRow, move.startCol)

        #undo en passant
        if move.isEnpassantMove:
            self.board[move.endRow][move.endCol] = "--" # trả vị trí bắt tốt về trống
            self.board[move.startRow][move.endCol] = move.pieceCaptured # trả vị trí tốt bị bắt về lại tốt
            self.enpassantPossible = (move.endRow,move.endCol) # trả lại vị trí en passant có thể bắt

        # undo 2 square pawn back
        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endCol) == 2:
            self.enpassantPossible = ()

    def getValidMoves(self):
        tempEnpassant = self.enpassantPossible
        #1) generate all possible moves
        moves = self.getAllValidMoves()
        #2) make move for each move
        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove #check enemy move
        #3) generate all enemy's moves
        #4) see if enemy can attack king
            if self.InCheck():
                moves.remove(moves[i])#5) if king can be attack ==> not a valid move
            self.whiteToMove = not self.whiteToMove
            self.Undo()

        if len(moves) == 0:
            if self.InCheck():
                self.checkMate = True
                print("Check Mate")
            else:
                self.stateMate = True
                print("State Mate")
        else:
            self.checkMate = False
            self.stateMate = False

        self.enpassantPossible = tempEnpassant #Khi makemode sẽ không thay đổi  vị trí pawn trước khi en passant
        return moves

    def InCheck(self):
        if self.whiteToMove:
            return self.sqUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.sqUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def sqUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch turn
        enemyMove = self.getAllValidMoves()
        self.whiteToMove = not self.whiteToMove #check if next turn can enemy attack king
        for move in enemyMove:
            if move.endRow == r and move.endCol == c:
                return True
        return False

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
        if self.whiteToMove:
            if self.board[r-1][c] == '--':
                moves.append(Move((r,c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == '--':
                    moves.append(Move((r,c), (r-2,c), self.board))

            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, isEnpassantMove=True))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, isEnpassantMove=True))

        else:
            if self.board[r+1][c] == '--':
                moves.append(Move((r, c), (r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == '--':
                    moves.append(Move((r, c), (r+2, c), self.board))

            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, isEnpassantMove=True))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, isEnpassantMove=True))

    def getRookMoves(self, r, c, moves):
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        enemy = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endCol < 8 and 0 <= endRow < 8: #onboard
                    endPieces = self.board[endRow][endCol]
                    if endPieces == "--": # if no piece
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPieces[0] == enemy: # if enemy piece
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # if friend piece
                        break
                else:   #out board
                    break

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endCol < 8 and 0 <= endRow < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKingMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally = "w" if self.whiteToMove else "b"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endCol < 8 and 0 <= endRow < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKnightMoves(self, r, c, moves):
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),(1, -2), (1, 2), (2, -1), (2, 1))
        ally = "w" if self.whiteToMove else "b"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endCol < 8 and 0 <= endRow < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


class Move:
    # maps key to value
    # key : value
    rankstoRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowstoRanks = {v: k for k, v in rankstoRows.items()}
    filestoCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colstoFiles = {v: k for k, v in filestoCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        #Pawn promotion
        self.isPawnpromotion = False
        if (self.pieceMoved == "wp" and self.endRow == 0) or  (self.pieceMoved == "bp" and self.endRow == 7):
            self.isPawnpromotion = True

        #En Passant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"

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