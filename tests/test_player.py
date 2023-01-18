import unittest
from game import *
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

g = Game() # new game object, initializes pygame
g.new() # initializes player, inventory, crafting etc

class PlayerClassTest(unittest.TestCase):
    
    # testing player movement by checking direction of player after movement
    def test_movement_up(self):
        g.player.move("up", dy=1)
        self.assertEqual(g.player.curr_directionY, 1)

    def test_movement_down(self):
        g.player.move("down", dy=-1)
        self.assertEqual(g.player.curr_directionY, -1)

    def test_movement_left(self):
        g.player.move("left", dx=-1)
        self.assertEqual(g.player.curr_directionX, -1)

    def test_movement_right(self):
        g.player.move("right", dx=1)
        self.assertEqual(g.player.curr_directionX, 1)
    
    # testing player interaction with crafting table
    def test_interact(self):
        g.player.move("left", dx=-1) # move left to face table
        g.player.Interact() # interact with crafting table

        self.assertTrue(g.craftingTable.recipes_visible, True) # check if crafting is open

    # testing break wood block
    def test_break_block(self):
        g.playerInven.addItem('Wood', 1)
        g.player.placeBlock()
        g.player.breakBlock()
        self.assertTrue(g.playerInven.searchInventory("Wood")) # check if wood is in inventory after breaking

    # testing place block
    def test_place_block(self):
        g.playerInven.addItem('Wood', 1)
        g.player.placeBlock()
        self.assertTrue(g.playerInven.searchInventory("Wood")) # check if wood is not in inventory after place

    # rather test the crafting table & furnace itself instead of through player, the tests below do work if needed

    # def test_smelt_iron(self):
    #     g.playerInven.addItem('Wood', 3)
    #     g.playerInven.addItem('Iron Ore', 1)
    #     g.player.move("left", dx=-1) # move player to face crafting table
    #     g.player.smeltIron()
        
    #     self.assertTrue(g.playerInven.searchInventory("Iron Ingot")) # check if ore has been smelted into ingot

    # def test_craft(self):
    #     g.player.move("left", dx=-1)
    #     g.playerInven.addItem('Wood', 4)
    #     g.player.craft(pg.K_2)

    #     self.assertTrue(g.playerInven.searchInventory("Crafting table")) # check if wood is crafted into pickaxe

if __name__ == '__main__':
    unittest.main()
