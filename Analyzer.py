from main import AICore
from FilterStrings import Open2, Open3, Open4, Open5, Closed4, Open2Val, Open3Val, Open4Val, Closed4Val, Open5Val
import time

class Analyzer():
    def __init__(self, Board, template=None):
        self.Board = Board
        if not template:
            self.template = GetDefaultTemplate()
        else:
            self.template = template

    def ThreatSpaceSearch(self):
        pass

    def Parser(self, StoneType):
        FoundPatterns = []
        PassedStones = []
        MyStones = self.Board.BlackStones if StoneType == "black" else self.Board.WhiteStones
        EnemyStones = self.Board.WhiteStones if StoneType == "black" else self.Board.BlackStones
        print("Parser Start")
        EnemyStoneType = "white" if StoneType == "black" else "black"
        print("Stone type:", StoneType)
        # Check Vertical repetitions
        for y in range(1, self.Board.size[1] + 1):
            for x in range(1, self.Board.size[0] + 1):
                if (x,y) not in PassedStones and (x,y) in MyStones:
                    if (x,y-1) not in MyStones:
                        data = ""
                        for g in range(0,6):
                            if (x,y-1+g) in MyStones:
                                data += "o"
                                PassedStones.append((x,y-1+g))
                            elif (x,y-1+g) in EnemyStones: data += "x"
                            else: data += "-"

                        if data.count("o") >= 2:
                            FoundPatterns.append(data)
        # Check Horizontal repetitions
        PassedStones = []
        for x in range(1,self.Board.size[0]+1):
            for y in range(1,self.Board.size[1]+1):
                if (x,y) not in PassedStones and (x,y) in MyStones:
                    if (x-1,y) not in MyStones:
                        data = ""
                        for g in range(0,6):
                            if (x-1+g,y) in MyStones:
                                data += "o"
                                PassedStones.append((x-1+g, y))
                            elif (x-1+g,y) in EnemyStones:
                                data += "x"
                            else:
                                data += "-"

                        if data.count("o") >= 2:
                            FoundPatterns.append(data)
        PassedStones = []
        startpos_x = 1
        startpos_y = 1


        print(FoundPatterns)
        print("Parser End")
        return FoundPatterns

    def Grader(self, StoneType):
        score = 0
        print("Grader Start")
        print("Stone type:", StoneType)
        print("Running Parser")
        patterns = self.Parser(StoneType)
        for pattern in patterns:
            if pattern in Open2:
                print(pattern, "Open2   +", Open2Val)
                score += Open2Val
            elif pattern in Open3:
                print(pattern, "Open3   +", Open3Val)
                score += Open3Val
            elif pattern in Open4:
                print(pattern, "Open4   +", Open4Val)
                score += Open4Val
            elif pattern in Open5:
                print(pattern, "Open5   +", Open5Val)
                score += Open5Val
            elif pattern in Closed4:
                print(pattern, "Closed4 +", Closed4Val)
                score += Closed4Val
        print("Move score:", score)
        print("End Grader")
        return score

    def Get_8(self, Position):
        data = []
        for x, y in [(Position[0] + i, Position[1] + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0]:
            if x > self.Board.size[0] or x < 0 or y > self.Board.size[1] or y < 0:
                pass
            else:
                data.append((x, y))
        return data

def GetDefaultTemplate():
    pass

if __name__ == "__main__":
    starttime = time.time()
    ai = AICore()
    # ai.AddHumanStone((7,7))
    ai.Board.AddStone("black", (7, 6))
    ai.Board.AddStone("black", (7, 7))
    ai.Board.AddStone("black", (7, 8))
    ai.Board.AddStone("black", (7, 9))
    ai.Board.AddStone("black", (7, 10))
    ai.Board.AddStone("black", (6, 7))
    ai.Board.AddStone("black", (6, 8))
    ai.Board.AddStone("black", (6, 9))
    ai.Board.AddStone("black", (6, 10))
    ai.Board.AddStone("black", (8, 7))

    # ai.Board.AddStone("black", (8, 8))
    # ai.Board.AddStone("white", (7, 6))
    ai.Board.AddStone("white", (6, 6))
    print("Black:", ai.Board.BlackStones)
    print("White:", ai.Board.WhiteStones)
    heuristics = Analyzer(ai.Board)

    heuristics.Grader("black")
    endtime = time.time()
    print("Total calculation time:", endtime-starttime if not endtime-starttime == 0.0 else "0.0 (<0.0001 seconds)")