


import random as random


class rankItem():
     def __init__(self,child=None,parent=None):
        self.child = child 
        self.parent = parent
     def match(self,item2):
        response = input("1 or 2?")
        if response == 1:
            self.child = item2
            item2.parent = self
        else:
            self.parent = item2
            item2.child = self

        return  

def readCsv(filepath):
        currList = []
        with open(filepath, newline=',') as csvInput:
            currReader = csv.reader(csvInput, delimiter=" ", quotechar='|') 
            for row in currReader:
                currList.append(row)
        return currList



##basic matching system



def mainLoop():
    matchMaking(currList)
    if len(sameParent)==0:
        if len(sameChild)==0:
            printResults()
def runMatches():
    for i in sameParent():
        i[1].match(i[2])
    matchMaking(currList)
    for i in sameChild():
        i[1].match(i[2])
    matchMaking(currList)     

def matchMaking(currList):
    for item in currList:
        currItem = item
        for thing in currList:
            if thing != item:
                if thing.parent==item.parent:
                    sameParent.append([item,thing])
                if thing.child==item.child:
                    sameChild.append([item,thing])
    
#define match rules function, submitted list will have the lsit of the matches for each you want to randomize the order of the amtches
def matchRandomizing(submittedList):
    matchQueue=[]
    for i in currList:
        currone = random.randrange(0, (len(submittedList)-1), 1)
        currtwo = random.randrange(0, (len(submittedList)-1), 1)
        while currtwo==currone:
            currtwo = random.randrange(0, (len(submittedList)-1), 1)
        currmatch = [currone,currtwo]
        matchQueue.push(currmatch)

def printResults():

    for item in initialList:
        if item.parent==None:
            top = item
    current = top.child
    printResult = [top, current]
    while current.child!=None:
        printResult.append(current.child)
    print(printResult)

#filepath = "C:\Users\Ethan\Documents\GitHub\match-based-item-ranker\ranking-app"

currList = readCsv("C:\Users\Ethan\Documents\GitHub\match-based-item-ranker\ranking-app")
initialList = currList
sameParent = []
sameChild = []




  