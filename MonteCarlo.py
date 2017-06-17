from AICore import AICore
from Analyzer import WinChecker
import threading, math, time, random, multiprocessing


class MonteCarlo(AICore):
    def __init__(self, board=None, reportui=None, aistoneType="white", searchrange=4, TimeLimit=10):
        AICore.__init__(self, board, aistoneType)
        self.TimeLimit = TimeLimit

        self.ReportUI = reportui
        self.SearchRange = searchrange
        self.process = []
        if self.AIStoneType == "black":
            self.AddAIStone((round(self.Board.size[0] / 2), round(self.Board.size[1] / 2)))
        self.inputqueue = multiprocessing.Queue()
        self.outputqueue = multiprocessing.Queue()
        self.process = multiprocessing.Process(target=MCTSActuator, args=(self.outputqueue, self.inputqueue, self.AIStoneType, self.SearchRange, self.TimeLimit))
        print("MonteCarlo: spawned slave process")
        self.process.daemon = True
        self.process.start()
    def ChooseMove(self):
        self.outputqueue.put(("START", self.Board))
        while True:
            data = self.inputqueue.get()
            if data:
                self.AddAIStone(data[0])
                try:
                    print(data[0], data[1], data[2], data[2] / data[1])
                except:
                    print(data[0], data[1], data[2], 0)
                break


"""Process communication protocol
1. Starting process:
function arguments: inputqueue, outputqueue, AIStoneType, searchrange, TimeLimit
inputqueue: queue where the process will recieve commands. outputqueue of the master process
outputqueue: queue where the process will send results. inputqueue of the mater class
aistonetype: aistonetype 
searchrange: smart open move search range
timelimit: thread simulation time limit
2. Sending commands to processes:
2-1. start montecarlo:
    Put following into inputqueue: ("START",gameboard)
    The process will start mcts starting from gameboard

2-2. kill process(soft kill):
    Put following into commqueue:"EXIT"
    This will kill the process AFTER ALL SIMULATIONS ARE FINISHED

3. Process results:
    Results are sent directly from process to the main process using inputqueue
    RESULT: (position, simulations, wins)
    position: selected best position
    simulations. total number of simulations done. ni on UCT
    wins: total number of winning simulations of root nude"""


class MCTSActuator(AICore):
    def __init__(self, inputqueue, outputqueue, AIStoneType, searchrange, TimeLimit=10):

        self.Event = threading.Event()

        self.SearchRange = searchrange

        self.AIStoneType = AIStoneType

        self.EnemyStoneType = "white" if self.AIStoneType == "black" else "black"
        self.TimeLimit = TimeLimit
        self.inputqueue = inputqueue
        self.outputqueue = outputqueue
        self.start()
    def start(self):
        print("MCTSActuator slave: online")
        while True:
            data = self.inputqueue.get()
            if not data:
                pass
            elif data == "EXIT":
                break
            else:
                if data[0] == "START":
                    starting_state = Node(data[1])
                    print("MCTSActuator: Recieved start simulation command",staticmethod)
                    for move in self.GetOpenMovesPlus(data[1]):
                        Node(super().GenerateCustomGameBoard(starting_state.gamestate, move, self.AIStoneType),
                             parent=starting_state, position=move)
                    self.iterate(starting_state)
                    uctvalues = []

                    for child in starting_state.children:
                        uctvalues.append((child, UCT(child.wins, child.traversals, starting_state.traversals)))
                    uctvalues = sorted(uctvalues, key=lambda x: x[1], reverse=True)

                    final_choice = uctvalues[0][0]
                    print("final",uctvalues)
                    self.outputqueue.put((final_choice.position, final_choice.simulations, final_choice.wins))

    def iterate(self, currentstate):
        print("currentstate",currentstate.position)
        start_state = currentstate
        starttime = time.time()
        while time.time() - starttime <= self.TimeLimit:
            print("current",start_state.position)
            #start_state.backpropogate(wins=0,simulations=0,traversals=1)
            if start_state.children:
                #print("children",start_state.children)
                uctvalues = []

                for child in start_state.children:
                    uctvalues.append((child, UCT(child.wins, child.simulations, start_state.simulations)))

                uctvalues = sorted(uctvalues, key=lambda x: x[1], reverse=True)
                #print("children uct",uctvalues)
                selection_state = uctvalues[0][0]
                selection_state.backpropogate(wins=0,simulations=0,traversals=1)
                print("current is highest child",selection_state.position,uctvalues[0][1])
                start_state = selection_state


            elif not start_state.children:
                print("no child",start_state.children)
                if start_state.traversals == 0:
                    print("backpropogate self")
                    start_state.backpropogate(self.simulate(start_state.gamestate),simulations=1,traversals=1)
                    start_state = currentstate
                elif start_state.traversals > 0:
                    #print("creating child",self.GetOpenMovesPlus(start_state.gamestate))
                    for move in self.GetOpenMovesPlus(start_state.gamestate):
                        Node(super().GenerateCustomGameBoard(start_state.gamestate, move, start_state.gamestate.turn),
                             parent=start_state, position=move)
                    if not start_state.children:
                        #print("reset to root")
                        #start_state = currentstate
                        start_state.backpropogate(self.simulate(start_state.gamestate),simulations=1,traversals=1)
                        start_state = currentstate
                    else:
                        print("current is first hcildren",start_state.children[0].position)
                        start_state = start_state.children[0]

    def simulate(self, gamestate):
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
            board.AddStone(turn, random.choice(super().GetOpenMovesPlus(board)))
            if winchecker.Check(turn) and turn == self.AIStoneType:
                wins = 1
                break
            elif winchecker.Check(turn) and turn == self.EnemyStoneType:
                wins = -1
                break
            turn = self.EnemyStoneType if turn == self.AIStoneType else self.AIStoneType
        return wins


class Node():
    def __init__(self, gamestate, parent=None, position=None):
        self.gamestate = gamestate
        self.parent = parent
        self.children = []
        self.traversals = 0
        self.simulations = 0
        self.wins = 0
        self.position = position
        if parent:
            self.parent.registerchild(self)

    def backpropogate(self, wins=1,simulations=1,traversals=0):
        self.traversals += traversals
        self.wins += wins
        self.simulations += simulations
        if self.parent:
            self.parent.backpropogate(wins,simulations,traversals)

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
        return wi / ni + c * math.sqrt(math.log(t) / ni)


if __name__ == "__main__":
    pass