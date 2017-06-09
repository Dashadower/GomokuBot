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








class MCTSActuator(threading.Thread,AICore):
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

    def start(self):
        starting_state = Node(self.GameState)

        for move in self.GetOpenMovesPlus(self.GameState):
            Node(super().GenerateCustomGameBoard(starting_state,move,self.AIStoneType),parent=starting_state)
        self.iterate(starting_state)
    def iterate(self,currentstate):
        while True:
            if currentstate.children:
                if currentstate.traversals == 0:
                    # rollout
                    result = self.simulate(currentstate)
                    currentstate.backpropogate(result)
                elif currentstate.traversals != 0:
                    for move in self.GetOpenMoves(currentstate):
                        Node(super().GenerateCustomGameBoard(currentstate,move,))
                """uctvalues = []
    
                for child in currentstate.children:
                    uctvalues.append((child,UCT(child.wins,child.traversals,currentstate.traversals)))
                uctvalues = sorted(uctvalues,key=lambda x: uctvalues[x][1],reverse=True)
    
                selection_state = uctvalues[0][0]
    
                if not selection_state.children:  # check if is terminal node
                    if selection_state.traversals == 0:  # check if it has NOT been visited(traversed)
                        result = self.simulate(selection_state.gamestate)  # simulate random playout to end
                        selection_state.backpropogate(result)
    
                    elif selection_state.traversals != 0:  # requires work on. UNFINISHED
                        for move in super().GetOpenMovesPlus(selection_state):
                            pass
                        uctvalues = []
                        for child in currentstate.children:
    
                            uctvalues.append((child, UCT(child.wins, child.traversals, currentstate.traversals)))
                        uctvalues = sorted(uctvalues, key=lambda x: uctvalues[x][1], reverse=True)
    
                        selection_state = uctvalues[0][0]
    
                elif selection_state.children:
                    self.iterate()"""



    def simulate(self,gamestate):
        if len(gamestate.BlackStones) == len(gamestate.WhiteStones):
            turn = self.AIStoneType if self.AIStoneType == "black" else self.EnemyStoneType
        elif len(gamestate.BlackStones) > len(gamestate.WhiteStones):
            turn = self.AIStoneType if self.AIStoneType == "white" else self.EnemyStoneType
        board = super().DuplicateBoard(gamestate)
        winchecker = WinChecker(board)
        while True:

            if not super().GetOpenMovesPlus(board):
                wins = 0
                break
            board.AddStone(turn,random.choice(super().GetOpenMovesPlus(board)))
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
            self.parent.registerchild(self)

    def backpropogate(self, wins=1):
        self.traversals += 1
        self.wins += wins
        if self.parent:
            self.parent.backpropogate(wins)

    def registerchild(self, child):
        self.children.append(child)


def UCT(wi, ni, t, c=math.sqrt(2)):
    """UCT SELECTION FUNCTION
    wi : number of wins after ith move
    ni : number of simulations after ith move
    c  : exploration parameter. default is sqrt(2)
    t  : total number of simulations (ni of parents node) sum of all ni"""
    return wi/ni + c*math.sqrt(math.log(t)/ni)