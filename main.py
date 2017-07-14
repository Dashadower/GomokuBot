

class GameBoard():
    def __init__(self, size_x, size_y):
        self.size = (size_x, size_y)
        self.stones = []
        self.BlackStones = []
        self.WhiteStones = []
        self.turn = "black"
        self.Moves = 0

    def AddStone(self, StoneType, Position): # Position: (x,y) tuple
        if StoneType == "black":
            self.BlackStones.append(Position)
            self.stones.append(Position)
            self.turn = "white"
        elif StoneType == "white":
            self.WhiteStones.append(Position)
            self.stones.append(Position)
            self.turn = "black"
        self.Moves += 1


if __name__ == "__main__":
    pass