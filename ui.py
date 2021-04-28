import layouts
import key
import curses

def main(stdscr):
    selection='default'

    #INIT WINDOWS
    Layout=layout(stdscrn,selection)

    #INIT KEY
    Key=inkey()

    while True:
        stdscr.clear()
        Layout.draw(stdscr)
        Layout.refresh(stdscr)
        Key.update(stdscr,Layout.mode,Layout.str)
        Layout.update(stdscr,Key)

# -----------------------------------------

if __name__ == "__main__":
    curses.wrapper(main)

#TODO
# HIDDEN VIEWS, c,i,TAB
# bottom command shell
