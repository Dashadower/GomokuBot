from AICore import AICore
from main import GameBoard
from Analyzer import Analyzer,WinChecker
import time, random, multiprocessing
class AlphaBeta(AICore):
    def __init__(self,initialgamestate,aistonetype, plydepth,tilesearchrange,processlimit):
        AICore.__init__(self, initialgamestate, aistonetype,tilesearchrange)
        self.EnemyStoneType = "black" if self.AIStoneType == "white" else "white"
        self.PlyDepth = plydepth
        self.ControlQueue = multiprocessing.Queue()
        self.OpenSearchRange = tilesearchrange
        self.ProcessLimit = processlimit
        self.Processes = []
        self.CommQueues = []
    def InitiateProcess(self):
        for x in range(0,self.ProcessLimit):
            q = multiprocessing.Queue()
            self.CommQueues.append(q)
            p = multiprocessing.Process(target=AlphaBetaActuator, args=(self.ControlQueue,q, self.AIStoneType, self.PlyDepth, self.OpenSearchRange))
            p.daemon = True
            self.Processes.append(p)
            p.start()
            print("STARTED PROCESS",p)
    def ChooseMove(self):

        moves = self.GetOpenMovesPlus(self.Board)
        startedprocesses = len(moves)
        distributedremainder = False
        numberofprocess, remainder = divmod(len(moves), self.ProcessLimit)
        datalist = []
        for q in self.CommQueues:
            sendingmoves = []
            datastream = []
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
            q.put(("START",datastream))
        while startedprocesses >0:
            data = self.ControlQueue.get()
            if data:
                print("GOT DATA",data)
                datalist.append(data)
                startedprocesses -= 1
        datalist = sorted(datalist,key=lambda x:x[0],reverse=True)
        self.AddAIStone(datalist[0][1])
    def GetResult(self):
        try:
            data = self.ControlQueue.get_nowait()
        except:
            return False
        else:
            return data[0]

class AlphaBetaActuator():
    def __init__(self,ControlQueue,DataQueue,aistonetype,depth,tilesearchrange):
        self.AIStoneType = aistonetype
        self.EnemyStoneType = "black" if self.AIStoneType == "white" else "white"
        self.ControlQueue  = ControlQueue
        self.DataQueue = DataQueue
        self.PlyDepth = depth
        self.OpenSearchRange = tilesearchrange
        self.CheckForWork()

    def CheckForWork(self):
        while True:
            data = self.DataQueue.get()
            if data:
                if data[0] == "START":
                    for coord,board in data[1]:


                        self.aiutils = AICore(board,self.AIStoneType,self.OpenSearchRange)

                        result = self.AlphaBeta(board,coord,self.PlyDepth,False,-10000000,10000000)

                        self.ControlQueue.put((result[0],coord))
                elif data == "EXIT":
                    break

    def AlphaBeta(self,board,move,depth,isMaximizingPlayer,alpha,beta):
        print("CURRENT POSITION",move,isMaximizingPlayer)
        if WinChecker(board).Check(self.AIStoneType) or WinChecker(board).Check(self.EnemyStoneType) or depth == 0:
            print("REACHED TERMINAL")
            return (Analyzer(board).Grader(self.AIStoneType)-Analyzer(board).Grader(self.EnemyStoneType),move)
        if isMaximizingPlayer:
            v = -10000000
            for moves in self.aiutils.GetOpenMovesPlus(board):
                v = max(v,self.AlphaBeta(self.aiutils.GenerateCustomGameBoard(board,moves,self.AIStoneType),moves,depth-1,False, alpha,beta)[0])
                alpha = max(alpha,v)
                if beta <= alpha:
                    break
            return (v,move)
        else:
            v = 10000000
            for moves in self.aiutils.GetOpenMovesPlus(board):
                v = min(v,self.AlphaBeta(self.aiutils.GenerateCustomGameBoard(board,moves,self.EnemyStoneType),moves,depth-1,True,alpha,beta)[0])
                beta = min(beta,v)
                if beta <= alpha:
                    break
            return (v,move)




