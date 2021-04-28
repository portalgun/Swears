import swears as sw
import random
from . import common

class pad(common):
    #CREATED BY WIN
    # bActive
    # y
    # x
    # height
    # width
    # winNum
    # first_row
    # full_height
    # full_width
    # CURSOR
    # OBJECT - object that will be displayed
    # object_type - 'list' or 'table'
    def __init__(self,win,winNum,*argv):
        self.reset(win,winNum,argv)
    def reset(*argv):
        assign_flag=0
        if len(argv)>0:
            win=argv[0]
            assignflag=1
        else:
            win=self.win
        if len(argv)>1:
            winNum=argv[1]
            assignflag=1
        else:
            winNum=self.winNum
        if len(argv)>3:
            bReset=argv[3]
        else:
            bReset=1

        if assignflag==1:
            self.assign_win(win,winNum)
        if bReset==1:
            self.reset_pos()
        if len(argv)>2:
            OBJECT=argv[2]
            self.set(OBJECT)
    def assign_win(self,win,winNum):
        self.bActive=win.bActive
        self.x=win.x
        self.y=win.y
        self.height=win.height
        self.width=win.width
        self.win_num=winNum
    def reset_pos(self):
        self.first_row=0
        self.first_col=0
    def new_pad(self):
        self.pad=curses.newpad(self.full_height,self.full_width)
    def inc(self,dir,num):
        if dir=='h':
            self.cursor.inc_h(num)
        elif dir=='v':
            self.cursor.inc_v(num)
        elif dir=='hc':
            self.cursor.inc_h_constrained(num)
        elif dir=='vc':
            self.cursor.inc_v_constrained(num)
        self.first_col=self.cursor.first_col
        self.first_row=self.cursor.first_row
    def sort(self,dir):
        if self.object_type=='list':
            pos=self.cursor.yN_full
            row=self.OBJECT[pos]
            if dir=='ascend':
                self.OBJECT.sort
            elif dir=='descend':
                self.OBJECT.sort(reverse = True)
            elif dir=='shuffle':
                random.shuffle(self.OBJECT)
            newPos=self.OBJECT.index(row)
        elif  self.object_type=='table':
            pos=self.cursor.yN_full-1
            newPos=self.table.original_ind(pos) # XXX
            self.OBJECT.sort(dir); # XXX
        else:
            return

        self.reset(self.win,self.winNum,self.OBJECT)
        self.cursor.move_to_row(newPos)
        self.first_row=self.cursor.first_row
    def move_row(self,num):
        #XXX
        pass
    def move_col(self,num):
        #XXX
        pass
    def set(self,OBJECT):
        if isinstance(OBJECT,list):
            self.assign_list(OBJECT)
        else:
            self.assign_table(OBJECT)
        self.new_pad()
        self.populate_object()
    def assign_table(self,table):
        self.object_type='table'
        self.OBJECT=table
        self.full_width=max(table.complete, key=operator.itemgetter(1))
        self.full_height=len(table.complete)+1 #plus header
    def assign_list(self,List):
        self.object_type='list'
        self.OBJECT=List
        self.full_width=max(List, key=operator.itemgetter(1))
        self.full_height=len(LIST)
    def assign_menu(self,Menu):
        self.object_type='menu'
        self.OBJECT=Menu
        #self.full_width #XXX
        #self.full_height #XXX
    def populate_object(self):
        if self.object_type=='list':
            self.populate_List()
        elif self.object_type=='table':
            self.populate_table()
    def populate_table(self):
        self.pad.addstr(0,0,self.OBJECT.header)
        for y in range(0,len(OBJECT.complete)-1):
            self.pad.addstr(y+1,0,OBJECT.complete[y])
    def populate_list(self):
        for y in range(0,len(OBJECT)-1):
            self.pad.addstr(y+1,0,OBJECT[y])
    def refresh(self,win):
        self.assign_win(win,self.winNum)
        self.cursor.refresh(self)
    def draw(self):
        self.pad.refresh(self.first_row,self.first_col,self.y,self.x,self.y+height,self.x+width)
    def get_char(self):
        self.no_delay(0)
        OUT=self.pad.getch()
        self.no_delay(1)
        return OUT
    def no_delay(self,val):
        self.pad.nodelay(val)
