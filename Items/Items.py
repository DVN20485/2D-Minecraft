import pygame
from os import path

item_folder = path.dirname(__file__)

class Item:
    def __init__(self, itemName, recipe, craftable,smeltable,placeable, tool): #parameters for the Item Class
        self.itemName = itemName
        self.recipe = recipe                    
        self.craftable = craftable
        self.smeltable = smeltable
        self.placeable = placeable
        self.tool = tool            #contains whether an item is a material block or a tool(can add more types later)


# recipes stored such that 
# stonePickaxe.recipe returns [('wood', 2), ('stone', 3)] 
# recipe[0] returns ('wood', 2)
# recipe[0][0] returns wood
craftList = []
def getRecipe(itemName): #returns recipe of an item in a paired array

    for x in itemList:
        if(x.itemName == itemName):
            itemCheck = True
            if(x.craftable or x.smeltable):
                return x.recipe
            else:
                return 'Item has no recipe'
                
    return 'Item does not exist'

def getMaterials(itemName): #return a list of materials an object needs to be crafted
    materialList = []
    for x in itemList:
        if(x.itemName == itemName):
            itemCheck = True
            if(x.craftable):
                for i in range(len(x.recipe)):
                    materialList.append(x.recipe[i][0])
                return materialList
            else:
                return 'Item has no recipe'
    return 'Item does not exist'

def craftableList(): #return list of items names that are craftable(not checking if the player has the resources for it)
    craftList = []
    for x in itemList:
        if(x.craftable):
            craftList.append(x.itemName)
    return craftList

def smeltableList(): #return list of items names that are smeltable(not checking if the player has the resources for it)
    smeltList = []
    for x in itemList:
        if(x.smeltable):
            smeltList.append(x.itemName)
    return smeltList

def blockList(): #return list of items names that are craftable(not checking if the player has the resources for it)
    blockList = []
    for x in itemList:
        if(x.placeable):
            blockList.append(x.itemName)
    return blockList

def toolList(): #return list of items names that are craftable(not checking if the player has the resources for it)
    toolList = []
    for x in itemList:
        if(x.tool):
            toolList.append(x.itemName)
    return toolList

#populate the item list
itemList = []

itemFile = open(path.join(item_folder, "Items.txt"),"r", encoding="utf-8")

for itemLine in itemFile:
    #loop through the Items.txt and split each line
    lineList = (itemLine.split('-'))
    itemName = lineList[0]

    tempRecipe = lineList[1].split(',')
    itemRecipe = []

    #make sure quanitities are stored adjacent to their material
    for x in range(len(tempRecipe) -1):      
        try:
            temp = (tempRecipe[x], int(tempRecipe[x+1]))
            itemRecipe.append(temp)
        except:
            continue
    
    itemCraft = (lineList[2] == 'True')
    itemSmelt = (lineList[3] == 'True')
    itemBlock = (lineList[4] == 'True')
    itemTool = (lineList[5].split('\n')[0] == 'True')
    
    tempItem = Item(itemName, itemRecipe, itemCraft, itemSmelt,itemBlock, itemTool)
    itemList.append(tempItem)

smeltableList()
craftableList()
blockList()
toolList()

