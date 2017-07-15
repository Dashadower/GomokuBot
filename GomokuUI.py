import tkinter
from GomokuBoardUI import GomokuBoard
from main import GameBoard
from tkinter.ttk import Progressbar
import AICore,GameManager, multiprocessing, AlphaBeta, AlphaBetaIterative
class MainScreen(tkinter.Frame):
    def __init__(self,master,gameboard,gridsize,buffer):
        tkinter.Frame.__init__(self,master)
        self.master = master
        self.pack(expand=tkinter.YES,fill=tkinter.BOTH)
        self.MainPane = tkinter.PanedWindow(self,orient=tkinter.HORIZONTAL)
        self.MainPane.pack(expand=tkinter.YES,fill=tkinter.BOTH)
        self.GameBoardBackground = tkinter.Frame(self.MainPane)
        self.MainPane.add(self.GameBoardBackground)
        self.SideBackground = tkinter.Frame(self.MainPane)
        self.MainPane.add(self.SideBackground)
        self.GomokuBoard = GomokuBoard(gameboard,self.GameBoardBackground,None,gridsize,buffer)
        self.TextFrame = tkinter.Frame(self.SideBackground)
        self.TextFrame.pack(side=tkinter.TOP,expand=tkinter.YES,fill=tkinter.BOTH)
        self.scrollbar = tkinter.Scrollbar(self.TextFrame)
        self.scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        self.InfoBox = tkinter.Text(self.TextFrame)
        self.InfoBox.pack(side=tkinter.LEFT,expand=tkinter.YES,fill=tkinter.BOTH)
        self.InfoBox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.InfoBox.yview)
        self.InfoBox.insert(tkinter.END,"고모쿠봇 ^^\n")
        self.InfoBox.config(state=tkinter.DISABLED)
        self.progressbar = Progressbar(self.SideBackground,mode="indeterminate")
        self.progressbar.pack(side=tkinter.BOTTOM,fill=tkinter.X)



def clearscreen():
    for child in root.winfo_children():
        child.destroy()
def OnNewGame():
    clearscreen()
    gboard = GameBoard(BOARDSIZE_X, BOARDSIZE_Y)
    screen = MainScreen(root,gboard,GRIDSIZE,BUFFER)
    if MODE == "VANILLA":
        ai = AlphaBeta.AlphaBeta(gboard,"white",DIFFICULTY,SEARCHRANGE)
        screen.InfoBox.config(state=tkinter.NORMAL)
        screen.InfoBox.insert(tkinter.END, "인공지능 설정(AlphaBeta): 심층 깊이 사용하지 않음, Zobrist 해쉬 사용하지 않음, 트랜스포지션 테이블 사용하지 않음\n")
        screen.InfoBox.config(state=tkinter.DISABLED)
    elif MODE == "HASHED":
        ai = AlphaBetaIterative.AlphaBeta(gboard, "white", DIFFICULTY, SEARCHRANGE)
        screen.InfoBox.config(state=tkinter.NORMAL)
        screen.InfoBox.insert(tkinter.END, "인공지능 설정(AlphaBetaIterative): 심층 깊이 사용, Zobrist 해쉬 사용, 트랜스포지션 테이블 사용\n")
        screen.InfoBox.config(state=tkinter.DISABLED)
    mgr = GameManager.GameManager(root,ai,AICore.ThreatSpaceSearch(gboard,"white"),screen.GomokuBoard,screen.InfoBox,screen.progressbar)
    screen.GomokuBoard.GameManager = mgr
    mgr.start()
if __name__ == "__main__":
    multiprocessing.freeze_support()
    root = tkinter.Tk()
    exec(open("settings.config").read())
    MainScreen(root,GameBoard(BOARDSIZE_X,BOARDSIZE_Y),GRIDSIZE,BUFFER) # in settings.config
    mainmenu = tkinter.Menu(root)
    filemenu = tkinter.Menu(mainmenu,tearoff=0)
    filemenu.add_command(label="게임하기",command=OnNewGame)
    mainmenu.add_cascade(label="파일",menu=filemenu)
    root.config(menu=mainmenu)
    root.mainloop()