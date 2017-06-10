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
    def __init__(self, board=None, reportui=None, aistoneType="white", TimeLimit=10):
        AICore.__init__(self, board, aistoneType)
        self.TimeLimit = TimeLimit

        self.ReportUI = reportui
        if self.AIStoneType == "black":
            self.AddAIStone((round(self.Board.size[0]/2),round(self.Board.size[1]/2)))
    def ChooseMove(self):
        returnqueue = queue.Queue()
        chooser = MCTSActuator(self.Board,returnqueue,self.AIStoneType,self.TimeLimit)
        chooser.start()
        return self.check(returnqueue)
    def check(self,queueobj):
        data = queueobj.get()
        if not data:
            if self.ReportUI:
                self.ReportUI.after(100,lambda:self.check(queueobj))
            else:
                time.sleep(0.1)
                self.check(queueobj)
        else:
            position = data.pos
            winrate = data.Wins/data.Simulations*100
            return (position,winrate)










class MCTSActuator(threading.Thread,AICore):
    def __init__(self,GameState,ReportQueue,AIStoneType,TimeLimit=10,searchrange=4):
        threading.Thread.__init__(self)

        self.Event = threading.Event()
        self.GameState = GameState


        self.AIStoneType = AIStoneType
        self.SearchRange = searchrange
        self.EnemyStoneType = "white" if self.AIStoneType == "black" else "black"
        self.TimeLimit = TimeLimit
        self.ReportQueue = ReportQueue
        self.Wins = 0
        self.Simulations = 0


    def start(self):
        starting_state = Node(self.GameState)
        self.starttime = time.time()
        for move in self.GetOpenMovesPlus(self.GameState):
            Node(super().GenerateCustomGameBoard(starting_state.gamestate,move,self.AIStoneType),parent=starting_state,pos=move)
        self.iterate(starting_state)
        ucbvalues = []
        for child in starting_state.children:
            ucbvalues.append((child, UCT(child.wins, child.traversals, starting_state.traversals)))
        ucbvalues = sorted(ucbvalues, key=lambda x: x[1], reverse=True)
        self.ReportQueue.put(ucbvalues[0][0])
    def iterate(self,currentstates):

        print("ctime:",time.time()-self.starttime)
        currentstate = currentstates
        while time.time()-self.starttime <= float(self.TimeLimit):  # @@@@@@@@@@@ NOT WORKING!! STOPPED IN LOOP
            print("loop",time.time()-self.starttime,currentstate)
            if not currentstate.children:  # check if terminal node
                if currentstate.traversals == 0:  # check if visited
                    # not visited, rollout
                    self.simulate(currentstate)

                elif currentstate.traversals != 0:  # already visited
                    cturn = currentstate.gamestate.turn
                    for move_1 in self.GetOpenMovesPlus(currentstate.gamestate):
                        newgamestate = self.GenerateCustomGameBoard(currentstate.gamestate,move_1,cturn)
                        for move_2 in self.GetOpenMovesPlus(newgamestate):
                            newturn = "black" if cturn == "white" else "black"
                            finalgamestate = self.GenerateCustomGameBoard(newgamestate,move_2,newturn)
                            Node(finalgamestate,currentstate)
                            self.simulate(currentstate.children[0])
                            currentstate = currentstate.children[0]
            elif currentstate.children:
                ucbvalues = []
                for child in currentstate.children:
                    ucbvalues.append((child,UCT(child.wins,child.traversals,currentstate.traversals)))
                ucbvalues = sorted(ucbvalues, key=lambda x: x[1], reverse=True)
                currentstate = ucbvalues[0][0]

            print("reached")


    




    def simulate(self,gamestate):
        turn = self.AIStoneType if gamestate.gamestate.turn == self.AIStoneType else self.EnemyStoneType
        board = super().DuplicateBoard(gamestate.gamestate)
        winchecker = WinChecker(board,debug=False)
        while True:

            if not super().GetOpenMovesPlus(board):
                wins = 0

                break
            else:
                board.AddStone(turn,random.choice(super().GetOpenMovesPlus(board)))
                if winchecker.Check(turn) and turn == self.AIStoneType:
                    wins = 1

                    break
                elif winchecker.Check(turn) and turn == self.EnemyStoneType:
                    wins = -1

                    break
                turn = self.EnemyStoneType if turn == self.AIStoneType else self.AIStoneType

        gamestate.backpropogate(wins)

class Node():
    def __init__(self, gamestate, parent=None,pos=None):
        self.gamestate = gamestate
        self.parent = parent
        self.children = []
        self.traversals = 0
        self.wins = 0
        self.pos = pos
        if parent:
            self.parent.registerchild(self)

    def backpropogate(self, winsval=1):
        self.traversals += 1
        self.wins += winsval
        if self.parent:
            self.parent.backpropogate(winsval)

    def registerchild(self, child):
        self.children.append(child)


def UCT(wi, ni, t, c=math.sqrt(2)):
    """UCT SELECTION FUNCTION
    wi : number of wins after ith move
    ni : number of simulations after ith move
    c  : exploration parameter. default is sqrt(2)
    t  : total number of simulations (ni of parents node) sum of all ni"""
    if ni == 0:
        return 0
    else:
        return wi/ni + c*math.sqrt(math.log(t)/ni)