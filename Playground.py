

"""def createui(board):
    root = tkinter.Tk()
    gameui = GomokuBoard(board, root)
    root.mainloop()"""
if __name__ == "__main__":

    from AICore import ThreatSpaceSearch
    from main import GameBoard
    from Analyzer import WinChecker
    import time,tkinter,threading
    from AlphaBetaParallel import AlphaBeta
    #from AlphaBetaMultiProcess import AlphaBeta
    from NegaMax import NegaMax
    #from HashTest import AlphaBeta
    board = GameBoard(10,10)


    #ai = NegaMax(board,"white",3,1)
    ai = AlphaBeta(board,"black",2,1)
    ai.InitiateProcess()
    ai.ChooseMove()
    data = ai.GetResult()
    print(data)
    ai.AddAIStone(data[1])
    threatspace = ThreatSpaceSearch(board,"white")
    refree = WinChecker(board)

    while True:
        print("Current Board white:", board.WhiteStones, "black:", board.BlackStones)
        x, y = input("Enter Human position with comma in between ex x,y:").split(",")
        ai.AddHumanStone((int(x), int(y)))
        if refree.Check("black"):
            print("BLACK WIN!!!!!")
            print("Current Board white:", board.WhiteStones, "black:", board.BlackStones)
            break
        starttime = time.time()
        if not threatspace.Check():
            ai.ChooseMove()
            while True:
                data = ai.GetResult()
                if not data:
                    pass
                else:
                    ai.AddAIStone(data[1])
                    break
        else:
            data = ai.AddAIStone(threatspace.Check())

            print("TSS!!!!")
        endtime = time.time()

        print("CALCULATION TIME", endtime - starttime, "SECONDS")

        if refree.Check("white"):
            print("WHITE AI WIN!!!!!")
            print("Current Board white:", board.WhiteStones, "black:", board.BlackStones)
            break




