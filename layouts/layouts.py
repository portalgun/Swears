import swears as sw

class layouts:
    """
    actNum
    """
    def __init__(self,layout_list):
        self.ALL=layout_list
        self.actNum=0
        self.main()
    def main(self):
        while True:
            self.draw()

            i=self.actNum
            if not self.ALL[i].OUT:
                continue

            self.actNum=self.actNum+self.ALL[i].OUT
            if self.actNum<0:
                self.actNum=len(self.ALL)-1
            elif self.actNum > len(self.ALL)-1:
                self.actNum=0
            self.ALL[i].OUT=[]
            self.redraw()
    def draw(self):
        i=self.actNum
        self.ALL[i].main()
    def redraw(self):
        i=self.actNum
        self.ALL[i].main_nokey()
    def create_layout(self):
        #XXX
        pass
