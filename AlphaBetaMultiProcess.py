from AICore import AICore
from main import GameBoard
from Analyzer import Analyzer,WinChecker
import time, random, multiprocessing
from collections import Counter
class AlphaBeta(AICore):
    def __init__(self,initialgamestate,aistonetype, plydepth,tilesearchrange,processlimit,transitionrange):
        AICore.__init__(self, initialgamestate, aistonetype,tilesearchrange)
        self.EnemyStoneType = "black" if self.AIStoneType == "white" else "white"
        self.PlyDepth = plydepth
        self.ControlQueue = multiprocessing.Queue()
        self.OpenSearchRange = tilesearchrange
        self.TransitionRange = transitionrange
        self.ReportHook = print
        self.ProcessLimit = processlimit
        self.Processes = []
        self.CommQueues = []
        self.datalist = []
        self.PIDs = []
    def InitiateProcess(self):
        for x in range(0,self.ProcessLimit):
            q = multiprocessing.Queue()

            self.CommQueues.append(q)
            p = multiprocessing.Process(target=AlphaBetaActuator, args=(self.ControlQueue,q, self.AIStoneType, self.PlyDepth, self.OpenSearchRange))
            p.daemon = True
            self.Processes.append(p)
            p.start()
            self.PIDs.append(p.pid)

        return (self.Processes,self.PIDs)
    def ChooseMove(self):
        moves = self.GetOpenMovesPlus(self.Board, self.OpenSearchRange)
        startedprocesses = len(moves)
        self.ReportHook("1PLY 검색 타일 수:"+str(startedprocesses))

        if startedprocesses >= self.TransitionRange:

            self.Calctype = "multi"

            self.processreturn = self.ProcessLimit

            self.datalist = []
            self.ReportHook("USING MULTIPROCESSES")
            distributedremainder = False
            numberofprocess, remainder = divmod(startedprocesses, self.ProcessLimit)

            for resultqueue in self.CommQueues:
                sendingmoves = []
                if not distributedremainder:
                    for g in range(numberofprocess+remainder):
                        sendingmoves.append(moves.pop())
                    distributedremainder = True
                else:
                    for g in range(numberofprocess):
                        sendingmoves.append(moves.pop())

                    #gboard = self.GenerateCustomGameBoard(self.Board,coord,self.AIStoneType)

                resultqueue.put(("START",(sendingmoves,self.Board)))
        else:
            self.ReportHook("USING SINGLE PROCESS")
            self.Calctype = "single"
            self.CommQueues[0].put(("START_SINGLE",self.Board))

    def GetResult(self):

        if self.Calctype == "multi":
            print("GetResult", self.processreturn)
            try:
                data = self.ControlQueue.get_nowait()
            except:
                if self.processreturn == 0:
                    datalist = sorted(self.datalist,key=lambda x:x[0],reverse=True)
                    return datalist[0]
                else:
                    return False
            else:
                if data:
                    self.datalist.append(data)
                    self.processreturn -= 1
                if self.processreturn == 0:
                    datalist = sorted(self.datalist,key=lambda x:x[0],reverse=True)
                    return datalist[0]
                else:
                    return False
        elif self.Calctype == "single":
            try:

                data = self.ControlQueue.get_nowait()
            except:
                return False
            else:


                # self.AddAIStone(data[1])
                return data


def compare(s, t):
    return Counter(s) == Counter(t)

class AlphaBetaActuator():
    def __init__(self,ControlQueue,DataQueue,aistonetype,depth,tilesearchrange):
        self.AIStoneType = aistonetype
        self.EnemyStoneType = "black" if self.AIStoneType == "white" else "white"
        self.ControlQueue = ControlQueue
        self.DataQueue = DataQueue
        self.PlyDepth = depth
        self.OpenSearchRange = tilesearchrange
        self.CheckForWork()

    def CheckForWork(self):
        while True:
            data = self.DataQueue.get()
            if data:
                if data[0] == "START_SINGLE":
                    self.aiutils = AICore(data[1], self.AIStoneType, self.OpenSearchRange)
                    datas = []
                    for moves in self.aiutils.GetOpenMovesPlus(data[1], self.OpenSearchRange):
                        result = self.AlphaBeta(self.aiutils.GenerateCustomGameBoard(data[1], moves,self.AIStoneType), moves, self.PlyDepth, False,-10000000, 10000000, self.OpenSearchRange)
                        datas.append((result[0], moves))
                    current = (-20000000000, ("flibbergibbit", "datasover1"))
                    for items in datas:
                        if int(items[0]) > current[0]:
                            current = items
                    self.ControlQueue.put(current)
                elif data[0] == "START":
                    moves, board = data[1]
                    datas = []
                    self.aiutils = AICore(board, self.AIStoneType, self.OpenSearchRange)
                    for move in moves:
                        result = self.AlphaBeta(self.aiutils.GenerateCustomGameBoard(board, move,self.AIStoneType), move, self.PlyDepth, False,-10000000, 10000000, self.OpenSearchRange)
                        datas.append((result[0],move))
                    datas = sorted(datas,key=lambda x:x[0],reverse=True)
                    self.ControlQueue.put(datas[0])
    def AlphaBeta(self,board,move,depth,isMaximizingPlayer,alpha,beta,tilesearchrange):
        #print("CURRENT POSITION",move,isMaximizingPlayer)
        if WinChecker(board).CheckBoth() or depth == 0:
            ganalyst = Analyzer(board)
            return (ganalyst.Grader(self.AIStoneType)-ganalyst.Grader(self.EnemyStoneType),move)

        if isMaximizingPlayer:
            v = -10000000
            for moves in self.aiutils.GetOpenMovesPlus(board,self.OpenSearchRange):
                v = max(v,self.AlphaBeta(self.aiutils.GenerateCustomGameBoard(board,moves,self.AIStoneType),moves,depth-1,False, alpha,beta,tilesearchrange)[0])
                alpha = max(alpha,v)
                if beta <= alpha:
                    #print("BETA CUTOFF")
                    break
            return (v,move)
        else:
            v = 10000000
            for moves in self.aiutils.GetOpenMovesPlus(board,self.OpenSearchRange):
                v = min(v,self.AlphaBeta(self.aiutils.GenerateCustomGameBoard(board,moves,self.EnemyStoneType),moves,depth-1,True,alpha,beta,tilesearchrange)[0])
                beta = min(beta,v)
                if beta <= alpha:
                    #print("ALPHA CUTOFF")
                    break
            return (v,move)






