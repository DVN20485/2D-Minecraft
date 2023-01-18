import unittest
from game import *
import pygame as pg
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

g = Game() # new game object, initializes pygame
g.new() # initializes player, inventory, crafting etc


class InventoryClassTest(unittest.TestCase):
    
    # testing crafting by calling craft method 
    def test_inven_addItemEmpty(self): #add item to empty inven
        g.new() # initializes player, inventory, crafting etc
        g.playerInven.addItem('Wood', 5)
        self.assertEqual(g.playerInven.invDict['Wood'], 5)

    def test_inven_addItemStack1(self):#add item to inven with same item
        g.new() # initializes player, inventory, crafting etc
        g.playerInven.addItem('Wood', 5)
        g.playerInven.addItem('Wood', 3)
        self.assertEqual(g.playerInven.invDict['Wood'], 8)

    def test_inven_addItemStack2(self):#add item to inven with same item
        g.new() # initializes player, inventory, crafting etc
        g.playerInven.addItem('Wood', 5)
        g.playerInven.addItem('Stone', 3)
        self.assertEqual(g.playerInven.invDict['Stone'], 3)

    def test_inven_searchItem(self):
        g.new() # initializes player, inventory, crafting etc
        g.playerInven.addItem('Wood', 5)
        self.assertEqual(g.playerInven.searchInventory('Wood'), True)

    
    def test_inven_equipBlock(self):
        g.new() # initializes player, inventory, crafting etc
        g.playerInven.addItem('Wood', 5)
        g.playerInven.equipBlock()
        self.assertEqual(g.playerInven.block, 'Wood')
    
    def test_inven_equipBlock2(self):
        g.new() # initializes player, inventory, crafting etc
        #g.playerInven.addItem('Wood', 5)
        g.playerInven.equipBlock()
        self.assertEqual(g.playerInven.block, '')
    
    def test_inven_equipBlock3(self):
        g.new() # initializes player, inventory, crafting etc
        g.playerInven.addItem('Wood', 5)
        g.playerInven.equipBlock()
        g.playerInven.addItem('Stone', 5)
        g.playerInven.equipBlock()
        self.assertEqual(g.playerInven.block, 'Stone')

    def test_inven_equipBlock4(self):
        g.new() # initializes player, inventory, crafting etc
        g.playerInven.addItem('Wood', 5)
        g.playerInven.equipBlock()
        g.playerInven.addItem('Stone', 5)
        g.playerInven.equipBlock()
        g.playerInven.equipBlock()
        self.assertEqual(g.playerInven.block, 'Wood')

    def test_inven_equipTool(self):
        g.new() # initializes player, inventory, crafting etc
        g.playerInven.addItem('Iron pickaxe', 1)
        g.playerInven.equipTool()
        self.assertEqual(g.playerInven.tool, 'Iron pickaxe')
    
    def test_inven_equipTool2(self):
        g.new() # initializes player, inventory, crafting etc
        #g.playerInven.addItem('Iron pickaxe', 1)
        g.playerInven.equipTool()
        self.assertEqual(g.playerInven.tool, '')

    def test_inven_equipTool3(self):
        g.new() # initializes player, inventory, crafting etc
        g.playerInven.addItem('Wood pickaxe', 1)
        g.playerInven.equipTool()
        g.playerInven.addItem('Iron pickaxe', 1)
        g.playerInven.equipTool()
        self.assertEqual(g.playerInven.tool, 'Iron pickaxe')

    def test_inven_equipTool4(self):
        g.new() # initializes player, inventory, crafting etc
        g.playerInven.addItem('Wood pickaxe', 1)
        g.playerInven.equipTool()
        g.playerInven.addItem('Iron pickaxe', 1)
        g.playerInven.equipTool()
        g.playerInven.equipTool()
        self.assertEqual(g.playerInven.tool, 'Wood pickaxe')
        
    
    def test_inven_removeItem1(self):
        g.new() # initializes player, inventory, crafting etc
        g.playerInven.addItem('Iron pickaxe', 1)
        g.playerInven.removeItem('Iron pickaxe', 1)
        self.assertEqual(len(g.playerInven.invDict), 0)

    def test_inven_removeItem2(self):
        g.new() # initializes player, inventory, crafting etc
        g.playerInven.addItem('Iron pickaxe', 2)
        g.playerInven.removeItem('Iron pickaxe', 1)
        self.assertEqual(g.playerInven.invDict['Iron pickaxe'], 1)
    

if __name__ == '__main__':
    unittest.main()