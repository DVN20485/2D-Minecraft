import unittest
from game import *
import sprites
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

g = Game() # new game object, initializes pygame
g.new() # initializes player, inventory, crafting etc

class MapClassTest(unittest.TestCase):

    #Test checks that chunks further out of few have not been loaded
    def test_is_bounded_up(self):
        self.assertEqual(g.map.isBounded(0,-90),False)

    def test_is_bounded_down(self):
        self.assertEqual(g.map.isBounded(0,90),False)

    def test_is_bounded_right(self):
        self.assertEqual(g.map.isBounded(90,0),False)
    
    def test_is_bounded_left(self):
        self.assertEqual(g.map.isBounded(-90,0),False)


    #Test checks if index exists in the world coordinates
    def test_get_in_bounds(self):
        self.assertGreater(g.map.get(0,0),-1)
    
    def test_get_out_bounds(self):
        self.assertEqual(g.map.get(90,0),-1)


    #Test checks if sprite exists in the world coordinates
    def test_getSprite_in_bounds(self):
        self.assertNotEqual(g.map.getSprite(0,0),False)
    
    def test_getSprite_in_bounds(self):
        self.assertEqual(g.map.getSprite(-90,0),False)
    

    #Test if map Generates row of chunks of distance 2 chunks away from spawn
    def test_horizontal_triple_grid(self):
        g.map.horizontal_triple_grid(0,-1,-1)
        time.sleep(4)#time for thread to finish adding to grid
        self.assertEqual(g.map.isBounded(0,-50),True)

    def test_vert_triple_grid(self):
        g.map.vert_triple_grid(-1,30,-1)
        time.sleep(4) #time for thread to finish adding to grid
        self.assertEqual(g.map.isBounded(-50,30),True)
