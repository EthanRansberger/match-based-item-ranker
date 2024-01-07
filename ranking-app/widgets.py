# -*- coding: utf-8 -*-
"""
*****************************************************************************
 * Copyright (c) 2023 Tolsimir
 *
 * The program "Object Creator" and all subsequent modules are licensed
 * under the GNU General Public License version 3.
 *****************************************************************************
"""
from ast import MatchAs
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDialog, QMenu, QGroupBox, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QTabWidget, QToolButton, QComboBox, QScrollArea, QScrollBar, QPushButton, QLineEdit, QLabel, QCheckBox, QSpinBox, QDoubleSpinBox, QListWidget, QFileDialog
from PyQt5 import uic, QtGui, QtCore
from PIL import Image, ImageGrab, ImageDraw
from PIL.ImageQt import ImageQt
from copy import copy
import io
import os.path
from os import getcwd
import numpy as np
from pkgutil import get_data
import random as random

import auxiliaries as aux

from customwidgets import RemapColorSelectWidget
import customwidgets as cwdg

from rctobject import constants as cts
from rctobject import sprites as spr
from rctobject import palette as pal
from rctobject import objects as obj


class comparisonWidget(QWidget):
    def __init__(self, inputList, mainWindow):
        super().__init__()
        uic.loadUi(aux.resource_path('gui/itemComparisonWindow.ui'), self)
        print("comparison initiated")
       #self.matchList= [[]]
        self.matches = 0
        #self.inputList = []
        #print(inputList)
       # self.inputList = ','.split(inputList[0][0])
       # print(self.inputList)
        #self.inputList = inputList
        self.tempList = inputList 
        self.inputList = []
        print(self.tempList)
        for i in self.tempList:
            g = listItem(self,i)
            self.inputList.append(g)
        self.matchOrder=[]
        self.itemone=0
        self.itemtwo=0
        self.sameParent = []
        self.sameChild = []
        self.mainWindow = mainWindow
        print(self.inputList)
        self.currList = self.inputList

        self.itema = listItem(self,"")
        self.itemb = listItem(self,"")
        self.tier = "parent"


        self.itemOneButton = self.findChild(QPushButton,"itemOneButton")
        self.itemTwoButton = self.findChild(QPushButton,"itemTwoButton")

        self.itemOneButton.clicked.connect(self.itemOnePressed)
        self.itemTwoButton.clicked.connect(self.itemTwoPressed)
        

      #  for i in self.inputList:
        
        #
         #  curr = random.randrange(0, (len(self.inputList)-1), 1)
        self.mainLoop()
    
        # self.matchOrder.append(self.inputList[curr])
        # self.inputList.remove(curr)
    def itemOnePressed(self):
        print("item 1 pressed")
        self.itema.child = self.itemb
        self.itemb.parent = self.itema
        if self.tier == "parent" and len(self.sameParent)>=1:
            print("parent tier pop")
            self.sameParent.pop()
           # self.runMatches()
            
           
        elif len(self.sameChild)>=1:
            print("child tier pop")
            self.sameChild.pop()
            
           # self.runMatches()
        #self.nextRound()
        """
        self.currList.append(self.currList.pop(self.currList.index(self.itema)))
        self.currList.append(self.currList.pop(self.currList.index(self.itemb)))"""
        self.currList.pop(self.currList.index(self.itemb))
        self.currList.pop(self.currList.index(self.itema))
        self.currList.append(self.itema)
        self.currList.append(self.itemb)
        self.matchMaking(self.currList)
    def itemTwoPressed(self):
        print("item 2 pressed")
        self.itemb.child = self.itema
        self.itema.parent = self.itemb
        if self.tier == "parent":
            self.sameParent.pop()
        
        else:
            self.sameChild.pop()
        self.currList.append(self.currList.pop(self.currList.index(self.itema)))
        self.currList.append(self.currList.pop(self.currList.index(self.itemb)))
        for i in self.currList:
            print(i.string)
        self.matchMaking(self.currList)
       # self.nextRound()
    def compareItems(self,itema,itemb):
        print("comparing items")
        self.itema = itema
        self.itemb = itemb
        self.itemOneButton.setText(itema.string)
        self.itemTwoButton.setText(itemb.string)
 
    def nextRound(self, winner):
        print("next round")
        return
        #####THE INITIAL ROUNDS NEED TO ENSURE THAT EVERYONE HAS A CHILD BY THE END 
        ## in the event of odd number of entries, for example, the first winner in the next round will play the only one without a child. 
        ##actually this isnt even true! it still works without needing to do that because lets say there are 5. 1 beats 2, 3 beats 4. Then 1 plays 3, then 1 will play 4 even if it really should be 1 plays 4 in TOURNAMENT mode
        ####tournament mode, may be a potential update!  


        ##THis should be the only condition you may need to check for, then the logic explained below should work:

        #first find any with the same parent (including null), add to list, then randomly select match
        #if noone has the same parent, find one with the same child, compare, 
        #If everyone has a unique parent and a unique child, then there should be a complete chain in order of how you ranked.
        
        #for item in list of items, take an item, then..
        ##for item2 in list of items that doesnt equal item, see if they have the same parent
        
        #same as above, add to the same list of new matches the matches of those with the same parents INCLUDING whoever loses the parent vs. parent match when now there are two with the same parent! 

        #return a list of the next sequence of matches!

    def mainLoop(self):
        print("starting main loop")
        self.matchMaking(self.inputList)
        #if len(self.sameParent)>=1 and len(self.sameChild)>=1:
           # self.runMatches()
        #if len(self.sameParent)==0:
        #    if len(self.sameChild)==0:
        #        self.printResults()
    def runMatches(self):
        print("running matches")
        #for i in self.sameParent():
          #  i[1].match(i[2])
        if len(self.sameParent)>=1:
            print("same parent match")
            print(self.sameParent)
            #print(self.sameParent)
            self.tier = "parent"
            i = self.sameParent[0]
            self.compareItems(i[0],i[1])
           # self.matchMaking(self.inputList)
        elif len(self.sameChild)>=1:
        #for i in self.sameChild():
         #   i[1].match(i[2])
            print("same child match")
            print(self.sameChild)
            self.tier = "child"
            i = self.sameChild[0]
            
            self.compareItems(i[0],i[1])
           # self.matchMaking(self.inputList)     
        #self.compareItems(self.itema,self.itemb)
        else:
            self.matchMaking(self.inputList)

    def matchMaking(self,currList):
        print("making matches")
        #print(currList)
        if len(currList)==0:
            currList = self.inputList
            self.currList=currList
            testingWin = True
        if len(self.sameParent)==0 and len(self.sameChild)==0:
            for item in currList:
            # print(item.string)

                for thing in currList:
                    #print(thing.string)
                    if thing != item:
                    # print(thing.string,thing.parent)
                    # print(item.string,item.parent)
                        if thing.parent==item.parent:
                            self.sameParent.append([item,thing])
                        elif thing.child==item.child:
                            self.sameChild.append([item,thing])
            print("same parent")
            print(self.sameParent)
            print("same child")
            print(self.sameChild)
            if len(self.sameParent)==0 and len(self.sameChild)==0:
                self.printResults
            else:
                self.runMatches()
        else:
            self.runMatches()
    #define match rules function, submitted list will have the lsit of the matches for each you want to randomize the order of the amtches
    def matchRandomizing(self,submittedList):
        print("randomizing match")
        matchQueue=[]
        for i in submittedList:
            currone = random.randrange(0, (len(submittedList)-1), 1)
            currtwo = random.randrange(0, (len(submittedList)-1), 1)
            while currtwo==currone:
                currtwo = random.randrange(0, (len(submittedList)-1), 1)
            currmatch = [currone,currtwo]
            matchQueue.push(currmatch)

    def printResults(self):
        print("printing results")
        # refer to main window, have main window replace the comparison widget with the result widget!
        return
class resultsWidget(QWidget):
    def __init__(self):
        super().__init__()
##### Settings window


class listItem():
    def __init__(self,widget,string,parent=None,child=None):
        self.widget = widget
        self.string = string
        self.parent = parent
        self.child = child
    def match(self,opponent):
        return
        
        ###compare all items with no child or no parent!
        ##then compare items with same parent or same child!





"""comparison process

        what it does is it creates a bracket 
        
        there will be tiers of a loser bracket 
        
        first divide all items by 2 
        
        so there will be a dictionary, for every item in the list
        
        the definition will be all of the items it was picked over
        
        If there is a chain, then there will be a rematch to break the chain of earlier opponents that maybe you forgot your preference
        
        or changed your mind as you kept running the matches!"""













