from ast import Index
from json import tool
from operator import eq
import pygame as pg
from Items.Items  import *
from configurations import *

class Inventory:
    def __init__(self):
        self.invDict = {}
        self.tool = ''
        self.block = ''
        self.visible = False  #variable controller for show/hide inventory
    
    def addItem(self, itemName, itemQuantity):
        #check if the item already exists in the Inventory
        quantity = 0

        if self.invDict:#check if inventory is empty
            if itemName in self.invDict:
                quantity += (self.invDict[itemName] + itemQuantity)
                self.invDict[itemName] = quantity     
            else:
                self.invDict[itemName] = itemQuantity          
        else:#if inventory empty just add the item
            self.invDict[itemName] = itemQuantity

    def removeItem(self, itemName, itemQuantity):#assuming player has the materials
        quantity = self.invDict[itemName]
        quantity -= itemQuantity
        if quantity == 0:
            del self.invDict[itemName]
        else: 
            self.invDict[itemName] = quantity

    def searchInventory(self, itemName):#check if player has a certain item
        if itemName in self.invDict:
            return True
        return False
    
    def equipTool(self):

        tools = []
        #populate tool list
        for item in self.invDict.keys():
            if item in toolList():
                tools.append(item)

        
        if (self.tool == ''): #if nothing equipped
            if tools:    #If theres items in inventory
                self.tool = tools[0]
            else:
                #print("Nothing to equip")
                self.tool = ''
        else:
            if(tools):
                if(self.tool == tools[-1]):
                    self.tool = tools[0]
                else:
                    if (self.tool in tools):
                        self.tool = tools[tools.index(self.tool) + 1]
                    else:
                        if(self.invDict):
                            self.tool = tools[0]
                        else:
                            self.tool = ''
                            #print('Nothing to equip')
            else:
                self.tool = ''      
        #print(self.tool)

    def equipBlock(self):

        blocks = []
        #populate tool list
        for item in self.invDict.keys():
            if item in blockList():
                blocks.append(item)

        
        if (self.block == ''): #if nothing equipped
            if blocks:    #If theres items in inventory
                self.block = blocks[0]
            else:
                self.block = ''
               # print("Nothing to equip")
        else:
            if(blocks):
                if(self.block == blocks[-1]):
                    self.block = blocks[0]
                else:
                    if (self.block in blocks):
                        self.block = blocks[blocks.index(self.block) + 1]
                    else:
                        if(self.invDict):
                            self.block = blocks[0]
                        else:
                            self.block = ''
                            #print('Nothing to equip')
            else:
                self.block = ''      
        #print(self.block)
        