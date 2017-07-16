import Analyzer
import tkinter,time,os,signal,sys
import tkinter.messagebox
class GameManager():
    def __init__(self,mainui,AIObject,TSS,gboard,textfield,progressbar,pids):
        self.MainUI = mainui
        self.TextField = textfield
        self.progressbar = progressbar
        self.pids = pids
        self.GomokuBoard = gboard
        self.AI = AIObject
        self.AIStoneType = self.AI.AIStoneType
        self.PlayerStoneType = "black" if self.AIStoneType == "white" else "white"
        self.refree = Analyzer.WinChecker(self.AI.Board)
        self.TSS = TSS
    def start(self):
        self.Writetotext("검색 깊이: "+str(self.AI.PlyDepth)+"(1)수(PLY) 검색 범위: "+str(self.AI.OpenSearchRange)+"칸(TILE)")
        tkinter.messagebox.showinfo("", "플레이어의 차례입니다")
        self.GomokuBoard.PlayerTurn = True
        self.StartTime = time.time()
    def End(self):
        if self.pids:
            for pid in self.pids:
                os.kill(pid,signal.SIGTERM)
            sys.exit()
        else:
            sys.exit()
    def CheckWin(self):
        if self.refree.Check(self.AIStoneType):
            tkinter.messagebox.showinfo("","컴퓨터의 승리입니다")
            self.GomokuBoard.PlayerTurn = False
            self.Writetotext("AI WIN")
            self.Writetotext("총 게임시간(입출력 시간 포함):" + str(time.time() - self.StartTime))
            return True
        elif self.refree.Check(self.PlayerStoneType):
            tkinter.messagebox.showinfo("","인간의 승리입니다.")
            self.GomokuBoard.PlayerTurn = False
            self.Writetotext("USER WIN")
            self.Writetotext("총 게임시간(입출력 시간 포함):" + str(time.time() - self.StartTime))
            return True
        else:
            return False
    def RegisterUserStone(self,coords):
        self.AI.AddHumanStone(coords)
        self.Writetotext("Human stone"+str(coords))
        self.GomokuBoard.PlayerTurn = False
        if not self.CheckWin():
            self.progressbar.start()
            self.Writetotext("인공지능의 차례입니다.")
            self.ChooseAImove()

    def ChooseAImove(self):
        self.CalcTime = time.time()
        if not self.TSS.Check():
            self.AI.ChooseMove()
            self.MainUI.after(200,self.waitforinput)
        else:
            self.progressbar.stop()
            self.Writetotext("ThreatSpaceSearch"+str(self.TSS.Check()))
            self.AI.AddAIStone(self.TSS.Check())
            self.Writetotext("계산시간(입출력 시간 포함):"+str(time.time()-self.CalcTime))
            self.GomokuBoard.clear()
            self.GomokuBoard.Draw()
            self.MainUI.update()
            if not self.CheckWin():
                tkinter.messagebox.showinfo("", "플레이어의 차례입니다")
                self.GomokuBoard.PlayerTurn = True
    def waitforinput(self):
        data = self.AI.GetResult()

        if data == False:
            self.MainUI.after(200,self.waitforinput)
            #self.Writetotext(str(data)+str(self.AI.ControlQueue.empty()))
        else:
            self.Writetotext("AI Move Recieved")
            self.progressbar.stop()
            self.Writetotext("평가함수 결과(Grader()):"+str(data[0])+" 위치:"+str(data[1]))
            self.AI.AddAIStone(data[1])
            if data[0] >= 900000000:
                self.Writetotext("인공지능의 필승입니다 ^^")
            self.Writetotext("계산시간(입출력 시간 포함):" + str(time.time() - self.CalcTime))
            self.GomokuBoard.clear()
            self.GomokuBoard.Draw()
            self.MainUI.update()
            if not self.CheckWin():
                tkinter.messagebox.showinfo("","플레이어의 차례입니다")
                self.GomokuBoard.PlayerTurn = True
    def Writetotext(self,text):
        self.TextField.config(state="normal")
        self.TextField.insert("end",str(text)+"\n")
        self.TextField.see("end")
        self.TextField.config(state="disabled")