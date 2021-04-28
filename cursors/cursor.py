class cursor():
    """
    yN      - y position within window
    yN_full - y position within full pad
    winHeight  - height of window
    height  - height of cursor
    full_height

    """
    def __init__(self,pad,bColHeader,bRowHeader):
        self.reset(pad)
    def reset(self,pad):
        self.color=cursorColor #XXX
        self.yN=1
        self.xN=1
        self.xN_full=1
        self.yN_full=1
        self.height=1
        self.width=1
        self.bActive=0
        self.bVisible=0
        self.refresh(pad)
    def refresh(self,pad):
        self.y=pad.y
        self.x=pad.x
        self.win_height=pad.height
        self.win_width=pad.width
        self.full_height=pad.full_height
        self.full_width=pad.full_height
        self.first_row=pad.first_row
        self.first_col=pad.first_col
    def move_to_row(self,row):
        self.yN_full=row
        if self.yN_full<0:
           self.yN_full=0
        elif self.yN_full>self.full_height:
           self.yN_full=self.full_height
        self.inc_v_first_react_constrained()
    def move_to_col(self,col):
        self.xN_full=col
        if self.xN_full<0:
           self.xN_full=0
        elif self.xN_full>self.full_width:
           self.yN_full=self.full_width
        self.inc_v_first_react_constrained()
    def inc_v(self,num):
        self.inc_v_abs(num)
        self.inc_v_rel_react()
        self.inc_v_first_react()
    def inc_h(self,num):
        self.inc_h_abs(num)
        self.inc_h_rel_react()
        self.inc_h_first_react()
    def inc_v_constrained(self,num):
        self.inc_v_abs(num)
        self.inc_v_first_react_constrained()
    def inc_h_constrained(self,num):
        self.inc_h_abs(num)
        self.inc_h_first_react_constrained()
    def inc_v_abs(self,num):
        self.orig_abs=self.yN_full;
        self.yN_full=self.yN_full+num
        if self.yN_full<0:
           self.yN_full=0
        elif self.yN_full>self.full_height:
           self.yN_full=self.full_height
    def inc_h_abs(self,num):
        self.orig_abs=self.xN_full;
        self.xN_full=self.xN_full+num
        if self.xN_full<0:
           self.xN_full=0
        elif self.xN_full>self.full_width:
           self.xN_full=self.full_width
    def inc_v_rel_react(self):
        self.orig_rel=self.yN;
        diff_abs=self.yN_full-self.orig_rel
        if self.yN+diff_abs < self.winHeight:
            self.yN=self.yN+diff_abs
        else:
            self.yN=self.winHeight
    def inc_h_rel_react(self):
        self.orig_rel=self.xN;
        diff_abs=self.xN_full-self.orig_rel
        if self.xN+diff_abs < self.winWidth:
            self.xN=self.xN+diff_abs
        else:
            self.xN=self.winWidth
    def inc_v_first_react(self):
        # PAD'S FIRST ROW
        diff_rel=self.yN-self.orig_rel
        self.first_row=self.first_row+diff_rel
    def inc_h_first_react(self):
        # PAD'S FIRST COL
        diff_rel=self.xN-self.orig_rel
    def inc_v_first_react_constrained(self):
        diff_abs=self.yN_full-self.orig_rel
        self.first_row+diff_abs
    def inc_h_first_react_constrained(self):
        diff_abs=self.xN_full-self.orig_rel
        self.first_row+diff_abs
    def yank_contents(self,OBJECT):
        # XXX
        pass
    def inc_block_v(self,num):
        # XXX
        pass
    def inc_block_h(self,num):
        # XXX
        pass
