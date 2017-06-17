

"""def createui(board):
    root = tkinter.Tk()
    gameui = GomokuBoard(board, root)
    root.mainloop()"""
if __name__ == "__main__":
    from MonteCarloTest import MonteCarlo

    from main import GameBoard
    from Analyzer import WinChecker
    import time,tkinter,threading
    from AICore import AlphaBeta
    board = GameBoard(10,10)


    ai = MonteCarlo(board,searchrange=2,TimeLimit=20)
    #ai = AlphaBeta(board,plydepth=5)
    refree = WinChecker(board)
    #threading.Thread(target=createui,args=(board,)).start()
    while True:
        print("Current Board white:", board.WhiteStones, "black:", board.BlackStones)
        x, y = input("Enter Human position with comma in between ex x,y:").split(",")
        ai.AddHumanStone((int(x), int(y)))
        if refree.Check("black"):
            print("BLACK WIN!!!!!")
            print("Current Board white:", board.WhiteStones, "black:", board.BlackStones)
            break
        starttime = time.time()
        ai.ChooseMove()
        endtime = time.time()

        print("CALCULATION TIME", endtime - starttime, "SECONDS")

        if refree.Check("white"):
            print("WHITE AI WIN!!!!!")
            print("Current Board white:", board.WhiteStones, "black:", board.BlackStones)
            break




