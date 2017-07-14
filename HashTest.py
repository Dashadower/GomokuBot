from AICore import AICore
from main import GameBoard
from collections import Counter
from Analyzer import Analyzer,WinChecker
import time, random, multiprocessing
class AlphaBeta(AICore):
    def __init__(self,initialgamestate,aistonetype, plydepth,tilesearchrange):
        AICore.__init__(self, initialgamestate, aistonetype,tilesearchrange)
        self.EnemyStoneType = "black" if self.AIStoneType == "white" else "white"
        self.PlyDepth = plydepth
        self.ControlQueue = multiprocessing.Queue()
        self.OpenSearchRange = tilesearchrange
        self.process = multiprocessing.Process(target=AlphaBetaActuator,args=(self.ControlQueue,self.AIStoneType,self.PlyDepth,self.OpenSearchRange))
        self.process.daemon = True
        self.process.start()
    def ChooseMove(self):
        self.ControlQueue.put(("START",self.Board))
        while True:
            data = self.ControlQueue.get()
            if data:
                if data[0] == "START":
                    self.ControlQueue.put(data)
                else:
                    print("GOT DATA",data)
                    self.AddAIStone(data[1])
                    break
    def GetResult(self):
        try:
            data = self.ControlQueue.get_nowait()
        except:
            return False
        else:
            return data[0]

def compare(s, t):
    return Counter(s) == Counter(t)

class AlphaBetaActuator():
    def __init__(self,ControlQueue,aistonetype,depth,tilesearchrange):
        self.AIStoneType = aistonetype
        self.EnemyStoneType = "black" if self.AIStoneType == "white" else "white"
        self.ControlQueue  = ControlQueue
        self.PlyDepth = depth
        self.OpenSearchRange = tilesearchrange
        self.CheckForWork()

    def CheckForWork(self):
        while True:
            data = self.ControlQueue.get()
            if data:
                if data[0] == "START":
                    self.aiutils = AICore(data[1],self.AIStoneType,self.OpenSearchRange)


                    for moves in self.aiutils.GetOpenMovesPlus(data[1]):
                        self.HashTable = []
                        for x in range(1,self.PlyDepth+1):
                            result = self.AlphaBeta(self.aiutils.GenerateCustomGameBoard(self.aiutils.DuplicateBoard(data[1]),moves,self.AIStoneType),moves,x,False,-10000000,10000000)
                            print("DEPTH",x,result)


                    self.ControlQueue.put(result)
                elif data == "EXIT":
                    break

    def AlphaBeta(self,board,move,depth,isMaximizingPlayer,alpha,beta):

        if WinChecker(board).Check(self.AIStoneType) or WinChecker(board).Check(self.EnemyStoneType) or depth == 0:
            now = time.time()
            found = False
            for item in self.HashTable:
                if compare(item[0][0],board.BlackStones) and compare(item[0][1],board.WhiteStones):
                    analysisresult = item[1]
                    found = True

            if not found:
                analysisresult = Analyzer(board).Grader(self.AIStoneType)-Analyzer(board).Grader(self.EnemyStoneType)
                self.HashTable.append(((board.BlackStones,board.WhiteStones),analysisresult))
            end = time.time()
            print(end-now, found)
            return (analysisresult,move)
        if isMaximizingPlayer:
            v = -10000000

            for moves in self.aiutils.GetOpenMovesPlus(board):
                result = self.AlphaBeta(self.aiutils.GenerateCustomGameBoard(board,moves,self.AIStoneType),moves,depth-1,False, alpha,beta)[0]
                v = max(v,result)

                alpha = max(alpha,v)
                if beta <= alpha:
                    break

            return (v, move)
        else:
            v = 10000000

            for moves in self.aiutils.GetOpenMovesPlus(board):
                result = self.AlphaBeta(self.aiutils.GenerateCustomGameBoard(board,moves,self.EnemyStoneType),moves,depth-1,True,alpha,beta)[0]
                v = min(v,result)
                beta = min(beta,v)

                if beta <= alpha:
                    break
            return (v,move)




