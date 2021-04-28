from . import common
import swears as sw

class status(common):
    """
    STATUS BAR

    PROPTERTIES
    height
    width
    maxHeight
    prcntHeight

    TODO
      NEED INFO
    """
    def __init__(self,screen,height,actNum,lIndex):
        self.lIndex=lIndex
        self.get_dims(height,screen.width,0,0)
        self.get_win(actNum)
    def get_dims(self,height,width,y,x):
        self.height=height
        self.width=width
        self.y=y
        self.x=x
    def draw(self,*argv):
        if len(argv)>0:
            bGet=argv[0]
        else:
            bGet=0

        self.win.win.addch(1,self.width-2,str(self.lIndex+1))
        self.win.win.redrawwin()
        if bGet==1:
            OUT=self.WINS[i].win.getch()
            return OUT
    def get_win(self,actNum):
        self.win=sw.win(-1,-1,self.height,self.width,0,0,actNum)
    def refresh(self,prcntHeight,screen,*args):
        #STATUS
        self.parse_cmd(args)
        self.run_cmd()
        self.get_dims(prcntHeight,screen)
        self.all()
