#!/usr/bin/env ipython
import curses
import sys
from pprint import pprint

sys.path.append("/home/dambam/Code/py/")
import swears


def scrn_fun(stdscr):

    frmat1=[[1,1],[.5, .5],[[[1,1],[.5,.5],[]],0,0,0] ]
    frmat2=[[1,1],[.5, .5],[0,[[1,1],[.5,.5],[]],0,0] ]
    statusHeight=5
    layout1=swears.layout(0,stdscr,frmat1,statusHeight)
    layout2=swears.layout(1,stdscr,frmat2,statusHeight)
    layout=[layout1, layout2]

    LAYOUTS=swears.layouts(layout);


# -----------------------------------------

if __name__ == "__main__":
    curses.wrapper(scrn_fun)

#TODO
# HIDDEN VIEWS, c,i,TAB
# bottom command shell
