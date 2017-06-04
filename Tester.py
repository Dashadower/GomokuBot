import random
from main import GameBoard
def RandomPopulate(Board):

    for x in range(1, Board.size[0]+1):
        for y in range(1, Board.size[1]+1):
            if round(random.random()) == 0:
                Board.AddStone("black",(x,y))
            else:
                Board.AddStone("white",(x,y))

