import cmd
import curses
import swears as sw
import sys

class inkey():
    def __init__(self):
        self.invalid=0
        self.cmd=""
        self.rep=""
        self.hist=[]
        settings=sw.settings()
        strdefs=sw.str_cmd_def()
        if settings.keyDef=="vim":
            self.defs=sw.key_def.vim_key_def()
        if sys.platform=="linux":
            self.scancodes=sw.scancodes.linux_codes().dic

    def update(self,layout):
        mode=layout.mode
        KEY=layout.KEY
        self.stri=layout.stri
        self.cmd=""
        self.rep=""
        if self.cmd:
            self.hist.append(self.cmd)

        if KEY==[]:
            return
        #raise NameError(KEY)
        KEY=self.scancode2keycode(KEY)
        self.keycode2cmd(KEY,mode)

    def scancode2keycode(self,KEY):
        if len(KEY)==1:
            KEY=str(KEY[0])
        else:
            KEY=str(KEY)

        KEY=self.scancodes.get(KEY)
        return KEY

    def keycode2cmd(self,KEY,mode):
        self.bExecute=1
        if mode=="normal":
            if not KEY:
                return
            elif KEY.isnumeric():
                self.rep=self.rep + KEY
                #continue
            elif not self.rep:
                self.rep=1
            self.cmd=self.defs.normalMode.get(KEY)
            if self.cmd=="toLine" and self.rep==1:
                self.cmd=["bottom",""]
        elif mode == "go":
            self.cmd=self.defs.goMode.get(KEY)
        elif mode == "visual":
            self.cmd=self.defs.visualMode.get(KEY)
        elif mode == "search":
            self.cmd=self.defs.searchMode.get(KEY)
        elif mode == "revsearch":
            self.cmd=self.defs.searchMode.get(KEY)
            if self.cmd=="next":
                self.cmd="previous"
            elif self.cmd=="previous":
                self.cmd="next"
        elif mode == "menu":
            self.cmd=self.defs.menuMode.get(KEY)
        elif mode == "mod":
            self.cmd=self.defs.modMode.get(KEY)
        elif mode == "string":
            self.cmd=self.defs.stringMode.get(KEY)
            bText=0
            self.bExecute=0
            if not self.cmd:
                self.cmd=KEY
                bText=1
            self.handle_string_char(bText)
        else:
            self.bExecute=0

        if self.bExecute==1:
            return
    def handle_string_char(self,bText):
        self.bExecute=1
        if   self.cmd[0]=="Return":
            self.handle_string_cmd
        elif self.cmd[0]=="Cancel":
            self.stri.text=""
        elif self.cmd[0]=="Backspace":
            self.stri.text=self.stri.text[:-1]
            self.stri.position -= 1
            self.stri.maxPosition -=1
        elif self.cmd[0]=="cursorLeft" and self.stri.position > 0:
            self.stri.position -= 1
        elif self.cmd[0]=="cursorRight" and self.stri.position <= self.stri.maxPosition:
            self.stri.position += 1
        elif self.cmd[0]=="prevHist" and self.stri.histInd > 0:
            self.stri.histInd -= self.stri.histInd
        elif self.cmd[0]=="nextHist" and self.stri.histInd < len(self.stri.hist):
            self.stri.histInd += self.stri.histInd
        elif bText==1:
            self.stri.text=stri.text + self.cmd
            self.stri.position += 1
            self.stri.maxPosition +=1
        else:
            self.bExecute=0
    def handle_string_cmd(self):
    #XXX col and full
            self.cmd=""
            if self.stri.submode=="stringYN":
                self.cmd=stringYNmode.get(self.stri.text)
            elif self.stri.submode=="stringYNstrict":
                self.cmd=stringYNstrictMode.get(self.stri.text)
            elif self.stri.submode=="exCmd":
                self.cmd=exCmd.get(self.stri.text)
            else:
                self.bExecute=0
                return

            if not self.cmd:
                self.stri.hist.append(self.stri.text)
                self.invalid=1
                self.bExecute=0
            else:
                self.stri.hist.append(self.stri.text)
                self.stri.text=""
    def convertKey(self,KEY):
        return KEYnew
