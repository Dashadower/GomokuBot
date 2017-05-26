from AICore import AICore
from Analyzer import Heuristics, WinChecker
import math
class MonteCarlo(AICore):
    def __init__(self, board=None, aistoneType="white", timelimit=10,threads=1):
        self.timelimit = timelimit
        self.threads = threads
        AICore.__init__(board,aistoneType)
        AICore.__init__(self,board,aistoneType)
        if self.AIStoneType == "black":
            self.AddAIStone((round(self.Board.size[0]/2),round(self.Board.size[1]/2)))

    def ChooseMove(self):
        pass

def UCT(wi, ni, t, c=math.sqrt(2)):
    """UCT SELECTION FUNCTION
    wi : number of wins after ith move
    ni : number of simulations after ith move
    c  : exploration parameter. default is sqrt(2)
    t  : total number of simulations (ni of parents node) sum of all ni"""
    return wi/ni + c*math.sqrt(math.log(t)/ni)