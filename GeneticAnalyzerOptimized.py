from FilterStrings import Open2, Open3, Open4, Open5, Closed4, Open2Val, Open3Val, Open4Val, Closed4Val, Open5Val
class Analyzer():
    def __init__(self, Board,Open2Val,Open3Val,Open4Val,Closed4Val):
        self.Board = Board

        self.Open2Val = Open2Val
        self.Open3Val = Open3Val
        self.Open4Val = Open4Val
        self.Closed4Val = Closed4Val


    def Grader(self, StoneType):
        """Current Execution time: O(n^2)
        I should try to minimize this"""
        score = 0
        PassedStones = []
        MyStones = self.Board.BlackStones if StoneType == "black" else self.Board.WhiteStones
        EnemyStones = self.Board.WhiteStones if StoneType == "black" else self.Board.BlackStones



        # Check Vertical repetitions
        for stone in sorted(MyStones,key=lambda x:x[1]):
            x,y = stone
            if (x,y) not in PassedStones:
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
                        data += "w"
                    elif (x,y-1+g) not in MyStones and (x,y-1+g) not in EnemyStones:
                        data += "-"

                if data == "xooooo" or data == "-ooooo" or data == "wooooo":
                    if (x,y+5) in MyStones:

                        checker_increment = 0
                        while True:
                            if (x,y+checker_increment+1) in MyStones:
                                checker_increment += 1
                            else:
                                break
                        for value in range(0,checker_increment):
                            PassedStones.append((x,y+value))


                    else:


                            score += Open5Val
                else:
                    if data.count("o") >= 2:
                        score += self.Parser(data)

        # print("vert Passedstones:",PassedStones)

        # Check Horizontal repetitions
        PassedStones = []
        for stone in sorted(MyStones,key=lambda x:x[0]):
            x,y = stone
            if (x,y) not in PassedStones:
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
                        data += "w"
                    elif (x-1+g, y) not in MyStones and (x-1+g, y) not in EnemyStones:
                        data += "-"

                if data == "xooooo" or data == "-ooooo" or data == "wooooo":
                    if (x+5,y) in MyStones:

                        checker_increment = 0
                        while True:
                            if (x+checker_increment+1,y) in MyStones:
                                checker_increment += 1
                            else:
                                break
                        for value in range(0, checker_increment):
                            PassedStones.append((x+value,y))

                    else:
                        score += Open5Val
                else:
                    if data.count("o") >= 2:
                        score += self.Parser(data)

        # print("Hori PassedStones:",PassedStones)
        PassedStones = []

        # check 2o`clock diagonal from 1,1 repetitions
        for stone in sorted(MyStones,key=lambda x:x[0]+x[1]): # stone coord: (x-y,y+1)
            x,y = stone
            if (x,y) not in PassedStones:
                data = ""
                for g in range(0,6):
                    if (x-1+g,y-1+g) in MyStones and (x-1+g,y-1+g) not in PassedStones:
                        data += "o"
                        PassedStones.append((x-1+g,y-1+g))
                    elif (x-1+g,y-1+g) in EnemyStones:
                        data += "x"
                        if g != 0:
                            break
                    elif x-1+g <= 0 or x-1+g > self.Board.size[0] or y-1+g <= 0 or y-1+g > self.Board.size[1]:
                        data += "w"
                    elif (x-1+g,y-1+g) not in MyStones and (x-1+g,y-1+g) not in EnemyStones:
                        data += "-"

                if data == "xooooo" or data == "-ooooo" or data == "wooooo":
                    if (x+5,y+5) in MyStones:
                        checker_increment = 0

                        while True:
                            if (x+checker_increment+1,y+checker_increment+1) in MyStones:
                                checker_increment += 1
                            else:
                                break
                        for value in range(0,checker_increment):
                            PassedStones.append((x+value,y+value))

                    else:

                        score += Open5Val
                else:
                    if data.count("o") >= 2:
                        score += self.Parser(data)
            # print(x - y, y + 1)
        PassedStones = []

        # check 5o`clock diagonal from 1,13 to 13,1 repetitions
        for stone in sorted(MyStones,key=lambda x:x[1]-x[0],reverse=True): # stone coord(x-self.Board.size[1]+y,y),but each time in g traverse, sub from y and add to x
            x,y = stone
            if (x,y) not in PassedStones:
                data = ""
                for g in range(0,6):
                    if (x-1+g,y+1-g) in MyStones and (x-1+g,y+1-g) not in PassedStones:
                        data += "o"
                        PassedStones.append((x-1+g,y+1-g))
                    elif (x-1+g,y+1-g) in EnemyStones:
                        data += "x"
                        if g != 0:
                            break
                    elif x-1+g <= 0 or x-1+g > self.Board.size[0] or y+1-g <= 0 or y+1-g > self.Board.size[1]:
                        data += "w"
                    elif (x-1+g,y+1-g) not in MyStones and (x-1+g,y+1-g) not in EnemyStones:
                        data += "-"

                if data == "xooooo" or data == "-ooooo" or data == "wooooo":
                    if (x+5,y-5) in MyStones:
                        checker_increment = 0

                        while True:
                            if (x+checker_increment+1,y-checker_increment-1) in MyStones:
                                checker_increment += 1
                            else:
                                break
                        for value in range(0,checker_increment):
                            PassedStones.append((x+checker_increment,y-checker_increment))

                    else:
                        score += Open5Val
                else:
                    if data.count("o") >= 2:
                        score += self.Parser(data)
            # print(x, y + (self.Board.size[1] - x))


        return score


    def Parser(self, pattern):
        if pattern in Open2:

            return self.Open2Val
        elif pattern in Open3:

            return self.Open3Val
        elif pattern in Open4:

            return self.Open4Val
        elif pattern in Open5:

            return Open5Val
        elif pattern in Closed4:
            return self.Closed4Val
        else:
            return 0
if __name__ == "__main__":
    from main import GameBoard
    import time
    board = GameBoard(13, 13)

    blackstones = [(3, 4), (4, 3)]

    for x in blackstones:
        board.AddStone("black", x)

    # RandomPopulate(board)
    print("Black:", board.BlackStones)
    print("White:", board.WhiteStones)
    heuristics = Analyzer(board)
    # heuristics = Analyzer(board,debug=True)
    starttime = time.time()
    print(heuristics.Grader("black"))
    # refree = WinChecker(board)
    # print(refree.CheckBoth())
    endtime = time.time()
    print("Total calculation time:", endtime - starttime if not endtime - starttime == 0.0 else "0.0 (<0.0001 seconds)")
    print(starttime, endtime)
    from GomokuBoardUI import GomokuBoard
    from tkinter import Tk

    root = Tk()
    UIboard = GomokuBoard(board, root, None)
    UIboard.Draw()
    root.mainloop()