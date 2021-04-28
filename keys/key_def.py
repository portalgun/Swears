class vim_key_def:
    def __init__(self):
        self.goMode = { "":"null"
                ,"g":["top",""]
        }
        self.visualMode = {"":"null"
            ,"j":["down",""]
            ,"k":["up",""]
            ,"G":["toLine",""]
            ,"h":["right",""]
            ,"l":["right",""]
            ,"g":["go",""]
        }

        self.searchMode = { "":"null"
                ,"RETURN":["Enter","table"]
                ,"ESC":["Cancel","table"]
                ,"n":["next","table"]
                ,"p":["previous","table"]
        }

        self.normalMode = { "":"null"
                #MODES
                ,"m":["menu","mode"]
                ,":":["ex","mode"]
                ,"M":["mod","mode"]
                ,"r":["run","mode"]
                ,"?":["revsearch","mode"]
                ,"v":["visual","mode"]
                ,"C-V":["block","mode"]
                ,"SLASH":["search","mode"]
                #CHANGE VIEW
                ,"TAB":["switch","view"]
                #,"c":["complete","view"]
                #,"i":["incomplete","view"]
                ,"q":["query","table"]
                ,"o":["sortToggle","table"]
                ,"a":["add","pad"]
                #SELECTIONS/CURSOR
                ,"SPACE":["select","table"]
                #MOVEMENT/NUMBER OPERATED
                ,"f":["Forward","focused"]
                ,"b":["Back","focused"]
                ,"j":["down","focused"]
                ,"k":["up","focused"]
                ,"G":["toLine","focused"]
                ,"h":["left","focused"]
                ,"l":["right","focused"]
                ,"g":["go","focused"]
                ,"H":["moveLeft","focused"]
                ,"L":["moveRight","focused"]
                ,"RIGHT":["incRight","focused"]
                ,"LEFT":["incLeft","focused"]
                ,"UP":["incUp","focused"]
                ,"DOWN":["incDown","focused"]
                #,"RETURN":["Enter","focused"]
                #,"ESC":["Cancel","focused"]
        }
        self.stringMode = { "":"null"
                ,"RETURN":["Return","string"]
                ,"ESC":["Cancel","string"]
                ,"BACKSPACE":["Backspace","string"]
                ,"UP":["prevHist","string"]
                ,"DOWN":["nextHist","string"]
                ,"LEFT":["cursorLeft","string"]
                ,"RIGHT":["cursorRight","string"]
        }
        self.menuMode = { "":"null"
                    ,"ESC":["Cancel","menu"]
                    ,"RETURN":["Return","menu"]
                    ,"h":["left","menu"]
                    ,"l":["right","menu"]
                    ,"j":["down","menu"]
                    ,"k":["up","menu"]
        }

        self.modMode = { "":"null"
            ,"D":["delete","mod"]
            ,"R":["rename","mod"]
            ,"M":["move","mod"]
            ,"d":["duplicate","mod"]
        }
