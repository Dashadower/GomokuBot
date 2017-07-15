from main import GameBoard
from Analyzer import Heuristics, WinChecker, AdvancedAnalyzer
from FilterStrings import Open2, Open3, Open4, Open5, Closed4
from copy import deepcopy
class AICore():
    def __init__(self, board=None, aistoneType="white",searchrange=1):
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
        board = GameBoard(GameState.size[0], GameState.size[1])
        for stone in GameState.BlackStones:
            board.AddStone("black",stone)
        for stone in GameState.WhiteStones:
            board.AddStone("white",stone)
        board.AddStone(StoneType,Position)
        return board # standard iteration is proved to be faster
        """board = deepcopy(GameState) 
        board.AddStone(StoneType,Position)
        return board"""

    def DuplicateBoard(self, Board):
        g = GameBoard(Board.size[0], Board.size[1])

        for x in Board.WhiteStones:
            g.AddStone("white", x)
        for y in Board.BlackStones:
            g.AddStone("black", y)
        return g
        # return deepcopy(Board) # standard iteration is proven to be faster

    def GetOpenMovesPlus(self,board,searchrange):
        """Returns available unoccupied positions  within a square of the outermost stones + range
        Used to reduce number of simulations"""


        OpenMoves = []


        for stones in board.stones:
            #for x, y in [(stones[0] + i, stones[1] + j) for i in (-2,-1, 0, 1,2) for j in (-2,-1, 0, 1,2) if i != 0 or j != 0]:
            for x, y in [(stones[0] + i, stones[1] + j) for i in range(-searchrange,searchrange+1) for j in range(-searchrange,searchrange+1) if i != 0 or j != 0]:
                if x > board.size[0] or x <= 0 or y > board.size[1] or y <= 0:
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
                    elif pattern[0] == Closed4[2] or pattern[0] == Closed4[5] or pattern[0] == Closed4[7]:
                        return (pattern[1][0],pattern[1][1]+2)
                    elif pattern[0] == Closed4[4] or pattern[0] == Closed4[6]:
                        return (pattern[1][0],pattern[1][1]+1)
                    elif pattern[0] == Closed4[8]:
                        return ((pattern[1][0],pattern[1][1]+3))
                elif pattern[2] == "hori":
                    if pattern[0] == Closed4[0] or pattern[0] == Closed4[3]:
                        return (pattern[1][0]+4,pattern[1][1])
                    elif pattern[0] == Closed4[1]:
                        return (pattern[1][0]-1,pattern[1][1])
                    elif pattern[0] == Closed4[2] or pattern[0] == Closed4[5] or pattern[0] == Closed4[7]:
                        return (pattern[1][0]+2,pattern[1][1])
                    elif pattern[0] == Closed4[4] or pattern[0] == Closed4[6]:
                        return (pattern[1][0]+1,pattern[1][1])
                    elif pattern[0] == Closed4[8]:
                        return (pattern[1][0]+3, pattern[1][1])
                elif pattern[2] == "diag2":
                    if pattern[0] == Closed4[0] or pattern[0] == Closed4[3]:
                        return (pattern[1][0]+4,pattern[1][1]+4)
                    elif pattern[0] == Closed4[1]:
                        return (pattern[1][0]-1,pattern[1][1]-1)
                    elif pattern[0] == Closed4[2] or pattern[0] == Closed4[5] or pattern[0] == Closed4[7]:
                        return (pattern[1][0]+2,pattern[1][1]+2)
                    elif pattern[0] == Closed4[4] or pattern[0] == Closed4[6]:
                        return (pattern[1][0]+1,pattern[1][1]+1)
                    elif pattern[0] == Closed4[8]:
                        return (pattern[1][0]+3,pattern[1][1]+3)
                elif pattern[2] == "diag5":
                    if pattern[0] == Closed4[0] or pattern[0] == Closed4[3]:
                        return (pattern[1][0]+4,pattern[1][1]-4)
                    elif pattern[0] == Closed4[1]:
                        return (pattern[1][0]-1,pattern[1][1]+1)
                    elif pattern[0] == Closed4[2] or pattern[0] == Closed4[5] or pattern[0] == Closed4[7]:
                        return (pattern[1][0]+2,pattern[1][1]-2)
                    elif pattern[0] == Closed4[4] or pattern[0] == Closed4[6]:
                        return (pattern[1][0]+1,pattern[1][1]-1)
                    elif pattern[0] == Closed4[8]:
                        return (pattern[1][0]+3,pattern[1][1]-3)
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
                    elif pattern[0] == Closed4[2] or pattern[0] == Closed4[5] or pattern[0] == Closed4[7]:
                        return (pattern[1][0],pattern[1][1]+2)
                    elif pattern[0] == Closed4[4] or pattern[0] == Closed4[6]:
                        return (pattern[1][0],pattern[1][1]+1)
                    elif pattern[0] == Closed4[8]:
                        return ((pattern[1][0],pattern[1][1]+3))
                elif pattern[2] == "hori":
                    if pattern[0] == Closed4[0] or pattern[0] == Closed4[3]:
                        return (pattern[1][0]+4,pattern[1][1])
                    elif pattern[0] == Closed4[1]:
                        return (pattern[1][0]-1,pattern[1][1])
                    elif pattern[0] == Closed4[2] or pattern[0] == Closed4[5] or pattern[0] == Closed4[7]:
                        return (pattern[1][0]+2,pattern[1][1])
                    elif pattern[0] == Closed4[4] or pattern[0] == Closed4[6]:
                        return (pattern[1][0]+1,pattern[1][1])
                    elif pattern[0] == Closed4[8]:
                        return (pattern[1][0]+3, pattern[1][1])
                elif pattern[2] == "diag2":
                    if pattern[0] == Closed4[0] or pattern[0] == Closed4[3]:
                        return (pattern[1][0]+4,pattern[1][1]+4)
                    elif pattern[0] == Closed4[1]:
                        return (pattern[1][0]-1,pattern[1][1]-1)
                    elif pattern[0] == Closed4[2] or pattern[0] == Closed4[5] or pattern[0] == Closed4[7]:
                        return (pattern[1][0]+2,pattern[1][1]+2)
                    elif pattern[0] == Closed4[4] or pattern[0] == Closed4[6]:
                        return (pattern[1][0]+1,pattern[1][1]+1)
                    elif pattern[0] == Closed4[8]:
                        return (pattern[1][0]+3,pattern[1][1]+3)
                elif pattern[2] == "diag5":
                    if pattern[0] == Closed4[0] or pattern[0] == Closed4[3]:
                        return (pattern[1][0]+4,pattern[1][1]-4)
                    elif pattern[0] == Closed4[1]:
                        return (pattern[1][0]-1,pattern[1][1]+1)
                    elif pattern[0] == Closed4[2] or pattern[0] == Closed4[5] or pattern[0] == Closed4[7]:
                        return (pattern[1][0]+2,pattern[1][1]-2)
                    elif pattern[0] == Closed4[4] or pattern[0] == Closed4[6]:
                        return (pattern[1][0]+1,pattern[1][1]-1)
                    elif pattern[0] == Closed4[8]:
                        return (pattern[1][0]+3,pattern[1][1]-3)


if __name__ == "__main__":
    board = GameBoard(5, 5)
    board.AddStone("black", (3, 3))
    board.AddStone("black", (3, 4))
    ai = AICore(board)
    print(ai.GetOpenMovesPlus(board,1))