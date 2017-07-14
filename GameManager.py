import Analyzer
import tkinter
import tkinter.messagebox
class GameManager():
    def __init__(self,mainui,AIObject,TSS,gboard,textfield,progressbar):
        self.MainUI = mainui
        self.TextField = textfield
        self.progressbar = progressbar

        self.GomokuBoard = gboard
        self.AI = AIObject
        self.AIStoneType = self.AI.AIStoneType
        self.PlayerStoneType = "black" if self.AIStoneType == "white" else "white"
        self.refree = Analyzer.WinChecker(self.GomokuBoard)
        self.TSS = TSS
    def start(self):
        tkinter.messagebox.showinfo("", "플레이어의 차례입니다")
        self.GomokuBoard.PlayerTurn = True
    def CheckWin(self):
        if self.refree.Check(self.AIStoneType):
            tkinter.messagebox.showinfo("","컴퓨터의 승리입니다")
            self.GomokuBoard.PlayerTurn = False
            self.Writetotext("AI WIN")
        elif self.refree.Check(self.PlayerStoneType):
            tkinter.messagebox.showinfo("","인간의 승리입니다.")
            self.GomokuBoard.PlayerTurn = False
            self.Writetotext("USER WIN")
    def RegisterUserStone(self,coords):
        self.AI.AddHumanStone(coords)
        self.Writetotext("Human stone"+str(coords))
        self.GomokuBoard.PlayerTurn = False
        self.progressbar.start()
        self.Writetotext("인공지능의 차레입니다.")
        self.ChooseAImove()

    def ChooseAImove(self):
        if not self.TSS.Check():
            self.AI.ChooseMove()
            self.MainUI.after(2000,self.waitforinput)
        else:
            self.progressbar.stop()
            self.Writetotext("ThreatSpaceSearch"+str(self.TSS.Check()))
            self.AI.AddAIStone(self.TSS.Check())
            tkinter.messagebox.showinfo("", "플레이어의 차례입니다")
            self.GomokuBoard.PlayerTurn = True
    def waitforinput(self):
        data = self.AI.GetResult()

        if not data:
            self.MainUI.after(500,self.waitforinput)
            self.Writetotext(str(data)+str(self.AI.ControlQueue))
        else:
            self.Writetotext("AI Move Recieved")
            self.progressbar.stop()
            self.Writetotext(str(data))
            self.AI.AddAIStone(data[1])
            tkinter.messagebox.showinfo("","플레이어의 차례입니다")
            self.GomokuBoard.PlayerTurn = True
    def Writetotext(self,text):
        self.TextField.config(state="normal")
        self.TextField.insert("end",text+"\n")
        self.TextField.see("end")
        self.TextField.config(state="disabled")