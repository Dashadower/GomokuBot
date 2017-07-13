from main import GameBoard
from Analyzer import Heuristics, WinChecker, AdvancedAnalyzer
from FilterStrings import Open2, Open3, Open4, Open5, Closed4

class AICore():
    def __init__(self, board=None, aistoneType="white",searchrange=4):
        if not board:
            self.Board = GameBoard(13, 13)
            self.CustomBoard = False
        else:
            self.Board = board
            self.CustomBoard = True
        self.SearchRange = searchrange
        self.AIStoneType = aistoneType



    def GenerateCustomGameBoard(self, GameState, Position, StoneType):
        """Generates a custom GameBoard class, merging the previous GameState GameBoard and a new stone type StoneType on position Position"""
        Stones = {}
        BlackStones = [x for x in GameState.BlackStones]
        WhiteStones = [x for x in GameState.WhiteStones]
        Stones["black"] = BlackStones
        Stones["white"] = WhiteStones
        Stones[StoneType].append(Position)
        board = GameBoard(GameState.size[0], GameState.size[1])
        for stone in Stones["black"]:
            board.AddStone("black",stone)
        for stone in Stones["white"]:
            board.AddStone("white",stone)
        if len(board.BlackStones) > len(board.WhiteStones):
            board.turn = "white"
        else:
            board.turn = "black"
        return board

    def DuplicateBoard(self, Board):
        g = GameBoard(Board.size[0], Board.size[1])

        for x in Board.WhiteStones:
            g.AddStone("white", x)
        for y in Board.BlackStones:
            g.AddStone("black", y)
        return g


    def GetOpenMovesPlus(self,board):
        """Returns available unoccupied positions  within a square of the outermost stones + range
        Used to reduce number of simulations"""

        low = [board.size[0],board.size[1]]
        high = [1,1]
        OpenMoves = []

        """for stone in board.stones:

            if stone[0] < low[0]:
                low[0] = stone[0]
            if stone[0] > high[0]:
                high[0] = stone[0]
            if stone[1] < low[1]:
                low[1] = stone[1]
            if stone[1] > high[1]:
                high[1] = stone[1]
        if low[0] > self.SearchRange:
            low[0] -= self.SearchRange
        else:
            low[0] = 1
        if low[1] > self.SearchRange:
            low[1] -= self.SearchRange
        else:
            low[1] = 1
        if high[0] < board.size[0]-self.SearchRange:
            high[0] += self.SearchRange
        else:
            high[0] = board.size[0]
        if high[1] < board.size[1]-self.SearchRange:
            high[1] += self.SearchRange
        else:
            high[1] = board.size[1]


        for x in range(low[0],high[0]+1):
            for y in range(low[1],high[1]+1):
                if (x,y) in board.BlackStones or (x,y) in board.WhiteStones:
                    pass
                else:
                    OpenMoves.append((x, y))"""
        for stones in board.stones:
            #for x, y in [(stones[0] + i, stones[1] + j) for i in (-2,-1, 0, 1,2) for j in (-2,-1, 0, 1,2) if i != 0 or j != 0]:
            for x, y in [(stones[0] + i, stones[1] + j) for i in range(-self.SearchRange,self.SearchRange+1) for j in range(-self.SearchRange,self.SearchRange+1) if i != 0 or j != 0]:
                if x > self.Board.size[0] or x < 0 or y > self.Board.size[1] or y < 0:
                    pass
                else:
                    if (x,y) not in board.stones:
                        OpenMoves.append((x, y))
        setted = set(OpenMoves)
        return list(setted)

    def GetOpenMoves(self, GameState):
        """Returns all available unoccupied positions in the board"""
        OpenMoves = []
        for x in range(1, GameState.size[0] + 1):
            for y in range(1, GameState.size[1] + 1):
                if (x,y) in GameState.BlackStones or (x,y) in GameState.WhiteStones:
                    pass
                else:
                    OpenMoves.append((x, y))
        return OpenMoves

    def AddHumanStone(self, Position):
        """Updates self.Board by adding a stone to the human stone type"""
        self.Board.AddStone("white" if self.AIStoneType == "black" else "black", Position)
        print("ADDED HUMAN STONE AT", Position, ",type is ", "white" if self.AIStoneType == "black" else "black")

    def AddAIStone(self, Position):
        """updates self.Board by adding a stone to the AI stone type"""
        self.Board.AddStone(self.AIStoneType, Position)
        print("ADDED AI STONE AT",Position,"type is ",self.AIStoneType)

class ThreatSpaceSearch():
    def __init__(self,board,aistonetype):
        self.board = board
        self.aistonetype = aistonetype
        self.enemystonetype = "white" if self.aistonetype == "black" else "black"
        self.analyzer = AdvancedAnalyzer(self.board)
    def Check(self):
        current_ai_threats = self.analyzer.Parser(self.aistonetype) #format: (pattern,pos,direction)
        current_enemy_threats = self.analyzer.Parser(self.enemystonetype)
        for pattern in current_ai_threats: # (pattern[1][0],pattern[1][1])
            if pattern[0] in Open4:
                if pattern[2] == "vert":
                    if (pattern[1][0],pattern[1][1]-1) not in self.board.stones:
                        return (pattern[1][0],pattern[1][1]-1)
                    else:
                        return (pattern[1][0], pattern[1][1]+4)
                elif pattern[2] == "hori":
                    if (pattern[1][0]-1, pattern[1][1]) not in self.board.stones:
                        return (pattern[1][0]-1, pattern[1][1])
                    else:
                        return (pattern[1][0]+4, pattern[1][1])
                elif pattern[2] == "diag2":
                    if(pattern[1][0] - 1, pattern[1][1]-1) not in self.board.stones:
                        return (pattern[1][0] - 1, pattern[1][1]-1)
                    else:
                        return (pattern[1][0] + 4, pattern[1][1]+4)
                elif pattern[2] == "diag5":
                    if(pattern[1][0] - 1, pattern[1][1]+1) not in self.board.stones:
                        return (pattern[1][0] - 1, pattern[1][1]+1)
                    else:
                        return (pattern[1][0] + 4, pattern[1][1]-4)
            elif pattern[0] in Closed4:
                if pattern[2] == "vert":
                    if pattern[0] == Closed4[0] or pattern[0] == Closed4[3]:
                        return (pattern[1][0],pattern[1][1]+4)
                    elif pattern[0] == Closed4[1]:
                        return (pattern[1][0],pattern[1][1]-1)
                    elif pattern[0] == Closed4[2]:
                        return (pattern[1][0],pattern[1][1]+2)
                elif pattern[2] == "hori":
                    if pattern[0] == Closed4[0] or pattern[0] == Closed4[3]:
                        return (pattern[1][0]+4,pattern[1][1])
                    elif pattern[0] == Closed4[1]:
                        return (pattern[1][0]-1,pattern[1][1])
                    elif pattern[0] == Closed4[2]:
                        return (pattern[1][0]+2,pattern[1][1])
                elif pattern[2] == "diag2":
                    if pattern[0] == Closed4[0] or pattern[0] == Closed4[3]:
                        return (pattern[1][0]+4,pattern[1][1]+4)
                    elif pattern[0] == Closed4[1]:
                        return (pattern[1][0]-1,pattern[1][1]-1)
                    elif pattern[0] == Closed4[2]:
                        return (pattern[1][0]+2,pattern[1][1]+2)
                elif pattern[2] == "diag5":
                    if pattern[0] == Closed4[0] or pattern[0] == Closed4[3]:
                        return (pattern[1][0]+4,pattern[1][1]-4)
                    elif pattern[0] == Closed4[1]:
                        return (pattern[1][0]-1,pattern[1][1]+1)
                    elif pattern[0] == Closed4[2]:
                        return (pattern[1][0]+2,pattern[1][1]-2)
        for pattern in current_enemy_threats:
            if pattern[0] in Open4:
                if pattern[2] == "vert":
                    if (pattern[1][0],pattern[1][1]-1) not in self.board.stones:
                        return (pattern[1][0],pattern[1][1]-1)
                    else:
                        return (pattern[1][0], pattern[1][1]+4)
                elif pattern[2] == "hori":
                    if (pattern[1][0]-1, pattern[1][1]) not in self.board.stones:
                        return (pattern[1][0]-1, pattern[1][1])
                    else:
                        return (pattern[1][0]+4, pattern[1][1])
                elif pattern[2] == "diag2":
                    if(pattern[1][0] - 1, pattern[1][1]-1) not in self.board.stones:
                        return (pattern[1][0] - 1, pattern[1][1]-1)
                    else:
                        return (pattern[1][0] + 4, pattern[1][1]+4)
                elif pattern[2] == "diag5":
                    if(pattern[1][0] - 1, pattern[1][1]+1) not in self.board.stones:
                        return (pattern[1][0] - 1, pattern[1][1]+1)
                    else:
                        return (pattern[1][0] + 4, pattern[1][1]-4)
            elif pattern[0] in Closed4:
                if pattern[2] == "vert":
                    if pattern[0] == Closed4[0] or pattern[0] == Closed4[3]:
                        return (pattern[1][0],pattern[1][1]+4)
                    elif pattern[0] == Closed4[1]:
                        return (pattern[1][0],pattern[1][1]-1)
                    elif pattern[0] == Closed4[2]:
                        return (pattern[1][0],pattern[1][1]+2)
                elif pattern[2] == "hori":
                    if pattern[0] == Closed4[0] or pattern[0] == Closed4[3]:
                        return (pattern[1][0]+4,pattern[1][1])
                    elif pattern[0] == Closed4[1]:
                        return (pattern[1][0]-1,pattern[1][1])
                    elif pattern[0] == Closed4[2]:
                        return (pattern[1][0]+2,pattern[1][1])
                elif pattern[2] == "diag2":
                    if pattern[0] == Closed4[0] or pattern[0] == Closed4[3]:
                        return (pattern[1][0]+4,pattern[1][1]+4)
                    elif pattern[0] == Closed4[1]:
                        return (pattern[1][0]-1,pattern[1][1]-1)
                    elif pattern[0] == Closed4[2]:
                        return (pattern[1][0]+2,pattern[1][1]+2)
                elif pattern[2] == "diag5":
                    if pattern[0] == Closed4[0] or pattern[0] == Closed4[3]:
                        return (pattern[1][0]+4,pattern[1][1]-4)
                    elif pattern[0] == Closed4[1]:
                        return (pattern[1][0]-1,pattern[1][1]+1)
                    elif pattern[0] == Closed4[2]:
                        return (pattern[1][0]+2,pattern[1][1]-2)


if __name__ == "__main__":
    pass