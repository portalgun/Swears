import swears as sw
import curses
from pprint import pprint

class common:
    def setup(self,actNum,*argv):
        if len(argv)>1:
            height=argv[1]
            width =argv[2]
            y     =argv[3]
            x     =argv[4]
        else:
            self.height=height
            self.width =width
            self.y     =y
            self.x     =x
        bSet=self.get_dims(height,width,y,x)
        self.set_dims(bSet)
        if self.win==None:
            return
        self.act_toggle(actNum)
        self.set_border()
    def set_border(self):
        if self.bBorder==1:
            self.win.attron(curses.color_pair(self.color))
            self.win.box()
            self.win.attroff(curses.color_pair(self.color))
    def get_dims(self,height,width,y,x):
        if self.height != height or self.width != width or self.y != y or self.x !=x:
            bSet=1
        else:
            bSet=1
        self.height=round(height)
        self.width=round(width)
        self.y=round(y)
        self.x=round(x)
        return bSet
    def set_dims(self,*argv):
        if len(argv)>0:
            bSet=argv[0]
        else:
            bSet=1
        if bSet==1:
            self.create_win();
    def create_win(self):
        if self.height < 0.5 or self.width < 0.5:
            self.win=None
        else:
            self.win=curses.newwin(self.height,self.width,self.y,self.x)
    def draw(self):
        self.key=self.win.refresh()
    def act_toggle(self,actNum):
        if self.num==actNum:
            self.activate()
        else:
            self.deactivate()
    def activate(self):
        self.color=sw.settings().ActColor1
        self.bActive=1
    def deactivate(self):
        self.color=sw.settings().InactColor1
        self.bActive=0
    def inc_y(self):
        self.yN=inc_fun(self,self.yN,self.maxYn,self.minYn)
    def inc_x(self):
        self.xN=inc_fun(self,self.xN,self.maxXn,self.minXn)
    def inc_width(self):
        self.width=inc_fun(self,self.width,self.maxWidth,self.minWidth)
    def inc_height(self):
        self.height=inc_fun(self,self.height,self.maxHeight,self.minHeight)
    def parse_cmd(self,*args):
        self.cmd=''
        if len(args)>0 and self.bActive==1 and args[0][1]==self.getClass():
            self.cmd=args[0]
    def run_cmd_common(self):
        if self.cmd=='':
            return
        elif self.cmd=='Left':
            self.sign=-1
            self.inc_x()
        elif self.cmd=='Right':
            self.sign=1
            self.inc_x()
        elif self.cmd=='Up':
            self.sign=-1
            self.inc_y()
        elif self.cmd=='Down':
            self.sign=1
            self.inc_y()
    def cmd_reset(self):
        self.inc=''
        self.val=''
        self.sign=''
