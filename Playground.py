

"""def createui(board):
    root = tkinter.Tk()
    gameui = GomokuBoard(board, root)
    root.mainloop()"""
if __name__ == "__main__":
    from MonteCarloTest import MonteCarlo
    from AICore import ThreatSpaceSearch
    from main import GameBoard
    from Analyzer import WinChecker
    import time,tkinter,threading
    from AlphaBeta import AlphaBeta
    board = GameBoard(10,10)


    #ai = MonteCarlo(board,searchrange=2,TimeLimit=20)
    ai = AlphaBeta(board,"white",2,1)
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
        else:
            ai.AddAIStone(threatspace.Check())
            print("TSS!!!!")
        endtime = time.time()

        print("CALCULATION TIME", endtime - starttime, "SECONDS")

        if refree.Check("white"):
            print("WHITE AI WIN!!!!!")
            print("Current Board white:", board.WhiteStones, "black:", board.BlackStones)
            break




