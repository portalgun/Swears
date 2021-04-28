from . import common
import swears as sw

class win(common):
    """
    Window within a workspace
    Can be nested
    PROPERTIES
      location
      height
      width
      y
      x
      child
    INHERITED METHODS
      setup
        set_border
        set_dims
        cmd_reset

      activate
      deactivate

      inc_y
      inc_x
      inc_width
      inc_height

      parse_cmd
      run_cmd_common
    """
    def __init__(self,num,ind,height,width,y,x,*argv):
        self.color=sw.settings().InactColor1
        self.bActive=0
        self.height=-1
        self.width=-1
        self.y=-1
        self.x=-1
        if len(argv)>0:
            actNum=argv[0]
        else:
            actNum=-1
        self.bBorder=1
        self.num=num
        self.ind=ind
        self.setup(actNum,1,height,width,y,x)
        self.key=[]
    def refresh(self):
        if self.win==None:
            return
        self.win.refresh()
    def draw(self):
        self.win.redrawwin()
    def get_char(self):
        self.no_delay(0)
        OUT=self.win.getch()
        self.no_delay(1)
        return OUT
    def no_delay(self,val):
        self.win.nodelay(val)
    def create_pad(self,query):
        queryO=query_db(query)
        table=parse_query(queryO)
        self.pad=pad(table)
        # XXX
        self.pad.get_pos(y,x,win_Y,win_X,height,width)
    def create_cursor(self):
        self.createCursor(win)
    #----------------------------
    def field_from_cursor(self):
        #NAIVE Y
        if self.curosr.bBlock:
            bH=self.cursor.blockHeight
            cH=self.cursor.yN
            if bH>cH:
                yN=range(cH,bH)
            elif bH<cH:
                yN=range(bH,cH)
            else:
                yN=cH
        else:
            yN=self.cursor.yN

        #NAIVE X
        if cursor.mode=="col":
            col=self.cursor.xN
        elif cursor.mode=="full":
            col=range(0,self.pad.colLengths-1)
