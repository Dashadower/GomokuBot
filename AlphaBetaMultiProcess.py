from AICore import AICore
from main import GameBoard
from Analyzer import Analyzer,WinChecker
import time, random, multiprocessing
from collections import Counter
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

        moves = self.GetOpenMovesPlus(self.Board,self.OpenSearchRange)
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

def compare(s, t):
    return Counter(s) == Counter(t)

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
                        """self.HashTable = []
                        for ply in range(1,self.PlyDepth+1):
                            result = self.AlphaBeta(board,coord,ply,False,-10000000,10000000,self.OpenSearchRange)
                            print("PLY",ply,"COMPLETE",result,len(self.HashTable))"""
                        result = self.AlphaBeta(board, coord, self.PlyDepth, False, -10000000, 10000000, self.OpenSearchRange)
                        self.ControlQueue.put((result[0],coord))
                elif data == "EXIT":
                    break

    def AlphaBeta(self,board,move,depth,isMaximizingPlayer,alpha,beta,tilesearchrange):
        #print("CURRENT POSITION",move,isMaximizingPlayer)
        if WinChecker(board).CheckBoth() or depth == 0:
            #print("REACHED TERMINAL")
            """matched = False
            for items in self.HashTable:

                if compare(board.BlackStones,items[0][0]) and compare(board.WhiteStones,items[0][1]):
                    if items[2] >= depth - 1:
                        heuristicdata = items[1]
                        matched = True
                        break
                    else:
                        self.HashTable.remove(items)
                        heuristicdata = Analyzer(board).Grader(self.AIStoneType) - Analyzer(board).Grader(self.EnemyStoneType)
                        self.HashTable.append([[board.BlackStones, board.WhiteStones], heuristicdata, depth])
                        matched = True
                        break
            if not matched:
                heuristicdata = Analyzer(board).Grader(self.AIStoneType)-Analyzer(board).Grader(self.EnemyStoneType)
                self.HashTable.append([[board.BlackStones,board.WhiteStones],heuristicdata,depth])"""
            heuristicdata = Analyzer(board).Grader(self.AIStoneType) - Analyzer(board).Grader(self.EnemyStoneType)
            return (heuristicdata,move)

        if isMaximizingPlayer:
            v = -10000000
            for moves in self.aiutils.GetOpenMovesPlus(board,self.OpenSearchRange):
                v = max(v,self.AlphaBeta(self.aiutils.GenerateCustomGameBoard(board,moves,self.AIStoneType),moves,depth-1,False, alpha,beta,tilesearchrange)[0])
                alpha = max(alpha,v)
                if beta <= alpha:
                    print("BETA CUTOFF")
                    break
            return (v,move)
        else:
            v = 10000000
            for moves in self.aiutils.GetOpenMovesPlus(board,self.OpenSearchRange):
                v = min(v,self.AlphaBeta(self.aiutils.GenerateCustomGameBoard(board,moves,self.EnemyStoneType),moves,depth-1,True,alpha,beta,tilesearchrange)[0])
                beta = min(beta,v)
                if beta <= alpha:
                    print("ALPHA CUTOFF")
                    break
            return (v,move)




