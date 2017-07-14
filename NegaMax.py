from AICore import AICore
from main import GameBoard
from Analyzer import Analyzer,WinChecker
import time, random, multiprocessing

class NegaMax(AICore):
    def __init__(self,initialgamestate,aistonetype, plydepth,tilesearchrange):
        AICore.__init__(self, initialgamestate, aistonetype,tilesearchrange)
        self.EnemyStoneType = "black" if self.AIStoneType == "white" else "white"
        self.PlyDepth = plydepth
        self.ControlQueue = multiprocessing.Queue()
        self.OpenSearchRange = tilesearchrange
        self.process = multiprocessing.Process(target=NegaMaxActuator,args=(self.ControlQueue,self.AIStoneType,self.PlyDepth,self.OpenSearchRange))
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
                    print("FINAL RESULT",data)
                    self.AddAIStone(data[1])
                    break
    def GetResult(self):
        try:
            data = self.ControlQueue.get_nowait()
        except:
            return False
        else:
            return data[0]

class NegaMaxActuator():
    def __init__(self,ControlQueue,aistonetype,depth,tilesearchrange):
        self.AIStoneType = aistonetype
        self.EnemyStoneType = "black" if self.AIStoneType == "white" else "white"
        self.ControlQueue  = ControlQueue
        self.PlyDepth = depth
        self.OpenSearchRange = tilesearchrange
        self.Currentturn = self.EnemyStoneType
        self.CheckForWork()

    def CheckForWork(self):
        while True:
            data = self.ControlQueue.get()
            if data:
                if data[0] == "START":
                    self.aiutils = AICore(data[1],self.AIStoneType,self.OpenSearchRange)
                    datas = []
                    for moves in self.aiutils.GetOpenMovesPlus(data[1],self.OpenSearchRange):
                        print("NEW GAME BROS!!")
                        result = self.NegaMax(self.aiutils.GenerateCustomGameBoard(self.aiutils.DuplicateBoard(data[1]),moves,self.AIStoneType),moves,self.AIStoneType,self.PlyDepth,-10000000,10000000,self.OpenSearchRange)
                        datas.append((result[0],moves))
                    current = (-20000000000,None)
                    for items in datas:
                        if int(items[0]) > current[0]:
                            current = items
                    self.ControlQueue.put(current)

                elif data == "EXIT":
                    break

    def NegaMax(self,board,move,turn,depth,alpha,beta,tilesearchrange):
        #print("CURRENT POSITION",move,isMaximizingPlayer)
        if WinChecker(board).CheckBoth() or depth == 0:
            #print("REACHED TERMINAL")
            return (Analyzer(board).Grader(self.AIStoneType)-Analyzer(board).Grader(self.EnemyStoneType),move)


        v = -10000000
        for moves in self.aiutils.GetOpenMovesPlus(board,self.OpenSearchRange):
            score = -self.NegaMax(self.aiutils.GenerateCustomGameBoard(board,moves,self.AIStoneType if turn == self.EnemyStoneType else self.EnemyStoneType),moves,self.AIStoneType if turn == self.EnemyStoneType else self.EnemyStoneType,depth-1,-beta,-alpha,tilesearchrange)[0]
            if score > v:
                v = score
            alpha = max(alpha,score)
            if alpha >= beta:
                print("AB CUTOFF")
                break

        return (v,move)





