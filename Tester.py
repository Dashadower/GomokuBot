import random
from main import GameBoard
def RandomPopulate(size_x,size_y,Board):

    for x in range(1, size_x+1):
        for y in range(1, size_y+1):
            if round(random.random()) == 0:
                Board.AddStone("black",(x,y))
            else:
                Board.AddStone("white",(x,y))
