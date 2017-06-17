
from FilterStrings import Open2, Open3, Open4, Open5, Closed4, Open2Val, Open3Val, Open4Val, Closed4Val, Open5Val
import time


class Heuristics():
    def __init__(self,Board,aistonetype,debug=True):
        self.Board = Board
        self.debug = debug
        self.AIStoneType = aistonetype
    def GetValue(self,maximizingturn):
        if maximizingturn:
            return Analyzer(self.Board,debug=self.debug).Grader(self.AIStoneType)
        else:
            return -Analyzer(self.Board,debug=self.debug).Grader("white" if self.AIStoneType == "black" else "black")



class Analyzer():
    def __init__(self, Board,debug=False):
        self.Board = Board

        self.debug = debug


    def Parser(self, StoneType):
        """Current Execution time: O(n^2)
        I should try to minimize this"""
        FoundPatterns = []
        PassedStones = []
        MyStones = self.Board.BlackStones if StoneType == "black" else self.Board.WhiteStones
        EnemyStones = self.Board.WhiteStones if StoneType == "black" else self.Board.BlackStones
        if self.debug:
            print("Parser Start")
        EnemyStoneType = "white" if StoneType == "black" else "black"
        if self.debug:
            print("Stone type:", StoneType)

        # Check Vertical repetitions
        for y in range(1, self.Board.size[1] + 1):
            for x in range(1, self.Board.size[0] + 1):
                if (x,y) in MyStones and (x,y) not in PassedStones:
                    # print("vert mystone:",x,y)
                    data = ""
                    for g in range(0,6):
                        if (x,y-1+g) in MyStones and (x,y-1+g) not in PassedStones:
                            data += "o"
                            PassedStones.append((x,y-1+g))
                        elif (x,y-1+g) in EnemyStones:
                            data += "x"
                            if g != 0:
                                break    # This fixed the Problem!!!!! Push 9818399
                        elif y-1+g <= 0 or y-1+g > self.Board.size[1]:
                            data += "x"
                        elif (x,y-1+g) not in MyStones and (x,y-1+g) not in EnemyStones:
                            data += "-"

                    if data == "xooooo" or data == "-ooooo":
                        if (x,y+5) in MyStones:

                            checker_increment = 0
                            while True:
                                if (x,y+checker_increment+1) in MyStones:
                                    checker_increment += 1
                                else:
                                    break
                            for value in range(0,checker_increment):
                                PassedStones.append((x,y+value))
                            if self.debug:
                                print("open6+ vert", x, y,"to",x,y+checker_increment)

                        else:
                            if self.debug:
                                print("open5 vert",x,y)
                            if data.count("o") >=2:
                                FoundPatterns.append(data)
                    else:
                        if data.count("o") >= 2:
                            FoundPatterns.append(data)

        # print("vert Passedstones:",PassedStones)

        # Check Horizontal repetitions
        PassedStones = []
        for x in range(1,self.Board.size[0]+1):
            for y in range(1,self.Board.size[1]+1):
                if (x,y) in MyStones and (x,y) not in PassedStones:
                    # print("hori mystone:",x,y)
                    data = ""
                    for g in range(0,6):
                        if (x-1+g,y) in MyStones and (x-1+g,y) not in PassedStones:
                            data += "o"
                            PassedStones.append((x-1+g, y))
                        elif (x-1+g,y) in EnemyStones:
                            data += "x"
                            if g != 0:
                                break    # This fixed the Problem!!!!! Push 9818399
                        elif x-1+g <=0 or x-1+g > self.Board.size[0]:
                            data += "x"
                        elif (x-1+g, y) not in MyStones and (x-1+g, y) not in EnemyStones:
                            data += "-"

                    if data == "xooooo" or data == "-ooooo":
                        if (x+5,y) in MyStones:

                            checker_increment = 0
                            while True:
                                if (x+checker_increment+1,y) in MyStones:
                                    checker_increment += 1
                                else:
                                    break
                            for value in range(0, checker_increment):
                                PassedStones.append((x+value,y))
                            if self.debug:
                                print("open6+ hori", x, y, "to", x+checker_increment, y)
                        else:
                            if self.debug:
                                print("open5 hori",x,y)
                            if data.count("o") >= 2:
                                FoundPatterns.append(data)
                    else:
                        if data.count("o") >= 2:
                            FoundPatterns.append(data)

        # print("Hori PassedStones:",PassedStones)
        PassedStones = []

        # check 2o`clock diagonal from 1,1 repetitions
        for x in range(1, self.Board.size[0] + 1):  # other half of board
            for y in range(0, x):  # stone coord: (x-y,y+1)
                if (x-y,y+1) in MyStones and (x-y,y+1) not in PassedStones:
                    data = ""
                    for g in range(0,6):
                        if (x-y-1+g,y+1-1+g) in MyStones and (x-y-1+g,y+1-1+g) not in PassedStones:
                            data += "o"
                            PassedStones.append((x-y-1+g,y+1-1+g))
                        elif (x-y-1+g,y+1-1+g) in EnemyStones:
                            data += "x"
                            if g != 0:
                                break
                        elif x-y-1+g <= 0 or x-y-1+g > self.Board.size[0] or y+1-1+g <= 0 or y+1-1+g > self.Board.size[1]:
                            data += "x"
                        elif (x-y-1+g,y+1-1+g) not in MyStones and (x-y-1+g,y+1-1+g) not in EnemyStones:
                            data += "-"

                    if data == "xooooo" or data == "-ooooo":
                        if (x-y+5,y+1+5) in MyStones:
                            checker_increment = 0

                            while True:
                                if (x-y+checker_increment+1,y+1+checker_increment+1) in MyStones:
                                    checker_increment += 1
                                else:
                                    break
                            for value in range(0,checker_increment):
                                PassedStones.append((x-y+value,y+1+value))
                            if self.debug:
                                print("open6+ diag2",x-y,y+1,"to",x-y+checker_increment,y+1+checker_increment)
                        else:
                            if self.debug:
                                print("open5 diag2",x-y,y+1)
                            if data.count("o") >= 2:
                                FoundPatterns.append(data)
                    else:
                        if data.count("o") >= 2:
                            FoundPatterns.append(data)
                # print(x - y, y + 1)
        PassedStones = []

        # check 5o`clock diagonal from 1,13 to 13,1 repetitions
        for x in range(1, self.Board.size[0] + 1):
            for y in range(self.Board.size[1], self.Board.size[1] - x, -1): # stone coord(x-self.Board.size[1]+y,y),but each time in g traverse, sub from y and add to x
                if (x-self.Board.size[1]+y,y) in MyStones and (x-self.Board.size[1]+y,y) not in PassedStones:
                    data = ""
                    for g in range(0,6):
                        if (x-self.Board.size[1]+y-1+g,y+1-g) in MyStones and (x-self.Board.size[1]+y-1+g,y+1-g) not in PassedStones:
                            data += "o"
                            PassedStones.append((x-self.Board.size[1]+y-1+g,y+1-g))
                        elif (x-self.Board.size[1]+y-1+g,y+1-g) in EnemyStones:
                            data += "x"
                            if g != 0:
                                break
                        elif x-self.Board.size[1]+y-1+g <= 0 or x-self.Board.size[1]+y-1+g > self.Board.size[0] or y+1-g <= 0 or y+1-g > self.Board.size[1]:
                            data += "x"
                        elif (x-self.Board.size[1]+y-1+g,y+1-g) not in MyStones and (x-self.Board.size[1]+y-1+g,y+1-g) not in EnemyStones:
                            data += "-"

                    if data == "xooooo" or data == "-ooooo":
                        if (x-self.Board.size[1]+y+5,y-5) in MyStones:
                            checker_increment = 0

                            while True:
                                if (x-self.Board.size[1]+y+checker_increment+1,y-checker_increment-1) in MyStones:
                                    checker_increment += 1
                                else:
                                    break
                            for value in range(0,checker_increment):
                                PassedStones.append((x-self.Board.size[1]+y+checker_increment,y-checker_increment))
                            if self.debug:
                                print("open6+ diag5",x-self.Board.size[1]+y,y,"to",x-self.Board.size[1]+y+checker_increment,y-checker_increment)
                        else:
                            if self.debug:
                                print("open5 diag5",x-self.Board.size[1]+y,y)
                            if data.count("o") >= 2:
                                FoundPatterns.append(data)
                    else:
                        if data.count("o") >= 2:
                            FoundPatterns.append(data)
                # print(x, y + (self.Board.size[1] - x))

        for y in range(1, self.Board.size[1]):  # other half of board
            for x in range(self.Board.size[0],y, -1):  # stone coord(x,x-y),but each time in g traverse, sub from y and add to x
                if (x,x-y) in MyStones and (x,x-y) not in PassedStones:
                    data = ""
                    for g in range(0,6):
                        if (x-1+g,x-y+1-g) in MyStones and (x-1+g,x-y+1-g) not in PassedStones:
                            data += "o"
                            PassedStones.append((x-1+g,x-y+1-g))
                        elif (x-1+g,x-y+1-g) in EnemyStones:
                            data += "x"
                            if g != 0:
                                break
                        elif x-1+g <= 0 or x-1+g > self.Board.size[0] or x-y+1-g <= 0 or x-y+1-g > self.Board.size[1]:
                            data += "x"
                        elif (x-1+g,x-y+1-g) not in MyStones and (x-1+g,x-y+1-g) not in EnemyStones:
                            data += "-"

                    if data == "xooooo" or data == "-ooooo":
                        if (x+5,x-y+5) in MyStones:
                            checker_increment = 0

                            while True:
                                if (x+checker_increment+1,x-y-checker_increment-1) in MyStones:
                                    checker_increment += 1
                                else:
                                    break
                            for value in range(0,checker_increment):
                                PassedStones.append((x+checker_increment,x-y-checker_increment))
                            if self.debug:
                                print("open6+ diag5",x,x-y,"to",x+checker_increment,x-y-checker_increment)
                        else:
                            if self.debug:
                                print("open5 diag5",x,x-y)
                            if data.count("o") >= 2:
                                FoundPatterns.append(data)
                    else:
                        if data.count("o") >= 2:
                            FoundPatterns.append(data)
                # print(x, y + (self.Board.size[1] - x))

        if self.debug:
            print(FoundPatterns)
            print("Parser End")
        return FoundPatterns

    def Grader(self, StoneType):
        score = 0
        if self.debug:
            print("Grader Start")
            print("Stone type:", StoneType)
            print("Running Parser")
        patterns = self.Parser(StoneType)
        for pattern in patterns:
            if pattern in Open2:
                if self.debug:
                    print(pattern, "Open2   +", Open2Val)
                score += Open2Val
            elif pattern in Open3:
                if self.debug:
                    print(pattern, "Open3   +", Open3Val)
                score += Open3Val
            elif pattern in Open4:
                if self.debug:
                    print(pattern, "Open4   +", Open4Val)
                score += Open4Val
            elif pattern in Open5:
                if self.debug:
                    print(pattern, "Open5   +", Open5Val)
                score += Open5Val
            elif pattern in Closed4:
                if self.debug:
                    print(pattern, "Closed4 +", Closed4Val)
                score += Closed4Val
        if self.debug:
            print("Move score:", score)
            print("Grader End")
        return score

    def Get_8(self, Position):
        data = []
        for x, y in [(Position[0] + i, Position[1] + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0]:
            if x > self.Board.size[0] or x < 0 or y > self.Board.size[1] or y < 0:
                pass
            else:
                data.append((x, y))
        return data


class AdvancedAnalyzer():
    def __init__(self, Board, debug=False):
        self.Board = Board

        self.debug = debug

    def Parser(self, StoneType):
        """Current Execution time: O(n^2)
        I should try to minimize this"""
        FoundPatterns = []
        PassedStones = []
        MyStones = self.Board.BlackStones if StoneType == "black" else self.Board.WhiteStones
        EnemyStones = self.Board.WhiteStones if StoneType == "black" else self.Board.BlackStones
        if self.debug:
            print("Parser Start")
        EnemyStoneType = "white" if StoneType == "black" else "black"
        if self.debug:
            print("Stone type:", StoneType)

        # Check Vertical repetitions
        for y in range(1, self.Board.size[1] + 1):
            for x in range(1, self.Board.size[0] + 1):
                if (x, y) in MyStones and (x, y) not in PassedStones:
                    # print("vert mystone:",x,y)
                    data = ""
                    for g in range(0, 6):
                        if (x, y - 1 + g) in MyStones and (x, y - 1 + g) not in PassedStones:
                            data += "o"
                            PassedStones.append((x, y - 1 + g))
                        elif (x, y - 1 + g) in EnemyStones:
                            data += "x"
                            if g != 0:
                                break  # This fixed the Problem!!!!! Push 9818399
                        elif y - 1 + g <= 0 or y - 1 + g > self.Board.size[1]:
                            data += "x"
                        elif (x, y - 1 + g) not in MyStones and (x, y - 1 + g) not in EnemyStones:
                            data += "-"

                    if data == "xooooo" or data == "-ooooo":
                        if (x, y + 5) in MyStones:

                            checker_increment = 0
                            while True:
                                if (x, y + checker_increment + 1) in MyStones:
                                    checker_increment += 1
                                else:
                                    break
                            for value in range(0, checker_increment):
                                PassedStones.append((x, y + value))
                            if self.debug:
                                print("open6+ vert", x, y, "to", x, y + checker_increment)

                        else:
                            if self.debug:
                                print("open5 vert", x, y)
                            if data.count("o") >= 2:
                                FoundPatterns.append((data,(x,y),"vert"))
                    else:
                        if data.count("o") >= 2:
                            FoundPatterns.append((data,(x,y),"vert"))

        # print("vert Passedstones:",PassedStones)

        # Check Horizontal repetitions
        PassedStones = []
        for x in range(1, self.Board.size[0] + 1):
            for y in range(1, self.Board.size[1] + 1):
                if (x, y) in MyStones and (x, y) not in PassedStones:
                    # print("hori mystone:",x,y)
                    data = ""
                    for g in range(0, 6):
                        if (x - 1 + g, y) in MyStones and (x - 1 + g, y) not in PassedStones:
                            data += "o"
                            PassedStones.append((x - 1 + g, y))
                        elif (x - 1 + g, y) in EnemyStones:
                            data += "x"
                            if g != 0:
                                break  # This fixed the Problem!!!!! Push 9818399
                        elif x - 1 + g <= 0 or x - 1 + g > self.Board.size[0]:
                            data += "x"
                        elif (x - 1 + g, y) not in MyStones and (x - 1 + g, y) not in EnemyStones:
                            data += "-"

                    if data == "xooooo" or data == "-ooooo":
                        if (x + 5, y) in MyStones:

                            checker_increment = 0
                            while True:
                                if (x + checker_increment + 1, y) in MyStones:
                                    checker_increment += 1
                                else:
                                    break
                            for value in range(0, checker_increment):
                                PassedStones.append((x + value, y))
                            if self.debug:
                                print("open6+ hori", x, y, "to", x + checker_increment, y)
                        else:
                            if self.debug:
                                print("open5 hori", x, y)
                            if data.count("o") >= 2:
                                FoundPatterns.append((data,(x,y),"hori"))
                    else:
                        if data.count("o") >= 2:
                            FoundPatterns.append((data,(x,y),"hori"))

        # print("Hori PassedStones:",PassedStones)
        PassedStones = []

        # check 2o`clock diagonal from 1,1 repetitions
        for x in range(1, self.Board.size[0] + 1):  # other half of board
            for y in range(0, x):  # stone coord: (x-y,y+1)
                if (x - y, y + 1) in MyStones and (x - y, y + 1) not in PassedStones:
                    data = ""
                    for g in range(0, 6):
                        if (x - y - 1 + g, y + 1 - 1 + g) in MyStones and (
                                    x - y - 1 + g, y + 1 - 1 + g) not in PassedStones:
                            data += "o"
                            PassedStones.append((x - y - 1 + g, y + 1 - 1 + g))
                        elif (x - y - 1 + g, y + 1 - 1 + g) in EnemyStones:
                            data += "x"
                            if g != 0:
                                break
                        elif x - y - 1 + g <= 0 or x - y - 1 + g > self.Board.size[
                            0] or y + 1 - 1 + g <= 0 or y + 1 - 1 + g > self.Board.size[1]:
                            data += "x"
                        elif (x - y - 1 + g, y + 1 - 1 + g) not in MyStones and (
                                    x - y - 1 + g, y + 1 - 1 + g) not in EnemyStones:
                            data += "-"

                    if data == "xooooo" or data == "-ooooo":
                        if (x - y + 5, y + 1 + 5) in MyStones:
                            checker_increment = 0

                            while True:
                                if (x - y + checker_increment + 1, y + 1 + checker_increment + 1) in MyStones:
                                    checker_increment += 1
                                else:
                                    break
                            for value in range(0, checker_increment):
                                PassedStones.append((x - y + value, y + 1 + value))
                            if self.debug:
                                print("open6+ diag2", x - y, y + 1, "to", x - y + checker_increment,
                                      y + 1 + checker_increment)
                        else:
                            if self.debug:
                                print("open5 diag2", x - y, y + 1)
                            if data.count("o") >= 2:
                                FoundPatterns.append((data,(x-y,y+1),"diag2"))
                    else:
                        if data.count("o") >= 2:
                            FoundPatterns.append((data,(x-y,y+1),"diag2"))
                            # print(x - y, y + 1)
        PassedStones = []

        # check 5o`clock diagonal from 1,13 to 13,1 repetitions
        for x in range(1, self.Board.size[0] + 1):
            for y in range(self.Board.size[1], self.Board.size[1] - x,
                           -1):  # stone coord(x-self.Board.size[1]+y,y),but each time in g traverse, sub from y and add to x
                if (x - self.Board.size[1] + y, y) in MyStones and (x - self.Board.size[1] + y, y) not in PassedStones:
                    data = ""
                    for g in range(0, 6):
                        if (x - self.Board.size[1] + y - 1 + g, y + 1 - g) in MyStones and (
                                        x - self.Board.size[1] + y - 1 + g, y + 1 - g) not in PassedStones:
                            data += "o"
                            PassedStones.append((x - self.Board.size[1] + y - 1 + g, y + 1 - g))
                        elif (x - self.Board.size[1] + y - 1 + g, y + 1 - g) in EnemyStones:
                            data += "x"
                            if g != 0:
                                break
                        elif x - self.Board.size[1] + y - 1 + g <= 0 or x - self.Board.size[1] + y - 1 + g > \
                                self.Board.size[0] or y + 1 - g <= 0 or y + 1 - g > self.Board.size[1]:
                            data += "x"
                        elif (x - self.Board.size[1] + y - 1 + g, y + 1 - g) not in MyStones and (
                                        x - self.Board.size[1] + y - 1 + g, y + 1 - g) not in EnemyStones:
                            data += "-"

                    if data == "xooooo" or data == "-ooooo":
                        if (x - self.Board.size[1] + y + 5, y - 5) in MyStones:
                            checker_increment = 0

                            while True:
                                if (x - self.Board.size[1] + y + checker_increment + 1,
                                    y - checker_increment - 1) in MyStones:
                                    checker_increment += 1
                                else:
                                    break
                            for value in range(0, checker_increment):
                                PassedStones.append(
                                    (x - self.Board.size[1] + y + checker_increment, y - checker_increment))
                            if self.debug:
                                print("open6+ diag5", x - self.Board.size[1] + y, y, "to",
                                      x - self.Board.size[1] + y + checker_increment, y - checker_increment)
                        else:
                            if self.debug:
                                print("open5 diag5", x - self.Board.size[1] + y, y)
                            if data.count("o") >= 2:
                                FoundPatterns.append((data,(x-self.Board.size[1]+y,y),"diag5"))
                    else:
                        if data.count("o") >= 2:
                            FoundPatterns.append((data,(x-self.Board.size[1]+y,y),"diag5"))
                            # print(x, y + (self.Board.size[1] - x))

        for y in range(1, self.Board.size[1]):  # other half of board
            for x in range(self.Board.size[0], y,
                           -1):  # stone coord(x,x-y),but each time in g traverse, sub from y and add to x
                if (x, x - y) in MyStones and (x, x - y) not in PassedStones:
                    data = ""
                    for g in range(0, 6):
                        if (x - 1 + g, x - y + 1 - g) in MyStones and (x - 1 + g, x - y + 1 - g) not in PassedStones:
                            data += "o"
                            PassedStones.append((x - 1 + g, x - y + 1 - g))
                        elif (x - 1 + g, x - y + 1 - g) in EnemyStones:
                            data += "x"
                            if g != 0:
                                break
                        elif x - 1 + g <= 0 or x - 1 + g > self.Board.size[0] or x - y + 1 - g <= 0 or x - y + 1 - g > \
                                self.Board.size[1]:
                            data += "x"
                        elif (x - 1 + g, x - y + 1 - g) not in MyStones and (
                                x - 1 + g, x - y + 1 - g) not in EnemyStones:
                            data += "-"

                    if data == "xooooo" or data == "-ooooo":
                        if (x + 5, x - y + 5) in MyStones:
                            checker_increment = 0

                            while True:
                                if (x + checker_increment + 1, x - y - checker_increment - 1) in MyStones:
                                    checker_increment += 1
                                else:
                                    break
                            for value in range(0, checker_increment):
                                PassedStones.append((x + checker_increment, x - y - checker_increment))
                            if self.debug:
                                print("open6+ diag5", x, x - y, "to", x + checker_increment, x - y - checker_increment)
                        else:
                            if self.debug:
                                print("open5 diag5", x, x - y)
                            if data.count("o") >= 2:
                                FoundPatterns.append((data,(x,x-y),"diag5"))
                    else:
                        if data.count("o") >= 2:
                            FoundPatterns.append((data,(x,x-y),"diag5"))
                            # print(x, y + (self.Board.size[1] - x))

        if self.debug:
            print(FoundPatterns)
            print("Parser End")
        return FoundPatterns

class WinChecker(Analyzer):
    def __init__(self, Board,debug=False):
        super().__init__(Board,debug)





    def Check(self, StoneType):
        """Check if a 5x exists for StoneType in self.GameBoard. Pretty much a copy of Analyzer() :p"""
        FoundPatterns = super().Parser(StoneType)
        for pattern in FoundPatterns:
            if pattern in Open5:
                return True
            else:
                pass



if __name__ == "__main__":
    #from Tester import RandomPopulate
    from main import GameBoard
    starttime = time.time()
    board = GameBoard(13,13)

    board.AddStone("black", (7, 6))
    board.AddStone("black", (7, 7))
    board.AddStone("black", (7, 8))
    board.AddStone("black", (7, 9))
    board.AddStone("white",(7,5))
    """board.AddStone("black", (7, 10))
    board.AddStone("black", (6, 7))
    board.AddStone("black", (6, 8))
    board.AddStone("black", (6, 9))
    board.AddStone("black", (6, 10))
    board.AddStone("black", (8, 7))

    board.AddStone("black", (8, 8))
    board.AddStone("black", (7, 11))
    board.AddStone("white", (6, 6))"""
    #RandomPopulate(board)
    print("Black:", board.BlackStones)
    print("White:", board.WhiteStones)
    heuristics = AdvancedAnalyzer(board)

    print(heuristics.Parser("black"))
    endtime = time.time()
    print("Total calculation time:", endtime-starttime if not endtime-starttime == 0.0 else "0.0 (<0.0001 seconds)")
    from GomokuBoardUI import GomokuBoard
    from tkinter import Tk
    root = Tk()
    UIboard = GomokuBoard(board, root)
    UIboard.Draw()
    root.mainloop()