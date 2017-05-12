class GameBoard():
    def __init__(self, size_x, size_y):
        self.size = (size_x, size_y)
        self.stones = []
        self.BlackStones = []
        self.WhiteStones = []
        self.Moves = 0

    def AddStone(self, StoneType, Position): # Position: (x,y) tuple
        if StoneType == "black":
            self.BlackStones.append(Position)
        elif StoneType == "white":
            self.WhiteStones.append(Position)

        self.Moves += 1


class AICore():
    def __init__(self, Board: object = None, PlyDepth: object = 4, AIStoneType: object = "white") -> object:
        if not Board:
            self.Board = GameBoard(14, 14)
            self.CustomBoard = False
        else:
            self.Board = Board
            self.CustomBoard = True

        self.PlyDepth = PlyDepth
        self.AIStoneType = AIStoneType
        self.StartAI()

    def ReadCustomBoard(self):
        if len(self.Board.BlackStones) == len(self.Board.WhiteStones):
            self.turn = "black"
        elif len(self.Board.BlackStones) > len(self.Board.WhietStones):
            self.turn = "white"

    def StartAI(self):
        if self.AIStoneType == "black":
            self.Board.AddStone(self.AIStoneType, (int(self.Board.size[0] / 2), int(self.Board.size[1] / 2)))

    def GenerateGameState(self):
        Stones = {}
        BlackStones = [x for x in self.Board.BlackStones]
        WhiteStones = [x for x in self.Board.WhiteStones]
        Stones["black"] = BlackStones
        Stones["white"] = WhiteStones
        return Stones

    def GenerateCustomGameState(self, GameState, Position, StoneType):
        Stones = {}
        BlackStones = [x for x in GameState["black"]]
        WhiteStones = [x for x in GameState["white"]]
        Stones["black"] = BlackStones
        Stones["white"] = WhiteStones
        Stones[StoneType].append(Position)
        return Stones

    def GetOpenMoves(self, GameState):
        OpenMoves = []
        for x in range(1, self.Board.size[0] + 1):
            for y in range(1, self.Board.size[1] + 1):
                if (x, y) in GameState["black"] or (x, y) in GameState["white"]:
                    pass
                else:
                    OpenMoves.append((x, y))
        return OpenMoves

    def AddHumanStone(self, Position):
        self.Board.AddStone("white" if self.AIStoneType == "black" else "black", Position)
        print("ADDED HUMAN STONE AT", Position, ",type is ", "white" if self.AIStoneType == "black" else "black")
        self.Choose_Move(self.GenerateGameState(), True)

    def AddAIStone(self, Position):
        self.Board.AddStone(self.AIStoneType, Position)

    def Choose_Move(self, GameState, MaximizingTurn):
        print("THE COMPUTER IS CHOOSING")
        depth = self.PlyDepth
        bestmove = self.MINIMAX(GameState, depth, True)
        self.AddAIStone(bestmove)
        print("THE COMPUTER DECIDED TO ADD A STONE TO ", bestmove[1])

    def MINIMAX(self, GameState, depth, MaximizingTurn):
        if depth == 0:
            return (self.Heuristics(GameState), "null")

        print("-------------")
        print(GameState)
        if MaximizingTurn:
            childvalues = []
            for moves in self.GetOpenMoves(GameState):
                heuristics = self.MINIMAX(self.GenerateCustomGameState(GameState, moves, "black" if self.AIStoneType == "white" else "white"), depth - 1, False)[0]
                print(heuristics, depth)
                childvalues.append((heuristics, moves))

            childvalues = sorted(childvalues, key=lambda x: x[0], reverse=True)
            print(childvalues[0])[0]
            return childvalues[0]
        elif not MaximizingTurn:
            childvalues = []
            for moves in self.GetOpenMoves(GameState):
                heuristics = self.MINIMAX(self.GenerateCustomGameState(GameState, moves, self.AIStoneType), depth - 1, True)[0]
                print(heuristics, depth)
                childvalues.append((heuristics, moves))

            childvalues = sorted(childvalues, key=lambda x: x[0])
            print(childvalues[0])[0]
            return childvalues
        """for moves in self.GetOpenMoves(GameState):
            heuristics = self.MINIMAX(self.GenerateCustomGameState(GameState,moves,"black" if self.AIStoneType == "white" else "white"),depth-1,False if MaximizingTurn else True)
            childvalues.append((heuristics,moves))

        print(depth,MaximizingTurn)
        if MaximizingTurn:
            childvalues = sorted(childvalues,key=lambda x:x[0],reverse=True)
            print("Sorted Moves using heuristics",childvalues)
            return childvalues[0][1]
        elif not MaximizingTurn:
            childvalues = sorted(childvalues,key=lambda x:x[0])
            print(childvalues)
            return childvalues[0][1]"""

    def Heuristics(self, GameState):
        " ooo  "  # 4
        "o oo "  # 4
        "oo   "  # 2
        "ooooo"  # 10000

        "xoooo"  # 8
        "oooo "  # 50
        return 12


def GetDefaultTemplate():
    template = {
        "ooooo": 100000,
        "oooo ": 90,
        "xoooo": 60,
        "ooo  ": 40,
        "o oo ": 40,
        " oo  ": 20,
        "o o  ": 20
    }
    case_open_3s = [
        "01110",
        "010110",
        "011010"
    ]
    return template


class Analyzer():
    def __init__(self, Board, template=None):
        self.Board = Board
        if not template:
            self.template = GetDefaultTemplate()
        else:
            self.template = template

    def ThreatSpaceSearch(self):
        pass
    def Analyze(self, StoneType):
        PassedStones = []
        Open3 = 0
        BlackStones = self.Board.BlackStones
        WhiteStones = self.Board.WhiteStones
        if StoneType == "black":
            for y in range(1, self.Board.size[1] + 1):
                for x in range(1, self.Board.size[0] + 1):
                    if not (x, y) in PassedStones:
                        if (x, y) in BlackStones:
                            pass
        """PassedStones = []
        BlackStones = self.Board.BlackStones
        WhiteStones = self.Board.WhiteStones
        if StoneType == "black":
            for y in range(1, self.Board.size[1] + 1):
                for x in range(1,self.Board.size[0]+1):
                    if (x,y) in BlackStones:
                        neighborpos = {}
                        neighbors = self.get_8(stones)

                        """

    def get_8(self, Position):
        data = []
        for x, y in [(Position[0] + i, Position[1] + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0]:
            if x > self.Board.size[0] or x < 0 or y > self.Board.size[1] or y < 0:
                pass
            else:
                data.append((x, y))
        return data

if __name__ == "__main__":
    ai = AICore()
    # ai.AddHumanStone((7,7))
    ai.Board.AddStone("black", (7, 7))
    ai.Board.AddStone("black", (7, 8))
    ai.Board.AddStone("black", (6, 7))
    ai.Board.AddStone("white", (7, 6))
    print(ai.Board.BlackStones)
    heuristics = Analyzer(ai.Board)
    print(heuristics.Analyze("black"))