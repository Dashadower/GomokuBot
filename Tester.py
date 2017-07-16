from AICore import AICore
from main import GameBoard

g = GameBoard(10,10)
ai = AICore(g)
g.AddStone("black",(2,4))
g.AddStone("black",(2,5))
g.AddStone("black",(2,6))
g.AddStone("black",(3,8))
print(ai.GetOpenMovesPlus(g,1))