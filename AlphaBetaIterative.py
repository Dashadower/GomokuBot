from AICore import AICore
from collections import Counter
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

def random_number():
    return random.randint(1,99999)
def random_matrix(board):
    randoms = []
    for x in range(0,board.size[0]):
        randoms.append([])
        for y in range(0,board.size[1]):

            rarr = [random_number(),random_number(),random_number()]
            randoms[x].append(rarr)
    randoms.insert(len(randoms),[random_number(),random_number()])
    return randoms
def Zobrist_Hash(board,matrix,isMaxmizing):
    board_hash = 0
    for x in range(1,board.size[0]+1):
        for y in range(1,board.size[1]+1):
            if (x,y) in board.BlackStones:
                piece = 1
            elif (x,y) in board.WhiteStones:
                piece = 2
            else:
                piece = 0
            board_hash ^= matrix[x-1][y-1][piece]
    if isMaxmizing:
        board_hash ^= matrix[len(matrix)-1][0]
    elif not isMaxmizing:
        board_hash ^= matrix[len(matrix)-1][1]
    return board_hash
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
                    self.RandomMatrix = random_matrix(data[1])
                    openmoves = self.aiutils.GetOpenMovesPlus(data[1],self.OpenSearchRange)
                    for moves in openmoves:
                        if len(openmoves) >= 30:
                            print("ZOBRIST MODE")
                            self.HashTable = []

                            for x in range(1,self.PlyDepth+1):
                                result = self.HashedAlphaBeta(self.aiutils.GenerateCustomGameBoard(self.aiutils.DuplicateBoard(data[1]),moves,self.AIStoneType),moves,x,False,-10000000,10000000,self.OpenSearchRange)
                        else:
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

    def HashedAlphaBeta(self,board,move,depth,isMaximizingPlayer,alpha,beta,tilesearchrange):
        #print("CURRENT POSITION",move,isMaximizingPlayer)
        if WinChecker(board).CheckBoth() or depth == 0:
            found = False
            zhash = Zobrist_Hash(board, self.RandomMatrix, isMaximizingPlayer)
            for item in self.HashTable:
                if item[0] == zhash:
                    if item[1] <= depth+1:
                        analysisresult = item[1]
                        found = True
                        break
                    else:
                        self.HashTable.remove(item)
                        break
            if not found:
                analysisresult = int(Analyzer(board).Grader(self.AIStoneType) - Analyzer(board).Grader(self.EnemyStoneType))

                self.HashTable.append((zhash,analysisresult,depth))

            return (analysisresult, move)

        if isMaximizingPlayer:
            v = -10000000
            for moves in self.aiutils.GetOpenMovesPlus(board,self.OpenSearchRange):
                newboard = self.aiutils.GenerateCustomGameBoard(board,moves,self.AIStoneType)
                zhash = Zobrist_Hash(newboard,self.RandomMatrix,True)
                found = False
                for item in self.HashTable:
                    if item[0] == zhash:
                        if item[1] <= depth + 1:
                            analysisresult = item[1]
                            found = True
                            break
                        else:
                            break
                if not found:
                    analysisresult = self.AlphaBeta(newboard,moves,depth-1,False,alpha,beta,tilesearchrange)[0]
                v = max(v,analysisresult)
                alpha = max(alpha,v)
                if beta <= alpha:
                    #print("BETA CUTOFF")
                    break
            return (v,move)
        else:
            v = 10000000
            for moves in self.aiutils.GetOpenMovesPlus(board,self.OpenSearchRange):
                newboard = self.aiutils.GenerateCustomGameBoard(board, moves, self.AIStoneType)
                zhash = Zobrist_Hash(newboard, self.RandomMatrix, False)
                found = False
                for item in self.HashTable:
                    if item[0] == zhash:
                        if item[1] <= depth + 1:
                            analysisresult = item[1]
                            found = True
                            break
                        else:
                            break
                if not found:
                    analysisresult = self.AlphaBeta(newboard, moves, depth - 1, True, alpha, beta, tilesearchrange)[0]
                v = min(v,analysisresult)
                beta = min(beta,v)
                if beta <= alpha:
                    #print("ALPHA CUTOFF")
                    break
            return (v,move)




