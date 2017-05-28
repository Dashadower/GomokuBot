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
        self.buffer = 100

        for x in range(0, self.GameBoard.size[0]-1):
            for y in range(0, self.GameBoard.size[1]-1):

                self.GameArea.create_rectangle((self.buffer+self.gridsize*x,self.buffer+self.gridsize*y,self.buffer+self.gridsize*x+self.gridsize,self.buffer+self.gridsize*y+self.gridsize))

        for x in range(1,self.GameBoard.size[0]+1):
            self.GameArea.create_text((self.buffer + self.gridsize * (x-1),self.buffer+self.gridsize*(self.GameBoard.size[0]-1)+self.buffer/2), text=x)
        for y in range(1,self.GameBoard.size[1]+1):
            self.GameArea.create_text((self.buffer/2,self.buffer+self.gridsize*(self.GameBoard.size[1]-y)), text=y)
        for stone in self.GameBoard.BlackStones:
            x = stone[0]-1
            y = self.GameBoard.size[1]-stone[1]
            self.GameArea.create_oval((self.buffer+x*self.gridsize-self.stonesize, self.buffer+y*self.gridsize+self.stonesize, self.buffer+x*self.gridsize+self.stonesize,self.buffer+y*self.gridsize-self.stonesize),fill="black")

        for stone in self.GameBoard.WhiteStones:
            x = stone[0]-1
            y = self.GameBoard.size[1]-stone[1]
            self.GameArea.create_oval((self.buffer+x*self.gridsize-self.stonesize, self.buffer+y*self.gridsize+self.stonesize, self.buffer+x*self.gridsize+self.stonesize,self.buffer+y*self.gridsize-self.stonesize),fill="white",outline="white")

if __name__ == "__main__":
    from main import GameBoard
    board = GameBoard(10,10)
    root = tkinter.Tk()
    boardui = GomokuBoard(board,root)
    boardui.Draw()
    root.mainloop()