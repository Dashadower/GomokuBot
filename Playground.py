from main import GameBoard
from AICore import AlphaBeta,MiniMax
"""board = GameBoard(5,5)
ai = MiniMax(board,plydepth=3)
while True:
    print("Current Board white:",board.WhiteStones,"black:",board.BlackStones)
    x,y = input("Enter Human position with comma in between ex x,y:").split(",")
    ai.AddHumanStone((x,y))
    if ai.CheckWin("black"):
        print("BLACK WIN!!!!!")
        break
    ai.ChooseMove()
    if ai.CheckWin("white"):
        print("WHITE AI WIN!!!!!")
        break"""
from AICore import AICore
b = GameBoard(3,3)
b.AddStone("black",(3,3))
print(b.BlackStones)
d = AICore(b)
print(d.GetOpenMoves(b))