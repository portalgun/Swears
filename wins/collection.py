class List_all:
    def __init__(self,*args):
        self.lists=[]
        self.names=[]
        self.length=0
    def refresh(self,*args)
        if len(args)>0 and args[0][1]=="List_all":
            cmd=args[0]
        if len(args)>0 and args[0][1]=="query":
            self.query(args[0])
    def add_LIST(self,LIST):
        if self.length == 0 or self.length==len(LIST):
            self.lists.append(LIST.List)
            self.names.append(LIST.name)
            if self.length==0:
                self.length=len(LIST)
        else:
            pass
            #XXX warning/error
