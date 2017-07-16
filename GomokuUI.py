import tkinter
from GomokuBoardUI import GomokuBoard
from main import GameBoard
from tkinter.ttk import Progressbar
import AICore,GameManager, multiprocessing, AlphaBetaMultiProcess,AlphaBeta
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
    if MODE == "SINGLE":
        print("SINGLE")
        ai = AlphaBeta.AlphaBeta(gboard,"white",DIFFICULTY,SEARCHRANGE)
        screen.InfoBox.config(state=tkinter.NORMAL)
        screen.InfoBox.insert(tkinter.END, "인공지능 설정(AlphaBeta): 프로세스 1개 사영\n")
        screen.InfoBox.config(state=tkinter.DISABLED)
    elif MODE == "MULTIPROCESS":
        print("MULTIPROCESS")
        screen.InfoBox.config(state=tkinter.NORMAL)
        screen.InfoBox.insert(tkinter.END, "인공지능 설정(AlphaBetaMultiProcess): 다중 프로세스 사용(프로세스 %d개), 전환 범위: %d수\n"%(MAXPROCESSES,MULTIPROCESS_CUTOFF))
        screen.InfoBox.config(state=tkinter.DISABLED)
        ai = AlphaBetaMultiProcess.AlphaBeta(gboard, "white", DIFFICULTY, SEARCHRANGE,MAXPROCESSES,MULTIPROCESS_CUTOFF)
        processes = ai.InitiateProcess()
        screen.InfoBox.config(state=tkinter.NORMAL)
        screen.InfoBox.insert(tkinter.END, "%s\n"%(processes))
        screen.InfoBox.config(state=tkinter.DISABLED)
        
    mgr = GameManager.GameManager(root,ai,AICore.ThreatSpaceSearch(gboard,"white"),screen.GomokuBoard,screen.InfoBox,screen.progressbar)
    ai.ReportHook = mgr.Writetotext
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