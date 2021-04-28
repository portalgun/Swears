import swears as sw
import ast
import curses
from itertools import chain
from pprint import pprint

class layout:
    """
    actNum - active window num
    curNum - current window population number

    self.WINS   - collection of all windows that can be indexed
    'num' specifies a linear index, 'index' specifies a nested index
    self.index  - 4:[1,2,3]                             (num -> index)
    self.indexM - 4:[1,2,3]                             (num -> index) only contains main
    self.indexR - [1,2,3]:4                             (index -> num)
    self.indexS - 4:[10 2]                              (num -> size)
    self.indexF - 4:[[3, 2], [[.5 .5],[.3]],[0,0,0,0]]  (num -> format)
    self.indexP - num -> padNum
    TODO
       limit resize - size, once zero, don't draw

    RECURSE WINS
    form = (dims,elements,elements...)
        quad
            (main,(elements))
            #always [1,1],
            [[1,1],[.5, .5],[0,0,0,0]]=[[.5 .5],[]]
            [[1,1],[.5, .5],[quad,0,0,pane]]
        pane
            [[3, 2], [[.5 .5],[.3]],[0,0,0,0]]=([3 2],[[.5 .5],[.3],[]])
            ([3, 2], [[.5 .5],[.3]],(quad,pane,0,0))
        XXX convert pane to quad
    """
    def __init__(self,lIndex,stdscrn,*argv):
        self.settings=sw.settings()
        height=self.settings.statusPrcntHeight

        self.screen=sw.screen(stdscrn)
        if len(argv)==0:
            self.frmat=[[1,1],[.5, .5],[[[1,1],[.5,.5],[]],0,0,0] ]
            self.statusHeight=5
        elif len(argv)==1:
            self.frmat=argv[0]
            self.statusHeight=5
        elif len(argv)==2:
            self.frmat=argv[0]
            self.statusHeight=argv[1]
        elif len(argv)==3:
            self.frmat=argv[0]
            self.statusHeight=argv[1]

        self.lIndex=lIndex
        self.key=sw.inkey()
        self.WINS=[]
        self.PADS=[]
        self.OUT=[]
        self.index=dict()
        self.indexR=dict()
        self.indexM=dict()
        self.indexF=dict()
        self.indexS=dict()
        self.indexP=dict()
        self.curNum=0
        self.actNum=3
        self.status=sw.status(self.screen,self.statusHeight,self.actNum,lIndex)

        self.focused="win"
        self.mode="normal"
        self.view="default"

        self.reset_cmd()
        self.stri=""

        self.KEY=[]
        self.bNew=1
        self.border=1

        parentLoc=[self.status.height,0]
        parentSize=[self.screen.height-self.status.height, self.screen.width]
        if len(self.frmat)==2:
            self.frmat=[[1,1],self.frmat[0],self.frmat[1]]
        if self.frmat[2]==[]:
            self.frmat[2]=[0,0,0,0]

        self.create_quad([0],parentSize,parentLoc,self.frmat,0)
        self.create_wins_all(self.frmat,parentSize,parentLoc,[0])
        self.set_nodelay(1)
    def loop(self):
        while True:
            self.main()
    def main(self):
        self.draw()
        self.key.update(self)
        self.refresh(self.key.cmd)
        curses.doupdate()
    def main_nokey(self):
        self.bNew=1
        self.main()
    def create_wins_all(self,form,parentSize,parentLoc,ind,*argv):
        if len(argv)>0:
            bReplace=argv[0]
        else:
            bReplace=0

        if len(form)==2:
            form=[[1,1],form[0],form[1]]
        if form[2]==[]:
            form[2]=[0,0,0,0]
        dims=form[0]
        prcnt=form[1]

        sizes=self.get_sizes(prcnt,parentSize)
        Locs=self.get_locs(sizes,parentLoc)

        for i in range(0,4):
            #create current
            newInd=ind[:]
            newInd.append(i)
            self.create_quad(newInd,sizes[i],Locs[i],form[2][i],bReplace)

            #create nested
            if form[2][i]==0:
                continue
            else:
                self.create_wins_all(form[2][i],sizes[i],Locs[i],newInd,bReplace)
    def create_quad(self,ind,currentSize,Loc,form,bReplace):
        height=currentSize[0]
        width=currentSize[1]
        y=Loc[0]
        x=Loc[1]
        if bReplace:
            num=self.get_num(ind)
        else:
            self.curNum+=1
            num=self.curNum
        WIN=sw.win(num,ind,height,width,y,x,self.actNum)
        if bReplace:
            self.WINS[num-1]=WIN
        else:
            self.WINS.append(WIN)
        IND=str(ind)
        NUM=str(num)
        self.indexR.update({IND:NUM})
        self.index.update({NUM:IND})
        if ind[-1]==0 and bReplace:
            self.indexM[NUM]=IND
            self.indexF[NUM]=form
            self.indexS[NUM]=currentSize
        elif ind[-1]==0:
            self.indexM.update({NUM:IND})
            self.indexF.update({NUM:form})
            self.indexS.update({NUM:currentSize})
    def create_pad_table(self,NUM):
        w=self.WINS[NUM]
        PAD=sw.pad(w)
        pNUM=len(PAD)
        self.PADS.append(PAD,NUM)
        self.IndexP.update({NUM:pNUM})
    def get_sizes(self,prcnt,parentSize):
        Y1=round(prcnt[0]*(parentSize[0]))-self.border
        X1=round(prcnt[1]*(parentSize[1]))-self.border
        Y2=(1-prcnt[0])*(parentSize[0])-self.border
        X2=(1-prcnt[1])*(parentSize[1])-self.border
        sizes=[[Y1,X1],[Y2,X1],[Y1,X2],[Y2,X2]]
        return sizes
    def get_locs(self,sizes,parentLoc):
        Y1=parentLoc[0]+self.border
        X1=parentLoc[1]+self.border
        Y2=Y1+sizes[0][0]-1+self.border
        X2=X1+sizes[1][1]-1+self.border
        Locs=[[Y1,X1],[Y2,X1],[Y1,X2],[Y2,X2]]
        return Locs
    def get_num(self,*argv):
        num=self.get_index_helper_rev("",argv)
        return num
    def get_index(self,*argv):
        ind=self.get_index_helper("",argv)
        return ind
    def get_indexM(self,*argv):
        ind=self.get_index_helper("M",argv)
        return ind
    def get_indexF(self,*argv):
        form=self.get_index_helper("F",argv)
        return form
    def get_indexS(self,*argv):
        size=self.get_index_helper("S",argv)
        return size
    def get_indexP(self,*argv):
        pNum=self.get_index_helper("P",argv)
        return pNum
    def get_index_helper(self,TYPE,*argv):
        num=self.argnum(argv)
        if not isinstance(num,str):
            num=str(num)
        if TYPE=="":
            ind=self.index.get(num)
        elif TYPE=="M":
            ind=self.indexM.get(num)
        elif TYPE=="S":
            ind=self.indexS.get(num)
            return ind
        elif TYPE=="F":
            ind=self.indexF.get(num)
            return ind
        # convert from string to list
        try:
            ind=ast.literal_eval(ind)
        except:
            raise NameError(num)
        return ind
    def get_index_helper_rev(self,TYPE,*argv):
        argv=self.flatten(argv)
        if len(argv) > 0:
            ind=argv[0]
        else:
            num=int(self.actNum)
            return num

        if not isinstance(ind,str):
            ind=str(ind)

        if TYPE=="":
            num=self.indexR.get(ind)
        if num!=None:
            num=int(num)
        return num
    def get_child_num(self,*argv):
        num=self.argnum(argv)
        p=self.get_index(num)
        nums=range(0,3)
        j=[]
        for i in range(len(nums)):
            k=p[:]
            k.append(i)
            if str(k) in self.indexR:
                j.append(k)
        if j==[]:
            j=None
        return j
    def get_neighbors_num(self,*argv):
        num=self.argnum(argv)
        nums=range(0,4)
        c=self.get_index(num)
        p=c[:-1]
        n=[]
        for i in nums:
            k=p[:]
            k.append(i)
            if str(k) in self.indexR:
                k=self.get_num(k)
                n.append(k)
        if n==[]:
            n=None
        return n
    def is_active_empty(self):
        if self.get_child_num(self.actNum) == None:
            return True
        else:
            return False
    def flatten(self,T):
        if not isinstance(T,tuple): return (T,)
        elif len(T) == 0: return ()
        else: return self.flatten(T[0]) + self.flatten(T[1:])
    def argnum(self,*argv):
        argv=self.flatten(argv)
        if len(argv)>0:
            num=argv[0]
        else:
            num=self.actNum
        return num
    def get_parent_size(self,*argv):
        num=self.argnum(argv)
        num=self.get_parent_num(num)
        return self.get_indexS(num)
    def get_parent_num(self,*argv):
        num=self.argnum(argv)
        k=self.get_index(num)
        return self.get_num(k[:-1])
    def get_parent_ind(self,*argv):
        num=self.argnum(argv)
        num=self.get_parent_num(num)
        ind=self.get_index(num)
        return ind
    def get_main_ind(self,*argv):
        num=self.argnum(argv)
        ind=self.get_parent_ind(num)
        ind.append(0)
        return ind
    def get_main_num(self,*argv):
        num=self.argnum(argv)
        ind=self.get_main_ind(num)
        num=self.get_num(ind)
        return num
    def get_format(self,*argv):
        num=self.argnum(argv)
        num=self.get_parent_num(num)
        form=self.get_indexF(num)
        return form
    def set_nodelay(self,val):
        for i in range(len(self.WINS)):
            if self.WINS[i].win == None:
                continue
            self.WINS[i].no_delay(val)
        self.status.win.win.nodelay(val)
    def draw(self):
        self.wins_draw()
        self.pads_draw()
        self.status.draw()
    def wins_draw(self):
        self.KEY=[]
        flag=0
        for i in range(len(self.WINS)):
            if self.WINS[i].win==None:
                continue
            elif i>0 or self.bNew==1:
                self.WINS[i].draw()
                self.bNew=0
                flag=1
            else:
                k=self.WINS[i].get_char()
                if k != -1:
                    self.KEY.append(k)
        if flag==1:
            self.bNew=1

    def pads_draw(self):
        flag=0
        for i in range(len(self.PADS)):
            if self.PADS[i].pad==None:
                continue
            elif i>0 or self.bNew==1:
                self.PADS[i].draw()
                self.bNew=0
                flag=1
            else:
                k=self.PADS[i].get_char()
                if k != -1:
                    self.KEY.append(k)
        if flag==1:
            self.bNew=1
    def refresh(self,*argv):
        #KEYS
        if len(argv) > 0:
            self.cmd_assign(argv[0])
            self.cmd_all()

        #REFRESH
        self.screen.refresh()
        self.wins_refresh()
        #self.pads_refresh()
        self.reset_cmd()
        self.bNew=0
    def wins_refresh(self):
        for i in range(len(self.WINS)):
            self.WINS[i].refresh()
        self.status.win.win.refresh()
    def pads_refresh(self):
        for i in range(len(self.PADS)):
            WIN=self.WINS[self.PADS[numP].winNum]
            self.PADS[numP].refresh(WIN)
    def reset_cmd(self):
        self.win_cmd="null"
        self.cursor_cmd="null"
        self.table_cmd="null"
        self.menu_cmd="null"
        self.mod_cmd="null"
        self.view_cmd="null"
    def cmd_all(self):
        self.change_view_cmd()
        self.change_win_cmd()
        #self.change_pad_cmd()
        #self.change_menu_cmd()
        self.change_mod_cmd()
    def cmd_assign(self,KEY):
        if not KEY:
            return

        loc=KEY[1]
        KEY=KEY[0]
        if loc=="mode":
            self.mode=KEY
        elif loc=="view" and self.focused=="win":
            self.view_cmd=KEY
        elif loc=="focused" and self.focused=="win":
            self.win_cmd=KEY
        elif loc=="focused" and self.focused=="pad":
            self.pad_cmd=KEY
        elif loc=="focused" and self.focused=="menu":
            self.menu_cmd=KEY
        elif loc=="focused" and self.focused=="mod":
            self.mod_cmd=KEY
    def change_view_cmd(self):
        if self.view_cmd=="null":
            return
        elif self.view_cmd=="switch":
            self.OUT=1
    def change_win_cmd(self):
        if self.win_cmd=="null":
            return
        self.change_win_inc()
        self.change_win_cardinal()
        self.change_win_zoom()
        for i in range(len(self.WINS)):
            height=self.WINS[i].height
            width=self.WINS[i].width
            y=self.WINS[i].y
            x=self.WINS[i].x
            self.WINS[i].setup(self.actNum,1,height,width,y,x)

    def change_pad_cmd(self):
        #pad command is 2 element
        if self.pad_cmd=="null":
            return
        cmd=self.pad_cmd[0]

        num=self.get_index(self.actNum)
        num=num[-1]
        numP=self.get_indexP(num)
        if not numP:
            return
        PAD=self.PADS[numP]
        if cmd=='win':
            cmd=self.pad_cmd[1:]
            PAD=self.change_pad_win(PAD,cmd)     #move contents to diff window
        elif cmd=='inc':
            cmd=self.pad_cmd[1:]
            PAD=self.change_pad_inc(PAD,cmd)     #move position within pad
        elif cmd=='order':
            cmd=self.pad_cmd[1:]
            PAD=self.change_pad_sort(PAD,cmd)   #col and rows
        elif cmd=='content':
            cmd=self.pad_cmd[1:]
            PAD=self.change_pad_content(PAD,cmd) #different content
        else:
            return
        self.PAD[ind]=PAD
    def change_pad_win(self,PAD,cmd):
        num=cmd[0]
        win=self.WINS[ind]
        PAD.assign_win(win,num)
        return PAD
    def change_pad_inc(self,PAD,cmd):
        dir=cmd[0]
        num=cmd[1]
        PAD.inc(dir,num)
        return PAD
    def change_pad_sort(self,PAD,cmd):
        dir=cmd[0]
        PAD.sort(dir)
        return PAD
    def change_pad_content(self,PAD,cmd):
        OBJECT=cmd[0]
        win=PAD.win
        winNum=PAD.winNum
        PAD=sw(win,winNum,OBJECT)
        return PAD
    def change_mod_cmd(self):
        # XXX
        pass
    def change_win_inc(self):
        if self.actNum==1:
            return
        elif self.win_cmd=="incLeft":
            dim="x"
            direct="down"
        elif self.win_cmd=="incRight":
            dim="x"
            direct="up"
        elif self.win_cmd=="incUp":
            dim="y"
            direct="down"
        elif self.win_cmd=="incDown":
            dim="y"
            direct="up"
        else:
            return
        self.inc_size(direct,dim)
    def change_win_cardinal(self):
        if self.win_cmd!="left" and self.win_cmd!="right" and self.win_cmd!="up" and self.win_cmd!="down":
            return
        direct=self.win_cmd
        bGd=self.check_direct_cardinal(direct)
        if not bGd:
            return
        self.change_focus_neighbor(direct)
    def change_win_zoom(self):
        if self.win_cmd!="Forward" and self.win_cmd!="Back":
            return
        direct=self.win_cmd
        bGd=self.check_direct_zoom(direct)
        if not bGd:
            return
        self.change_focus_zoom(direct)
    def check_direct_cardinal(self,direct):
        N=self.get_neighbors_num()
        if N==None:
            bGd=False
            return bGd
        c=N.index(self.actNum)
        ind=self.quad_ind_direct(c,direct)
        if ind==c:
            bGd=False
        else:
            bGd=True
        return bGd
    def check_direct_zoom(self,direct):
        bGd=True
        if direct=='Back':
            p=self.get_parent_num()
            if p==None:
                bGd=False
        elif direct=='Forward':
            c=self.get_child_num()
            if c==None:
                bGd=False
        return bGd
    def change_focus_zoom(self,direct):
        if direct=="Back":
            self.actNum=self.get_parent_num()
        elif direct=="Forward":
            N=self.get_child_num()
            N=str(N[0])
            self.actNum=self.get_num(N)
            # XXX need routine to save and apply previous zoom path
    def change_focus_neighbor(self,direct):
        N=self.get_neighbors_num()
        c=N.index(self.actNum)
        ind=self.quad_ind_direct(c,direct)
        c=N.index(self.actNum)
        try:
            self.actNum=N[ind]
        except:
            pass
    def change_focus_parent_jump(self,direct):
        actNum=self.actNum

        #ind for child location in parent neighbor
        n=self.get_neighbors_num()
        c=N.index(self.actNum)
        revdirect=self.rev_direct(direct)
        ind=self.quad_ind_direct(c,revdirect)

        #ind for
        self.actNum=self.get_parent_num()
        #ind for
        Felf.actNum=self.get_parent_num()
        N=self.get_neighbors_num()
    def rev_direct(direct):
        if direct=="left":
            direct="right"
        elif direct=="right":
            direct="left"
        elif direct=="up":
            direct="down"
        elif direct=="down":
            direct="up"
    def quad_ind_direct(self,c,direct):
        res=False
        if c==0:
            if   direct=="left":
                res=c
            elif direct=="right":
                res=2
            elif direct=="up":
                res=c
            elif direct=="down":
                res=1
        elif c==1:
            if   direct=="left":
                res=c
            elif direct=="right":
                res=3
            elif direct=="up":
                res=0
            elif direct=="down":
                res=c
        elif c==2:
            if   direct=="left":
                res=0
            elif direct=="right":
                res=c
            elif direct=="up":
                res=c
            elif direct=="down":
                res=3
        elif c==3:
            if   direct=="left":
                res=1
            elif direct=="right":
                res=c
            elif direct=="up":
                res=2
            elif direct=="down":
                res=c
        return res
    def check_size(self,prcnt,inc,dim,*argv):
        num=self.argnum(argv)
        pSize=self.get_parent_size(num)
        if dim=="y":
            pSize=pSize[0]
        elif dim=="x":
            pSize=pSize[1]
        newSize=(prcnt+inc)*pSize
        maxSize=pSize-self.border
        minSize=self.border
        if newSize > maxSize:
            newSize=maxSize
        elif newSize < minSize:
            newSize=minSize
        newPrcnt=newSize/pSize
        return newPrcnt
    def inc_size(self,direct,dim,*argv):
        num=self.argnum(argv)
        if direct=="up":
            inc=.05
        elif direct=="down":
            inc=-.05
        form=self.get_format(num)
        if dim=="y":
            form[1][0]=self.check_size(form[1][0],inc,"y")
        elif dim=="x":
            form[1][1]=self.check_size(form[1][1],inc,"x")
            #try:
            #    form[1][1]=self.check_size(form[1][1]+inc)
            #except:
            #    raise NameError(form)
        elif dim=="b":
            form[1][0]=self.check_size(form[1][0],inc,"y")
            form[1][1]=self.check_size(form[1][1],inc,"x")
        self.reshape(form,self.actNum)
    def reshape(self,form,num):
        ind=self.get_parent_ind(num)
        num=self.get_parent_num(num)
        p=self.WINS[num-1]
        parentSize=[p.height, p.width]
        parentLoc=[p.y, p.x]
        self.create_quad(ind,parentSize,parentLoc,form,1)
        self.create_wins_all(form,parentSize,parentLoc,ind,1)
    def append_pad(self,num,*argv):
        win=self.WINS[num]
        self.PADS.append(pad(win,num),argv)
        padNum=len(self.PADS)
        return padNum
    def append_pad_active(self,*argv):
        padNum=self.append_pad(self.actNum,argv)
        return padNum
    def menu_to_active(self):
        menu=sw.menu()
        padNum=self.append_pad_active(menu)
    def display_format(self):
        # XXX
        pass
    def move_contents_v(self,num):
        # XXX
        pass
    def move_contents_h(self,num):
        # XXX
        pass
