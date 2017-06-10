
if __name__ == "__main__":
    from MonteCarlo import MonteCarlo

    from main import GameBoard
    from Analyzer import WinChecker
    import time
    board = GameBoard(10,10)


    ai = MonteCarlo(board)

    refree = WinChecker(board)
    while True:
        print("Current Board white:",board.WhiteStones,"black:",board.BlackStones)
        x,y = input("Enter Human position with comma in between ex x,y:").split(",")
        ai.AddHumanStone((int(x),int(y)))
        if refree.Check("black"):
            print("BLACK WIN!!!!!")
            break
        starttime = time.time()
        data = ai.ChooseMove()
        endtime = time.time()
        ai.AddAIStone(data[0])
        print("CALCULATION TIME",endtime-starttime,"SECONDS")
        print("AI WINRATE",data[1])
        if refree.Check("white"):
            print("WHITE AI WIN!!!!!")
            break


