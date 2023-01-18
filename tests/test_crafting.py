import unittest
from game import *
import pygame as pg
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

g = Game() # new game object, initializes pygame
g.new() # initializes player, inventory, crafting etc


class CraftingTableClassTest(unittest.TestCase):
    
    # testing crafting by calling craft method 
    def test_craft_noResources_emptyInv(self):
        #tests the boundary case where player tries to craft with no resources whatsoever. Should add nothing to inventory
        g.new() # initializes player, inventory, crafting etc
        g.craftingTable.on_interact()
        g.craftingTable.craft(pg.K_1)
        g.craftingTable.craft(pg.K_2)
        g.craftingTable.craft(pg.K_3)
        g.craftingTable.craft(pg.K_4)
        g.craftingTable.craft(pg.K_5)
        self.assertEqual(len(g.playerInven.invDict), 0)
        

    def test_craft_insufResources_inv3Wood(self):
        g.new() # initializes player, inventory, crafting etc
        #tests the case where the player does not quite have enough resources to craft anything
        #takes 3 wood as it is just 1 wood shy of being able to craft crafting table (boundary case)
        #sufficient to prove for all cases where player has insufficient material to craft any item
        g.playerInven.addItem("Wood", 3)
        g.craftingTable.on_interact()
        g.craftingTable.craft(pg.K_1) #all these inputs should result in no change
        g.craftingTable.craft(pg.K_2)
        g.craftingTable.craft(pg.K_3)
        g.craftingTable.craft(pg.K_4)
        g.craftingTable.craft(pg.K_5)
        self.assertEqual(len(g.playerInven.invDict), 1) #should be length 1 due to wood
        

    def test_craft_sufResourcesForCraftTable_inv1CraftTable(self):
        g.new() # initializes player, inventory, crafting etc
        g.playerInven.addItem("Wood", 4)
        g.craftingTable.on_interact()
        g.craftingTable.craft(pg.K_1) #this input should add crafting table to inv
        g.craftingTable.craft(pg.K_2) #the rest should do nothing
        g.craftingTable.craft(pg.K_3)
        g.craftingTable.craft(pg.K_4)
        g.craftingTable.craft(pg.K_5)
        self.assertTrue(g.playerInven.searchInventory("Crafting Table"))
    
    def test_craft_sufResourcesForCraftTableButTryTwice_inv1CraftTable(self):
        g.new() # initializes player, inventory, crafting etc
        g.playerInven.addItem("Wood", 4)
        g.craftingTable.on_interact()
        g.craftingTable.craft(pg.K_1) #this input should add crafting table to inv
        g.craftingTable.craft(pg.K_1) #repeated to make sure it only crafts once ie this should do nothing
        g.craftingTable.craft(pg.K_2) #the rest should do nothing
        g.craftingTable.craft(pg.K_3)
        g.craftingTable.craft(pg.K_4)
        g.craftingTable.craft(pg.K_5)
        g.playerInven.removeItem("Crafting Table", 1) #should remove the only crafting table in inv
        self.assertTrue(not g.playerInven.searchInventory("Crafting Table")) #no crafting table in inv

    def test_craft_sufResourcesForCraftTableWoodPick_invHasCraftTableOrWoodPick(self):
        g.new() # initializes player, inventory, crafting etc
        g.playerInven.addItem("Wood", 5)
        g.craftingTable.on_interact()
        g.craftingTable.craft(pg.K_1) #this input should add crafting table or wood pickaxe to inv. Doesn't really matter which
        g.craftingTable.craft(pg.K_1) #repeated to make sure it only crafts once ie this should do nothing
        g.craftingTable.craft(pg.K_2) #the rest should do nothing
        g.craftingTable.craft(pg.K_3)
        g.craftingTable.craft(pg.K_4)
        g.craftingTable.craft(pg.K_5)
        self.assertTrue(g.playerInven.searchInventory("Crafting Table") or g.playerInven.searchInventory("Wood pickaxe"))
    
    def test_craft_sufResourcesForCraftTableAndWoodPick_invHasCraftTableAndWoodPick(self):
        g.new() # initializes player, inventory, crafting etc
        g.playerInven.addItem("Wood", 10)
        g.craftingTable.on_interact()
        g.craftingTable.craft(pg.K_1) #this input should add crafting table or wood pickaxe to inv. Doesn't really matter which
        g.craftingTable.craft(pg.K_2) #this input should add the other item
        #player should now not have sufficient resources to craft anything so
        g.craftingTable.craft(pg.K_1) #both repeated to make sure it only crafts once per item ie these should do nothing
        g.craftingTable.craft(pg.K_2) 
        g.craftingTable.craft(pg.K_3) #the rest should do nothing
        g.craftingTable.craft(pg.K_4)
        g.craftingTable.craft(pg.K_5)
        self.assertTrue(g.playerInven.searchInventory("Crafting Table") and g.playerInven.searchInventory("Wood pickaxe"))
    
    def test_craft_sufResourcesForAllButtons_invHasFiveNewItems(self):
        g.new() # initializes player, inventory, crafting etc
        g.playerInven.addItem("Wood", 99)
        g.playerInven.addItem("Stone", 99)
        g.playerInven.addItem("Iron Ingot", 99)
        g.craftingTable.on_interact()
        g.craftingTable.craft(pg.K_1) #each input should add a new item to the inventory
        g.craftingTable.craft(pg.K_2) 
        g.craftingTable.craft(pg.K_3) 
        g.craftingTable.craft(pg.K_4)
        g.craftingTable.craft(pg.K_5)
        self.assertEqual(len(g.playerInven.invDict), 8)
    

if __name__ == '__main__':
    unittest.main()