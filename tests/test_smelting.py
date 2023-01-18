import unittest
from game import *
import pygame as pg
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

g = Game() # new game object, initializes pygame
g.new() # initializes player, inventory, smelting etc


class FurnaceClassTest(unittest.TestCase):
    
    def test_smeltButton1_sufResourcesFor1_smeltTrue(self):
        g.new() # initializes player, inventory, smelting etc
        g.playerInven.addItem("Wood", 3)
        g.playerInven.addItem("Iron Ore", 1)
        g.furnace.on_interact()
        self.assertTrue(g.furnace.smelt(pg.K_6))
    
    def test_smeltButton2_sufResourcesFor1_smeltTrue(self):
        g.new() # initializes player, inventory, smelting etc
        g.playerInven.addItem("Wood", 3)
        g.playerInven.addItem("Iron Ore", 1)
        g.playerInven.addItem("Copper Ore", 1)
        g.furnace.on_interact()
        self.assertTrue(g.furnace.smelt(pg.K_7))

    def test_smeltButton3_sufResourcesFor1_smeltTrue(self):
        g.new() # initializes player, inventory, smelting etc
        g.playerInven.addItem("Wood", 3)
        g.playerInven.addItem("Iron Ore", 1)
        g.playerInven.addItem("Copper Ore", 1)
        g.playerInven.addItem("Gold Ore", 1)
        g.furnace.on_interact()
        self.assertTrue(g.furnace.smelt(pg.K_8))

    def test_smeltButton4_sufResourcesFor1_smeltTrue(self):
        g.new() # initializes player, inventory, smelting etc
        g.playerInven.addItem("Wood", 3)
        g.playerInven.addItem("Iron Ore", 1)
        g.playerInven.addItem("Copper Ore", 1)
        g.playerInven.addItem("Gold Ore", 1)
        g.playerInven.addItem("Diamond Ore", 1)
        g.furnace.on_interact()
        self.assertTrue(g.furnace.smelt(pg.K_9))

    def test_smeltButton5_sufResourcesFor1_smeltTrue(self):
        g.new() # initializes player, inventory, smelting etc
        g.playerInven.addItem("Wood", 3)
        g.playerInven.addItem("Iron Ore", 1)
        g.playerInven.addItem("Copper Ore", 1)
        g.playerInven.addItem("Gold Ore", 1)
        g.playerInven.addItem("Diamond Ore", 1)
        g.playerInven.addItem("Phosphorus Ore", 1)
        g.furnace.on_interact()
        self.assertTrue(g.furnace.smelt(pg.K_0))
    
    # testing smelting by calling smelt method 
    def test_smelt_noResources_emptyInv(self):
        #tests the boundary case where player tries to smelt with no resources whatsoever. Should add nothing to inventory
        g.new() # initializes player, inventory, smelting etc
        g.furnace.on_interact()
        g.furnace.smelt(pg.K_6)
        g.furnace.smelt(pg.K_7)
        g.furnace.smelt(pg.K_8)
        g.furnace.smelt(pg.K_9)
        g.furnace.smelt(pg.K_0)
        self.assertEqual(len(g.playerInven.invDict), 0)
        

    def test_smelt_insufResources0Ore_inv3Wood(self):
        g.new() # initializes player, inventory, smelting etc
        #tests the case where the player does not have enough ore to smelt anything but has enough wood
        #takes 3 wood (minimum required for smelting)
        #sufficient to prove for all cases where player has insufficient ore to smelt any item
        g.playerInven.addItem("Wood", 3)
        g.furnace.on_interact()
        g.furnace.smelt(pg.K_6) #all these inputs should result in no change
        g.furnace.smelt(pg.K_7)
        g.furnace.smelt(pg.K_8)
        g.furnace.smelt(pg.K_9)
        g.furnace.smelt(pg.K_0)
        self.assertEqual(len(g.playerInven.invDict), 1) #should be length 1 due to wood
        

    def test_smelt_insufResources0Wood_inv1Ore(self):
        g.new() # initializes player, inventory, smelting etc
        g.playerInven.addItem("Iron Ore", 1)
        g.furnace.on_interact()
        g.furnace.smelt(pg.K_6) #all these inputs should result in no change
        g.furnace.smelt(pg.K_7)
        g.furnace.smelt(pg.K_8)
        g.furnace.smelt(pg.K_9)
        g.furnace.smelt(pg.K_0)
        self.assertEqual(len(g.playerInven.invDict), 1) #should be length 1 for just ore
    
    def test_smelt_sufResourcesForSmelt_inv1IronIngot(self):
        #when this passes, no longer necessary to check every button as they have been given ample chance to activate
        g.new() # initializes player, inventory, smelting etc
        g.playerInven.addItem("Wood", 3)
        g.playerInven.addItem("Iron Ore", 1)
        g.furnace.on_interact()
        g.furnace.smelt(pg.K_6) #should add 1 Iron Ingot to inv
        g.furnace.smelt(pg.K_7) #rest of inputs should do nothing
        g.furnace.smelt(pg.K_8)
        g.furnace.smelt(pg.K_9)
        g.furnace.smelt(pg.K_0)
        self.assertTrue(g.playerInven.searchInventory("Iron Ingot")) #1 Iron Ingot in inv

    def test_smeltTwice_sufResourcesForSmeltOnce_inv1IronIngot(self):
        g.new() # initializes player, inventory, smelting etc
        g.playerInven.addItem("Wood", 3)
        g.playerInven.addItem("Iron Ore", 1)
        g.furnace.on_interact()
        g.furnace.smelt(pg.K_6) #should add 1 Iron Ingot to inv
        g.furnace.smelt(pg.K_6) #repeated so this and rest of inputs should do nothing
        g.playerInven.removeItem("Iron Ingot", 1)
        self.assertTrue(not g.playerInven.searchInventory("Iron Ingot")) #should no longer be Iron Ingot in inv

    def test_smeltTwice_sufWoodForSmeltOnce_inv1IronIngot(self):
        g.new() # initializes player, inventory, smelting etc
        g.playerInven.addItem("Wood", 3) #enough wood to smelt once
        g.playerInven.addItem("Iron Ore", 2) #enough iron ore to smelt twice
        g.furnace.on_interact()
        g.furnace.smelt(pg.K_6) #should add 1 Iron Ingot to inv
        g.furnace.smelt(pg.K_6) #repeated so this and rest of inputs should do nothing (no more wood left)
        g.playerInven.removeItem("Iron Ingot", 1)
        self.assertTrue(not g.playerInven.searchInventory("Iron Ingot")) #should no longer be Iron Ingot in inv
    
    def test_smeltTwice_sufIronOreForSmeltOnce_inv1IronIngot(self):
        g.new() # initializes player, inventory, smelting etc
        g.playerInven.addItem("Wood", 6) #enough wood to smelt twice
        g.playerInven.addItem("Iron Ore", 1) #enough iron ore to smelt once
        g.furnace.on_interact()
        g.furnace.smelt(pg.K_6) #should add 1 Iron Ingot to inv
        g.furnace.smelt(pg.K_6) #repeated so this and rest of inputs should do nothing (no more iron ore left)
        g.playerInven.removeItem("Iron Ingot", 1)
        self.assertTrue(not g.playerInven.searchInventory("Iron Ingot")) #should no longer be Iron Ingot in inv
    
    def test_smeltThrice_sufResourcesForSmeltTwice_inv2IronIngot(self):
        #tests to make sure that the correct number of resources (wood and ore) are being removed each time
        #being able to craft twice given exactly the right amount of resources to do this sufficiently proves that the correct number of resources are
        #subtracted each time
        g.new() # initializes player, inventory, smelting etc
        g.playerInven.addItem("Wood", 6) #enough wood to smelt twice
        g.playerInven.addItem("Iron Ore", 2) #enough iron ore to smelt twice
        g.furnace.on_interact()
        g.furnace.smelt(pg.K_6) #should add 1 Iron Ingot to inv
        g.furnace.smelt(pg.K_6) #should add 1 more Iron Ingot to inv
        g.furnace.smelt(pg.K_6) #repeated so this and rest of inputs should do nothing (no more resources left)
        g.playerInven.removeItem("Iron Ingot", 2)
        self.assertTrue(not g.playerInven.searchInventory("Iron Ingot")) #should no longer be Iron Ingot in inv
    

if __name__ == '__main__':
    unittest.main()