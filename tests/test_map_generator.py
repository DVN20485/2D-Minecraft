import unittest
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
import random
import maps.mapGenerator as mpg
import numpy as np

class MapGeneratorClassTest(unittest.TestCase):
    random.seed(1234)  #this is the seed that essentially controls the rest of world generation
    ts = [f"{random.randint(0, 99999999): 09}" for j in range(9)]  #array of seeds used in biome generation
    test_map = mpg.generateMap([0,0], ts).split('\n')
    test_map1 = np.empty((30,30), dtype=np.int8)
    for i in range(30):
        test_map1[i] = test_map[i].split(',')  #getting map.txt into a 2d numpy array

    def test_dirt_count_spawn(self): #checks number of dirt in test seed
        self.assertEqual(np.sum(self.test_map1 == 1), 749, "There should be 749 dirt in spawn chunk") 

    def test_tree_count_spawn(self):  #checks number of trees in test seed
        self.assertEqual(np.sum(self.test_map1 == 2), 87, "There should be 87 trees in spawn chunk") 

    def test_stone_count_spawn(self): #checks number of stone in test seed
        self.assertEqual(np.sum(self.test_map1 == 3), 23, "There should be 23 stone in spawn chunk")

    def test_iron_count_spawn(self): #checks number of iron in test seed
        self.assertEqual(np.sum(self.test_map1 == 4), 9, "There should be 9 iron in spawn chunk") 

    def test_crafting_table_count_spawn(self): #checks number of crafting table in test seed
        self.assertEqual(np.sum(self.test_map1 == 9), 1, "There should be only 1 crafting table in spawn chunk")
    
    def test_water_count_spawn(self): #checks number of water in test seed
        self.assertEqual(np.sum(self.test_map1 == 10), 31, "There should be 31 water in spawn chunk") 

if __name__ == '__main__':
    unittest.main()