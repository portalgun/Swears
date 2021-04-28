class str_cmd_def:
    def __init__(self):
        self.stringYNcmd = { "":"Cancel"
                    ,"1":"y"
                    ,"Y":"y"
                    ,"y":"y"
                    ,"yes":"y"
                    ,"Yes":"y"
                    ,"YES":"y"
                    ,"n":"n"
                    ,"N":"n"
                    ,'0':"n"
                    ,"no":"n"
                    ,"No":"n"
                    ,"NO":"n"
                }

        self.stringYNstrictCmd = { "":"Cancel"
                        ,"YES":"y"
                        ,"NO":"n"
        }

        self.exCmd = { "":"Cancel"
                    ,"q":"quit"
                    ,"delete":"delete"
        }
