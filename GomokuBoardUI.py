import tkinter


class GomokuBoard(tkinter.Frame):
    def __init__(self, GameBoard, master):
        self.master = master
        tkinter.Frame.__init__(self, self.master)
        self.pack(expand=tkinter.YES, fill=tkinter.BOTH)
        self.GameBoard = GameBoard


    def Draw(self):

        self.GameArea = tkinter.Canvas(self,bg="green")
        self.GameArea.pack(expand=tkinter.YES, fill=tkinter.BOTH)
        self.gridsize = 50
        self.stonesize = self.gridsize/2
        self.buffer = 20

        for x in range(1, self.GameBoard.size[0]+1):
            for y in range(1, self.GameBoard.size[1]+1):
                self.GameArea.create_rectangle((self.buffer+50*x,self.buffer+50*y,self.buffer+50*x+50,self.buffer+50*y+50))
        for stone in self.GameBoard.BlackStones:
            x = self.GameBoard.size[0]-stone[0]+1
            y = self.GameBoard.size[1]-stone[1]+1
            self.GameArea.create_oval((self.buffer+x*self.gridsize-self.stonesize, self.buffer+y*self.gridsize+self.stonesize, self.buffer+x*self.gridsize+self.stonesize,self.buffer+y*self.gridsize-self.stonesize),fill="black")

        for stone in self.GameBoard.WhiteStones:
            x = self.GameBoard.size[0]-stone[0]+1
            y = self.GameBoard.size[1]-stone[1]+1
            self.GameArea.create_oval((self.buffer+x*self.gridsize-self.stonesize, self.buffer+y*self.gridsize+self.stonesize, self.buffer+x*self.gridsize+self.stonesize,self.buffer+y*self.gridsize-self.stonesize),fill="white")
