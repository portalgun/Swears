import curses
class screen:
    """
    PROPERTIES
      height
      width
      status
    """
    def __init__(self,stdscrn):
        self.stdscr=stdscrn
        self.refresh()
    def clear(self):
        self.stdscr.clear()
    def refresh(self):
        self.stdscr.clear()
        self.height = curses.LINES
        self.width = curses.COLS
        if curses.has_colors():
            curses.start_color
            curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
            curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
            curses.init_pair(3,curses.COLOR_GREEN,curses.COLOR_BLACK)
