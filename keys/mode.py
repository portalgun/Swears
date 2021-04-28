class mode:
    def __init__(self):
        self.mode="normal"
        self.string=""
        self.bExecute=0
    def refresh(self):
        self.current=stdscr.getkey()
        self.parse_key
    def parse_key(self):
        if self.mode=="normal":
            char=normalMode.get(self.current)
            # XXX handle numbers differently
        elif self.mode=="visual":
            char=visualMode.get(self.current)
            # XXX handle numbers differently
        elif self.mode=="goMode":
            char=goMode.get(self.current)
            # XXX NEED TO FIGURE OUT DETAILS HERE
        elif self.mode=="menu":
            char=menuMode.get(self.current)
            if char == "Cancel":
                self.mode=self.modePrevious
                return
        elif self.mode=="mod":
            char=modMode.get(self.current)
            if char == "Cancel":
                self.mode=self.modePrevious
                return
        elif self.mode=="string":
            char=stringMode.get(self.current)
            if char == "":
                char=self.current
                self.string=self.string + char
            elif char == "Return":
                self.Execute=1
            elif char == "Cancel":
                self.string=""
                self.mode=self.modePrevious
                return

        if char == "":
            return
        else:
            self.cmd=char
            self.bExecute=1
