from MonteCarlo import MonteCarlo
from main import GameBoard
from Analyzer import WinChecker
board = GameBoard(10,10)
ai = MonteCarlo(board,searchrange=3,TimeLimit=None,GameLimit=100)
refree = WinChecker(board)
while True:
    print("Current Board white:",board.WhiteStones,"black:",board.BlackStones)
    x,y = input("Enter Human position with comma in between ex x,y:").split(",")
    ai.AddHumanStone((int(x),int(y)))
    if refree.Check("black"):
        print("BLACK WIN!!!!!")
        break
    data = ai.ChooseMove()
    ai.AddAIStone(data[0])
    print("AI WINRATE",data[1])
    if refree.Check("white"):
        print("WHITE AI WIN!!!!!")
        break


