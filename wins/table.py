class table:
    def __init__(self,List_all,*args):
        #args[0] is order list, args[1] is reverse sort
        if len(args) > 0 and len(List_all) == len(args[0]):
            self.order=args[0]
        elif len(args) > 0:
            pass
            #XXX warning/error
        # XXX ADD IN SORTING ARG
        else:
            self.order=list(range(0,len(List_all)))
        self.length=List_all.length
        self.names=List_all.names
        self.lists=List_all.lists
        self.sort_fields()
        self.sort_lists()
    def refresh(self,*args):
        if len(args)>0 and args[0][1]=="table":
            pass
        if len(args)>0 and args[0][1]=="List_all":
            self.List_all.refresh(args[0])
    def sort_fields(self,fieldOrder):
        listNew=[]
        namesNew=[]
        for I in range(0,len(fieldOrder)-1):
            i=fieldOrder[I]
            namesNew.append(self.names[i])
            listsNew.append(self.lists[i])
        self.lists=listsNew
        self.names=namesNew
    def sort_lists(self,*args):
        self.complete=list(zip(self.lists[0]))
        for l in range(1,self.length-1):
            self.complete.append(self.lists[l])
        if len(args) > 0 and args[0]==True:
            self.complete.sort(reverse=True)
        else:
            self.complete.sort(reverse=False)
