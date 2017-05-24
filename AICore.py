from main import GameBoard
from Analyzer import Analyzer


class AICore():
    def __init__(self, board=None, aistoneType="white"):
        if not board:
            self.Board = GameBoard(13, 13)
            self.CustomBoard = False
        else:
            self.Board = board
            self.CustomBoard = True

        self.AIStoneType = aistoneType



    def GenerateCustomGameBoard(self, GameState, Position, StoneType):
        """Generates a custom GameBoard class, merging the previous GameState GameBoard and a new stone type StoneType on position Position"""
        Stones = {}
        BlackStones = [x for x in GameState.BlackStones]
        WhiteStones = [x for x in GameState.WhiteStones]
        Stones["black"] = BlackStones
        Stones["white"] = WhiteStones
        Stones[StoneType].append(Position)
        board = GameBoard(self.Board.size[0], self.Board.size[1])
        board.WhiteStones = Stones["white"]
        board.BlackStones = Stones["black"]
        board.Moves = len(Stones["black"])+len(Stones["white"])
        return board

    def GetOpenMoves(self, GameState):
        """Returns all available unoccupied positions in the board"""
        OpenMoves = []
        for x in range(1, GameState.size[0] + 1):
            for y in range(1, GameState.size[1] + 1):
                if (x, y) in GameState.BlackStones or (x, y) in GameState.WhiteStones:
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


class AlphaBeta(AICore):
    def __init__(self, board=None, aistoneType="white",plydepth=10,threads=1):
        self.PlyDepth = plydepth
        self.threads = threads
        AICore.__init__(self,board,aistoneType)
        if self.AIStoneType == "black":
            self.AddAIStone((round(self.Board.size[0]/2),round(self.Board.size[1]/2)))

    def ChooseMove(self):
        avaliablemoves = {}
        for moves in self.GetOpenMoves(self.Board):
            movevalue = self.AlPhaBeta(self.Board,self.PlyDepth,-1000000,1000000,True)
            avaliablemoves[moves] = movevalue
        bestvalue = 0
        bestpos = ()
        for key in avaliablemoves.keys():
            if avaliablemoves[key] > bestvalue:
                bestvalue = avaliablemoves[key]
                bestpos = key
        print("reached")
        self.AddAIStone(bestpos)

    def AlPhaBeta(self,GameState,depth,a,b,IsMaximizingTurn):
        enemystonetype = "white" if self.AIStoneType == "black" else "white"
        if depth == 0:
            return Analyzer(GameState).Grader(self.AIStoneType if IsMaximizingTurn else enemystonetype)
        if IsMaximizingTurn:
            v = -1000000
            for paths in self.GetOpenMoves(GameState):
                v = max(v,self.AlPhaBeta(self.GenerateCustomGameBoard(GameState,paths,enemystonetype),depth-1,a,b,False))
                a = max(a,v)
                if b <= a:
                    break
            return v
        else:
            v = 1000000
            for paths in self.GetOpenMoves(GameState):
                v = min(v,self.AlPhaBeta(self.GenerateCustomGameBoard(GameState,paths,self.AIStoneType),depth-1,a,b,True))
                b = min(b,v)
                if b <= a:
                    break
            return v

if __name__ == "__main__":
    board = GameBoard(3,3)
    ai = AlphaBeta(board,plydepth=3)
    ai.AddHumanStone((3,3))
    ai.ChooseMove()