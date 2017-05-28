from AICore import AICore
from Analyzer import WinChecker
import threading, math, time,random, queue
from main import GameBoard


class MonteCarlo(AICore):
    def __init__(self, board=None, reportui=None, aistoneType="white",searchrange=4, TimeLimit=10,GameLimit=None,threadlimit=None):
        AICore.__init__(self, board, aistoneType)
        self.TimeLimit = TimeLimit
        self.GameLimit = GameLimit
        self.threadlimit = threadlimit
        self.ReportUI = reportui
        self.SearchRange = searchrange
        if self.AIStoneType == "black":
            self.AddAIStone((round(self.Board.size[0]/2),round(self.Board.size[1]/2)))

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


    def ChooseMove(self):
        moves = self.GetOpenMovesPlus(self.Board)
        totalmovecount = 0
        totalwins = 0
        movedata = []
        reportqueue = queue.Queue()
        threads = []
        startedthreads = 0
        for move in moves:
            passboard = self.GenerateCustomGameBoard(self.Board,move,self.AIStoneType)

            t = MCTSActuator(move,passboard,reportqueue,self.AIStoneType,self.SearchRange,self.TimeLimit,self.GameLimit)
            print("start thread",t)
            t.daemon = True
            t.start()
            startedthreads += 1
            threads.append(t)


        while threads:
            print(threads)
            data = reportqueue.get()
            if data[0] == "RESULT":
                print("GOT DATA",data)
                movedata.append((data[1],data[2],data[3]))
                totalmovecount += data[2]
                totalwins += data[3]
                if self.ReportUI:
                    self.ReportUI(data[1],data[2],data[3])
                startedthreads -= 1
            if startedthreads <= 0:
                break
            for t in threads:
                if t.isAlive():
                    pass
                else:

                    threads.remove(t)
        print("reached")
        biggest = 0
        bestmove = None
        for data in movedata:
            if UCT(data[2],data[1],totalmovecount) > biggest:
                bestmove = data[0]
        return bestmove, totalwins/totalmovecount


class MCTSActuator(threading.Thread):
    def __init__(self,move,GameState,ReportQueue,AIStoneType,searchrange,TimeLimit=10,GameLimit=None):
        threading.Thread.__init__(self)
        self.Event = threading.Event()
        self.GameState = GameState
        self.SearchRange = searchrange

        self.AIStoneType = AIStoneType
        self.MyMove = move
        self.EnemyStoneType = "white" if self.AIStoneType == "black" else "black"
        if not GameLimit:
            self.TimeMode = True
            self.TimeLimit = TimeLimit
        elif not TimeLimit:
            self.TimeMode = False
            self.GameLimit = GameLimit
        self.ReportQueue = ReportQueue
        self.Wins = 0
        self.Simulations = 0

    def run(self):
        self.Simulate()
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

    def DuplicateBoard(self,Board):
        g = GameBoard(Board.size[0],Board.size[1])

        for x in Board.WhiteStones:
            g.AddStone("white",x)
        for y in Board.BlackStones:
            g.AddStone("black",y)


        return g
    def Simulate(self):

        if self.TimeMode:
            starttime = time.time()
            while time.time()-starttime <= self.TimeLimit and not self.Event.is_set():
                self.Simulations += 1
                cboard = self.DuplicateBoard(self.GameState)

                winchecher = WinChecker(cboard)
                turn = self.EnemyStoneType
                while True:
                    if not self.GetOpenMovesPlus(cboard):
                        break
                    cboard.AddStone(turn,random.choice(self.GetOpenMovesPlus(cboard)))
                    if winchecher.Check(turn) and turn == self.AIStoneType:
                        self.Wins += 1
                        break
                    elif winchecher.Check(turn) and turn == self.EnemyStoneType:    # test code to encourage defense
                        self.Wins -= 1
                        break
                    turn = self.EnemyStoneType if turn == self.AIStoneType else self.AIStoneType

        elif not self.TimeMode:

            while self.Simulations < self.GameLimit and not self.Event.is_set():
                self.Simulations += 1
                cboard = self.DuplicateBoard(self.GameState)
                winchecher = WinChecker(cboard)
                turn = self.EnemyStoneType
                while True:
                    if not self.GetOpenMovesPlus(cboard):
                        break
                    cboard.AddStone(turn, random.choice(self.GetOpenMovesPlus(cboard)))
                    if winchecher.Check(turn) and turn == self.AIStoneType:
                        self.Wins += 1
                        break
                    elif winchecher.Check(turn) and turn == self.EnemyStoneType:    # test code to encourage defense
                        self.Wins -= 1
                        break
                    turn = self.EnemyStoneType if turn == self.AIStoneType else self.AIStoneType

        self.ReportQueue.put(("RESULT",self.MyMove,self.Simulations,self.Wins))
        print("END THREAD",self)

def UCT(wi, ni, t, c=math.sqrt(2)):
    """UCT SELECTION FUNCTION
    wi : number of wins after ith move
    ni : number of simulations after ith move
    c  : exploration parameter. default is sqrt(2)
    t  : total number of simulations (ni of parents node) sum of all ni"""
    return wi/ni + c*math.sqrt(math.log(t)/ni)