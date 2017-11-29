from AICore import AICore
from main import GameBoard
from Analyzer import Analyzer,WinChecker
import time, random, multiprocessing
from collections import Counter

class AlphaBeta(AICore):
    def __init__(self,initialgamestate,aistonetype, plydepth,tilesearchrange):
        AICore.__init__(self, initialgamestate, aistonetype,tilesearchrange)
        self.EnemyStoneType = "black" if self.AIStoneType == "white" else "white"
        self.PlyDepth = plydepth
        self.ControlQueue = multiprocessing.Queue()
        self.OpenSearchRange = tilesearchrange

        self.ReportHook = print
        self.Process = None
        self.CommQueue = None
        self.datalist = []
        self.PID = None
    def InitiateProcess(self):

        q = multiprocessing.Queue()

        self.CommQueue = q
        p = multiprocessing.Process(target=AlphaBetaActuator, args=(self.ControlQueue,q, self.AIStoneType, self.PlyDepth, self.OpenSearchRange))
        p.daemon = True
        self.Process = p
        p.start()
        self.PID = p.pid

        return (self.Process,self.PID)
    def ChooseMove(self):
        moves = self.GetOpenMovesPlus(self.Board, self.OpenSearchRange)
        startedprocesses = len(moves)
        self.ReportHook("1PLY 검색 타일 수:"+str(startedprocesses))
        #gboard = self.GenerateCustomGameBoard(self.Board,coord,self.AIStoneType)
        self.CommQueue.put(("START",self.Board))


    def GetResult(self):
        try:
            data = self.ControlQueue.get_nowait()
        except:
            return False
        else:
            if data:
                return data
            else:
                return False

class Node():
        def __init__(self, position, value, parent):
            self.position = position
            self.value = value
            self.parent = parent
            self.children = []
            if self.parent:
               self.parent.register_child(self)
        def register_child(self, node):
            self.children.append(node)
            node.parent = self


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
            if data[0] == "START":
                board = data[1]
                self.aiutils = AICore(board, self.AIStoneType, self.OpenSearchRange)
                startnode = Node(None, None, None)
                result = self.AlphaBeta(self.aiutils.DuplicateBoard(board),startnode, self.PlyDepth, True,-10000000, 10000000, self.OpenSearchRange)
                print("*"*10)
                print(len(startnode.children))
                result = []
                for items in startnode.children:
                    print(items.position, items.value)
                    result.append((items.position, items.value))
                result = sorted(result,key=lambda x:x[1],reverse=True)
                print("RESULT:",result)
                self.ControlQueue.put(result[0][0])
    def AlphaBeta(self,board,node,depth,isMaximizingPlayer,alpha,beta,tilesearchrange):
        #print("CURRENT POSITION",move,isMaximizingPlayer)
        if WinChecker(board).CheckBoth() or depth == 0:
            ganalyst = Analyzer(board)
            return (ganalyst.Grader(self.AIStoneType if isMaximizingPlayer else self.EnemyStoneType)-ganalyst.Grader(self.EnemyStoneType if isMaximizingPlayer else self.AIStoneType))

        if isMaximizingPlayer:
            v = -10000000
            for moves in self.aiutils.GetOpenMovesPlus(board,self.OpenSearchRange):
                g = Node(moves, None, node)
                v = max(v,self.AlphaBeta(self.aiutils.GenerateCustomGameBoard(board,moves,self.AIStoneType),g,depth-1,False, alpha,beta,tilesearchrange))
                g.value = v
                alpha = max(alpha,v)
                if beta <= alpha:
                    #print("BETA CUTOFF")
                    break
            return v
        else:
            v = 10000000
            for moves in self.aiutils.GetOpenMovesPlus(board,self.OpenSearchRange):
                g = Node(moves, None, node)
                v = min(v,self.AlphaBeta(self.aiutils.GenerateCustomGameBoard(board,moves,self.EnemyStoneType),g,depth-1,True,alpha,beta,tilesearchrange))
                g.value = v
                beta = min(beta,v)
                if beta <= alpha:
                    #print("ALPHA CUTOFF")
                    break
            return v












