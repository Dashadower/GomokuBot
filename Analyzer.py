from main import AICore

class Analyzer():
    def __init__(self, Board, template=None):
        self.Board = Board
        if not template:
            self.template = GetDefaultTemplate()
        else:
            self.template = template

    def ThreatSpaceSearch(self):
        pass
    def Analyze(self, StoneType):
        FoundPatterns = []
        PassedStones = []
        Open3 = 0
        BlackStones = self.Board.BlackStones
        WhiteStones = self.Board.WhiteStones
        if StoneType == "black":
            # Check Vertical repetitions
            for y in range(1, self.Board.size[1] + 1):
                for x in range(1, self.Board.size[0] + 1):
                    if (x,y) not in PassedStones and (x,y) in BlackStones:
                        if (x,y-1) not in WhiteStones and (x,y-1) not in BlackStones:
                            data = ""
                            pos = []
                            for g in range(0,6):
                                if (x,y-1+g) in BlackStones:
                                    data += "o"
                                    PassedStones.append((x,y-1+g))
                                elif (x,y-1+g) in WhiteStones: data += "x"
                                else: data += " "

                            if data.count("o") >= 2:
                                FoundPatterns.append(data)
            # Check Horizontal repetitions
            PassedStones = []
            for x in range(1,self.Board.size[0]+1):
                for y in range(1,self.Board.size[1]+1):
                    if (x,y) not in PassedStones and (x,y) in BlackStones:
                        if (x-1,y) not in WhiteStones and (x-1,y) not in BlackStones:
                            data = ""
                            pos = []
                            for g in range(0,6):
                                if (x-1+g,y) in BlackStones:
                                    data += "o"
                                    PassedStones.append((x-1+g, y))
                                elif (x-1+g,y) in WhiteStones: data += "x"
                                else: data += " "

                            if data.count("o") >= 2:
                                FoundPatterns.append(data)

        return FoundPatterns

    def Lexer(self):
        pass
    def get_8(self, Position):
        data = []
        for x, y in [(Position[0] + i, Position[1] + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0]:
            if x > self.Board.size[0] or x < 0 or y > self.Board.size[1] or y < 0:
                pass
            else:
                data.append((x, y))
        return data

def GetDefaultTemplate():
    pass

ai = AICore()
# ai.AddHumanStone((7,7))
ai.Board.AddStone("black", (7, 7))
ai.Board.AddStone("black", (7, 8))
ai.Board.AddStone("black", (7, 9))
ai.Board.AddStone("black", (7, 10))
ai.Board.AddStone("black", (6, 7))
ai.Board.AddStone("black", (6, 8))
ai.Board.AddStone("black", (6, 10))
ai.Board.AddStone("black", (8, 7))
#ai.Board.AddStone("black", (8, 8))

ai.Board.AddStone("white", (6, 6))
print("Black:",ai.Board.BlackStones)
heuristics = Analyzer(ai.Board)
print(heuristics.Analyze("black"))