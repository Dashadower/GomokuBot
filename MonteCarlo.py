from AICore import AICore
from Analyzer import Heuristics, WinChecker

class MonteCarlo(AICore):
    def __init__(self, board=None, aistoneType="white",timelimit=10,threads=1):
        self.timelimit = timelimit
        self.threads = threads
        AICore.__init__(self,board,aistoneType)
        if self.AIStoneType == "black":
            self.AddAIStone((round(self.Board.size[0]/2),round(self.Board.size[1]/2)))

    def ChooseMove(self):
