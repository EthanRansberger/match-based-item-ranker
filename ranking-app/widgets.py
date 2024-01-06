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
        self.matchList= [[]]
        self.matches = 0
        #self.inputList = []
        self.inputList = ','.split(inputList[0][0])
        print(self.inputList)
        self.matchOrder=[]
        self.itemone=0
        self.itemtwo=0
        self.sameParent = []
        self.sameChild = []
        self.mainWindow = mainWindow
       # for i in self.inputList:
        
        
        #   curr = random.randrange(0, (len(self.inputList)-1), 1)
        """if curr in self.matchOrder:
        while curr in self.matchOrder:
        curr=random.randrange(0,self.matches,1)"""
    
        # self.matchOrder.append(self.inputList[curr])
        # self.inputList.remove(curr)
    def compareItems(self):
     """   if itemone=="win":
            itemtwo.parent==itemone
            itemone.child==itemtwo
        if item """
    def nextRound(self):
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
        self.matchMaking(self.inputList)
        if len(self.sameParent)==0:
            if len(self.sameChild)==0:
                self.printResults()
    def runMatches(self):
        for i in self.sameParent():
            i[1].match(i[2])
        self.matchMaking(self.inputList)
        for i in self.sameChild():
            i[1].match(i[2])
        self.matchMaking(self.inputList)     

    def matchMaking(self,currList):
        for item in currList:
            
            for thing in currList:
                if thing != item:
                    if thing.parent==item.parent:
                        self.sameParent.append([item,thing])
                    if thing.child==item.child:
                        self.sameChild.append([item,thing])
        
    #define match rules function, submitted list will have the lsit of the matches for each you want to randomize the order of the amtches
    def matchRandomizing(self,submittedList):
        matchQueue=[]
        for i in submittedList:
            currone = random.randrange(0, (len(submittedList)-1), 1)
            currtwo = random.randrange(0, (len(submittedList)-1), 1)
            while currtwo==currone:
                currtwo = random.randrange(0, (len(submittedList)-1), 1)
            currmatch = [currone,currtwo]
            matchQueue.push(currmatch)

    def printResults(self):
        # refer to main window, have main window replace the comparison widget with the result widget!
        return
class resultsWidget(QWidget):
    def __init__(self):
        super().__init__()
##### Settings window


class listItem():
    def __init__(self,parent,child):
        self.parent = parent
        self.child = child
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













