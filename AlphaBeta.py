from AICore import AICore
from main import GameBoard
from Analyzer import WinChecker, Analyzer
#from AnalyzerOptimized import Analyzer
import time, random, multiprocessing

class AlphaBeta(AICore):
    def __init__(self,initialgamestate,aistonetype, plydepth,tilesearchrange):
        AICore.__init__(self, initialgamestate, aistonetype,tilesearchrange)
        self.EnemyStoneType = "black" if self.AIStoneType == "white" else "white"
        self.PlyDepth = plydepth
        self.ControlQueue = multiprocessing.Queue()
        self.ResultQueue = multiprocessing.Queue()
        self.OpenSearchRange = tilesearchrange
        self.process = multiprocessing.Process(target=AlphaBetaActuator,args=(self.ControlQueue,self.ResultQueue,self.AIStoneType,self.PlyDepth,self.OpenSearchRange))
        self.process.daemon = True
        self.process.start()
    def ChooseMove(self):
        self.ControlQueue.put(("START",self.Board))
        """while True:
            data = self.ControlQueue.get()
            if data:
                if data[0] == "START":
                    self.ControlQueue.put(data)
                else:
                    print("GOT DATA",data)
                    print("FINALIZED DATA",data)
                    self.AddAIStone(data[1])
                    break"""
    def GetResult(self):
        try:

            data = self.ResultQueue.get_nowait()
            print(data)
        except:
            return False
        else:


            print("GOT DATA", data)
            print("FINALIZED DATA", data)
            #self.AddAIStone(data[1])
            return data

class AlphaBetaActuator():
    def __init__(self,ControlQueue,ResultQueue,aistonetype,depth,tilesearchrange):
        self.AIStoneType = aistonetype
        self.EnemyStoneType = "black" if self.AIStoneType == "white" else "white"
        self.ControlQueue = ControlQueue
        self.ResultQueue = ResultQueue
        self.PlyDepth = depth
        self.OpenSearchRange = tilesearchrange
        self.CheckForWork()

    def CheckForWork(self):
        while True:
            data = self.ControlQueue.get()
            if data:
                if data[0] == "START":
                    self.aiutils = AICore(data[1],self.AIStoneType,self.OpenSearchRange)
                    datas = []
                    for moves in self.aiutils.GetOpenMovesPlus(data[1],self.OpenSearchRange):
                        #print("NEW GAME BROS!!")
                        result = self.AlphaBeta(self.aiutils.GenerateCustomGameBoard(self.aiutils.DuplicateBoard(data[1]),moves,self.AIStoneType),moves,self.PlyDepth,False,-10000000,10000000,self.OpenSearchRange)
                        datas.append((result[0],moves))
                    current = (-20000000000,("flibbergibbit","datasover1"))
                    print(datas)
                    for items in datas:
                        if int(items[0]) > current[0]:
                            current = items

                    self.ResultQueue.put(current)

                    print("SENT DATA", current,self.ResultQueue.empty())


                elif data == "EXIT":
                    break

    def AlphaBeta(self,board,move,depth,isMaximizingPlayer,alpha,beta,tilesearchrange):
        #print("CURRENT POSITION",move,isMaximizingPlayer)
        if WinChecker(board).CheckBoth() or depth == 0:

            return (Analyzer(board).Grader(self.AIStoneType)-Analyzer(board).Grader(self.EnemyStoneType),move)

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




