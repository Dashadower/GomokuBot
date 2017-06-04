from AICore import AICore
from Analyzer import WinChecker
import threading, math, time,random, queue
from main import GameBoard
"""THREAD PROTOCOL
1.THREAD CREATION move,GameState,ReportQueue,AIStoneType,searchrange,TimeLimit=10,GameLimit=None: 
    Thread creation is explicitly done within the MonteCarlo class. no protocols
    move: current move being evaluated
    GameState: GameBoard object WITH move inserted
    ReportQueue: Queue in which RESULT are sent
    AIStoneType: -
    searchrange: smart open move searcher range
    timelimit: thread simulation time limit
    gamelimit: thread simulation max number of games
2. RESULT
    The following tuple format is put into ReportQueue:
    (move,totalsims,wins)
    move: move simulated
    totalsims: total number of simulations done on thread
    wins: total number of AIStoneType WINNING simulations"""

class MonteCarlo(AICore):
    def __init__(self, board=None, reportui=None, aistoneType="white",searchrange=4, TimeLimit=10):
        AICore.__init__(self, board, aistoneType)
        self.TimeLimit = TimeLimit

        self.ReportUI = reportui
        self.SearchRange = searchrange
        if self.AIStoneType == "black":
            self.AddAIStone((round(self.Board.size[0]/2),round(self.Board.size[1]/2)))








class MCTSActuator(threading.Thread):
    def __init__(self,move,GameState,ReportQueue,AIStoneType,searchrange,TimeLimit=10):
        threading.Thread.__init__(self)
        self.Event = threading.Event()
        self.GameState = GameState
        self.SearchRange = searchrange

        self.AIStoneType = AIStoneType
        self.MyMove = move
        self.EnemyStoneType = "white" if self.AIStoneType == "black" else "black"
        self.TimeLimit = TimeLimit
        self.ReportQueue = ReportQueue
        self.Wins = 0
        self.Simulations = 0

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

    def GetOpenMovesPlus(self,board):
        """Returns available unoccupied positions  within a square of the outermost stones + range
        Used to reduce number of simulations"""

        low = [board.size[0],board.size[1]]
        high = [1,1]
        OpenMoves = []

        for stone in board.stones:

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
                    OpenMoves.append((x, y))

        return OpenMoves

    def DuplicateBoard(self, Board):
        g = GameBoard(Board.size[0], Board.size[1])

        for x in Board.WhiteStones:
            g.AddStone("white", x)
        for y in Board.BlackStones:
            g.AddStone("black", y)

        return g
    def start(self):
        starting_state = Node(self.GameState)
        total_simulations = 0
        for move in self.GetOpenMovesPlus(self.GameState):
            Node(self.GenerateCustomGameBoard(starting_state,move,self.AIStoneType),parent=starting_state)
        self.iterate(starting_state,total_simulations)
    def iterate(self,currentstate):
        uctvalues = []

        for child in currentstate.children:
            uctvalues.append((child,UCT(child.wins,child.traversals,currentstate.traversals)))
        uctvalues = sorted(uctvalues,key=lambda x: uctvalues[x][1],reverse=True)

        selection_state = uctvalues[0][0]

        if not selection_state.children:  # check if is terminal node
            if selection_state.traversals == 0:  # check if it has NOT been visited(traversed)
                result = self.simulate(selection_state.gamestate)  # simulate random playout to end
                selection_state.backpropogate(result)

            elif selection_state.traversals != 0:  # requires work on. UNFINISHED
                for move in self.GetOpenMovesPlus(selection_state):
                    pass
                uctvalues = []
                for child in currentstate.children:

                    uctvalues.append((child, UCT(child.wins, child.traversals, currentstate.traversals)))
                uctvalues = sorted(uctvalues, key=lambda x: uctvalues[x][1], reverse=True)

                selection_state = uctvalues[0][0]



    def simulate(self,gamestate):
        if len(gamestate.BlackStones) == len(gamestate.WhiteStones):
            turn = self.AIStoneType if self.AIStoneType == "black" else self.EnemyStoneType
        elif len(gamestate.BlackStones) > len(gamestate.WhiteStones):
            turn = self.AIStoneType if self.AIStoneType == "white" else self.EnemyStoneType
        board = self.DuplicateBoard(gamestate)
        winchecker = WinChecker(board)
        while True:

            if not self.GetOpenMovesPlus(board):
                wins = 0
                break
            board.AddStone(turn,random.choice(self.GetOpenMovesPlus(board)))
            if winchecker.Check(turn) and turn == self.AIStoneType:
                wins = 1
                break
            elif winchecker.Check(turn) and turn == self.EnemyStoneType:
                wins = -1
                break
            turn = self.EnemyStoneType if turn == self.AIStoneType else self.AIStoneType
        return wins

class Node():
    def __init__(self, gamestate, parent=None):
        self.gamestate = gamestate
        self.parent = parent
        self.children = []
        self.traversals = 0
        self.wins = 0
        if parent:
            self.parent.register(self)

    def backpropogate(self, wins=1):
        self.traversals += 1
        self.wins += wins
        if self.parent:
            self.parent.backpropogate(wins)

    def register(self, child):
        self.children.append(child)


def UCT(wi, ni, t, c=math.sqrt(2)):
    """UCT SELECTION FUNCTION
    wi : number of wins after ith move
    ni : number of simulations after ith move
    c  : exploration parameter. default is sqrt(2)
    t  : total number of simulations (ni of parents node) sum of all ni"""
    return wi/ni + c*math.sqrt(math.log(t)/ni)