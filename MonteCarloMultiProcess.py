from AICore import AICore

import  math, queue, multiprocessing, threading

from MonteCarlo import MCTSActuator
"""Process communication protocol
1. Starting process:
function arguments: commqueue,resultqueue,aistonetype,searchrange,timelimit,gamelimit
commqueue: queue object where COMMANDs are recieved
resultqueue: queue object where RESULTs are sent
aistonetype: aistonetype 
searchrange: smart open move search range
timelimit: thread simulation time limit
gamelimit: thread simulation max number of games
(if timelimit is set, gamelimit must be set to None, vice versa)
2. Sending commands to processes:
2-1. start simulations:
    Put following into commqueue: ("START",[((1,1),GameBoard),((1,2),GameBoard)])
    The process will simulate all game states in the list
    
2-2. kill process(soft kill):
    Put following into commqueue:"EXIT"
    This will kill the process AFTER ALL SIMULATIONS ARE FINISHED

3. Process results:
    Results are sent directly from process threads to the main process using resultqueue
    Refer to MonteCarlo.py for thread protocols"""



class MultiProcessedMCTC(AICore):
    def __init__(self, board=None, reportui=None, aistoneType="white",searchrange=4, TimeLimit=10,GameLimit=None,threadlimit=None,processlimit=4):
        AICore.__init__(self, board, aistoneType)
        self.TimeLimit = TimeLimit
        self.GameLimit = GameLimit
        self.threadlimit = threadlimit
        self.ProcessLimit = processlimit
        self.ReportUI = reportui
        self.SearchRange = searchrange
        self.CommQueues = []
        self.ReportQueue = multiprocessing.Queue()
        self.Processes = []
        if self.AIStoneType == "black":
            self.AddAIStone((round(self.Board.size[0]/2),round(self.Board.size[1]/2)))
    def InitiateProcess(self):
        for x in range(0,self.ProcessLimit):
            commqueue = multiprocessing.Queue()
            self.CommQueues.append(commqueue)
            p = multiprocessing.Process(target=ProcessHandler,args=(commqueue,self.ReportQueue,self.AIStoneType,self.SearchRange,self.TimeLimit,self.GameLimit))
            p.daemon = True
            self.Processes.append(p)
            p.start()
            print("STARTED PROCESS",p)


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
        startedthreads = len(moves)
        distributedremainder = False
        numberofprocess,remainder = divmod(len(moves),self.ProcessLimit)
        print("Each process gets ",numberofprocess,"remainder",remainder,"distributed")
        for x in self.CommQueues:
            datastream = []
            sendingmoves = []
            if not distributedremainder:
                for g in range(numberofprocess+remainder):
                    sendingmoves.append(moves.pop())
                distributedremainder = True
            else:
                for g in range(numberofprocess):
                    sendingmoves.append(moves.pop())
            for coord in sendingmoves:
                gboard = self.GenerateCustomGameBoard(self.Board,coord,self.AIStoneType)
                datastream.append((coord,gboard))
            x.put(("START",datastream))

        totalmovecount = 0
        totalwins = 0
        movedata = []

        while True:
            data = self.ReportQueue.get()
            if data[0] == "RESULT":
                print("GOT DATA", data)
                movedata.append((data[1],data[2],data[3]))
                totalmovecount += data[2]
                totalwins += data[3]
                startedthreads -= 1
            if startedthreads <= 0:
                break




        print("reached")
        biggest = 0
        bestmove = None
        for data in movedata:
            if UCT(data[2],data[1],totalmovecount) > biggest:
                bestmove = data[0]
        return bestmove, totalwins/totalmovecount

def ProcessHandler(commqueue,resultqueue,aistonetype,searchrange,timelimit,gamelimit):
    while True:
        data = commqueue.get()
        if data[0] == "EXIT":
            break
        elif data[0] == "START":
            tasks = data[1]


            startedthreads = 0
            for task in tasks:
                t = MCTSActuator(task[0],task[1],resultqueue,aistonetype,searchrange,timelimit,gamelimit)
                t.daemon = True
                t.start()
                print("start thread",t)









def UCT(wi, ni, t, c=math.sqrt(2)):
    """UCT SELECTION FUNCTION
    wi : number of wins after ith move
    ni : number of simulations after ith move
    c  : exploration parameter. default is sqrt(2)
    t  : total number of simulations (ni of parents node) sum of all ni"""
    return wi/ni + c*math.sqrt(math.log(t)/ni)