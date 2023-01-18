from math import floor
from os import path
import random
from _thread import *

from configurations import *
from craftingTable import*
from furnace import*
from sprites import *
from collections import defaultdict
import maps.mapGenerator as mpg
import time


game_folder = path.dirname(__file__) # Get current directory
map_folder = path.join(game_folder, "maps") # Map directory

class Map:
    def __init__(self, game, seed):
        self.game = game
        self.seed = seed 
        random.seed(self.seed)  #this is the seed that essentially controls the rest of world generation
        self.ts = [f"{random.randint(0, 99999999): 09}" for j in range(9)]  #array of seeds used in biome generation
        self.map_data = defaultdict(dict) #stores the Map represented by ID's
        self.sprite_map = defaultdict(dict) #stores the Map represented by references to their sprites
        self.load_map() #loads the starting chunk and surrounding 8 chunks N,S,E,W   NW,NE,SW,SE
        # self.load_text_map() #loads the starting chunk using a text file and surrounding 8 chunks as only water N,S,E,W   NW,NE,SW,SE

    def get(self,x,y):
        if self.isBounded(x,y):
            return self.map_data[y][x]
        return -1

    #Return true if given coordinates lie in grid
    def isBounded(self,x,y):
        if y not in self.map_data:
            return False
        elif x not in self.map_data[y]:
            return False
        return True

    #Return true if given coordinates can be walked on (Dirt or Bounded)
    def isWalkable(self,x,y):
        return (self.isBounded(x,y) and self.get(x,y)==1)
    
    #returns the sprite object at coordinate
    def getSprite(self,x,y):
        if self.isBounded(x,y):
            return self.sprite_map[y][x]
        return False
    
    #Given an index on the map and the respected blockID, the sprite at the coord will be replaced by the new block
    def createBlock(self,x,y,blockID):# pragma: no cover
        if self.isBounded(x,y):
            block = self.game.map.getSprite(x,y)
            if type(block) is not int :
                block.kill()
                klass = globals()[SPRITENAME[blockID]]
                self.game.map.sprite_map[y][x] = klass(self.game, x, y)
                self.map_data[y][x] = blockID

    #Given an index on the map, the sprite will be removed and replaced with dirt, map class also updated on the backend
    def breakBlock(self,x,y):# pragma: no cover
        if self.isBounded(x,y):
            block = self.game.map.getSprite(x,y)
            if type(block)is not int:
                block.kill()
                self.game.map.sprite_map[y][x] = Dirt(self.game, x, y)
                self.map_data[y][x] = MAPID["Dirt"]

    #when given a chunk direction returns the coordinate of the origin of target chunk in the world space 
    #directionX and directionY tells the function how many chunks vertically and horizontally to move to get the origin
    def get_offsets(self,curr_x,curr_y,directionX,directionY):
        chunk_coord_x = floor(curr_x/30)
        chunk_coord_y = floor(curr_y/30)
        target_chunk_x = chunk_coord_x +directionX
        target_chunk_y = chunk_coord_y +directionY
        offset_x = target_chunk_x*MAP_WIDTH
        offset_y = target_chunk_y*MAP_HEIGHT
        return offset_x,offset_y
    
    #Join grid given by text file name onto a 30x30 chunk space defined by directionX and directionY
    def concat_grid(self,curr_x,curr_y,directionX,directionY):
        offset_x ,offset_y = self.get_offsets(curr_x,curr_y,directionX,directionY)
        mapfile = mpg.main(offset_x, offset_y, self.ts)
        temp_list = mapfile.splitlines()
        
        
        # with open(path.join(map_folder, MAP), 'rt') as file: # open and read map file
        # for line in file: # Add every line in file to temp_list
        #     temp_list.append(line)
        
        for row, tiles in enumerate(temp_list): # loop through every row of tiles
            temp_row = tiles.split(",")
            for col, tile in enumerate(temp_row): # loop through every tile in row
                offset_col = col+offset_x
                offset_row = row+offset_y
                sprite_tile = None
                tile = int(tile)
                # if(tile == MAPID["Wall"]): # boundary
                #     pass
                if(tile == MAPID["Dirt"] or tile == MAPID["Player"]): # dirt or player
                    sprite_tile = Dirt(self.game, offset_col, offset_row)
                elif(tile == MAPID["Tree"]): # tree
                    sprite_tile = Tree(self.game, offset_col, offset_row)
                elif(tile == MAPID["Stone"]): # stone
                    sprite_tile = Stone(self.game, offset_col, offset_row)
                elif(tile == MAPID["Water"]): # stone
                    sprite_tile = Water(self.game, offset_col, offset_row)
                elif(tile == MAPID["Iron"]): # stone
                    sprite_tile = IronOre(self.game, offset_col, offset_row)
                elif(tile == MAPID["CraftingTable"]): # workbench
                    sprite_tile = CraftingTable(self.game, offset_col, offset_row)
                    if not hasattr(self.game, 'craftingTable'): # allows initialization of one crafting table that can be used elsewhere on map
                        self.game.craftingTable = craftingTable(self.game, offset_col,offset_row)
                        self.game.furnace = furnace(self.game)
                
                self.map_data[offset_row][offset_col] = tile
                
                # If map data has no existing sprite yet
                # if sprite_tile == None:
                #     continue

                # print("x:",offset_col,"y:",offset_row) debugging
                self.sprite_map[offset_row][offset_col] = sprite_tile #store addresses of each sprite object incase we want to index them later
    
    #loads the starting chunk and surrounding 8 chunks N,S,E,W   NW,NE,SW,SE can take in map file 
    def load_map(self):
        for x in range(-1,2):
            for y in range(-1,2):
                self.concat_grid(15,15,x,y)

    def vert_triple_grid(self,player_x,player_y,direction):
        for i in range(-1,2):
            offset_x,offset_y =self.get_offsets(player_x,player_y,direction,i)
            if not self.isBounded(offset_x,offset_y):
                start_new_thread(self.concat_grid,(player_x,player_y,direction,i))
            
    
    def horizontal_triple_grid(self,player_x,player_y,direction):
        for i in range(-1,2):
            offset_x,offset_y =self.get_offsets(player_x,player_y,i,direction)
            if not self.isBounded(offset_x,offset_y):
                start_new_thread(self.concat_grid,(player_x,player_y,i,direction))

   
    #Code to generate water chunks around a predefined text file chunk
    def concat_water_chunk(self,curr_x,curr_y,directionX,directionY): # pragma: no cover
        offset_x ,offset_y = self.get_offsets(curr_x,curr_y,directionX,directionY)
        temp_list = [[MAPID["Water"]]*30]*30
        
        for row, tiles in enumerate(temp_list): # loop through every row of tiles
            for col, tile in enumerate(tiles): # loop through every tile in row
                offset_col = col+offset_x
                offset_row = row+offset_y
                sprite_tile = None
                tile = int(tile)
                
                if(tile == MAPID["Water"]): # water
                    sprite_tile = Water(self.game, offset_col, offset_row)
                
                self.map_data[offset_row][offset_col] = tile
                
                # If map data has no existing sprite yet
                # if sprite_tile == None:
                #     continue

                # print("x:",offset_col,"y:",offset_row) debugging
                self.sprite_map[offset_row][offset_col] = sprite_tile #store addresses of each sprite object incase we want to index them later


    #Add a chunk defined by a text file ("File name in configutations.py") [File must contain location of crafting table ID 9]
    def concat_file_chunk(self,curr_x,curr_y,directionX,directionY,): # pragma: no cover
        offset_x ,offset_y = self.get_offsets(curr_x,curr_y,directionX,directionY)
        
        temp_list = []
        
        with open(path.join(map_folder, MAP), 'rt') as file: # open and read map file
            for line in file: # Add every line in file to temp_list
                temp_list.append(line)
        
        for row, tiles in enumerate(temp_list): # loop through every row of tiles
            temp_row = tiles.split(",")
            for col, tile in enumerate(temp_row): # loop through every tile in row
                offset_col = col+offset_x
                offset_row = row+offset_y
                sprite_tile = None
                tile = int(tile)
                # if(tile == MAPID["Wall"]): # boundary
                #     pass
                if(tile == MAPID["Dirt"] or tile == MAPID["Player"]): # dirt or player
                    sprite_tile = Dirt(self.game, offset_col, offset_row)
                elif(tile == MAPID["Tree"]): # tree
                    sprite_tile = Tree(self.game, offset_col, offset_row)
                elif(tile == MAPID["Stone"]): # stone
                    sprite_tile = Stone(self.game, offset_col, offset_row)
                elif(tile == MAPID["Water"]): # stone
                    sprite_tile = Water(self.game, offset_col, offset_row)
                elif(tile == MAPID["Iron"]): # stone
                    sprite_tile = IronOre(self.game, offset_col, offset_row)
                elif(tile == MAPID["CraftingTable"]): # workbench
                    sprite_tile = CraftingTable(self.game, offset_col, offset_row)
                    if not hasattr(self.game, 'craftingTable'): # allows initialization of one crafting table that can be used elsewhere on map
                        self.game.craftingTable = craftingTable(self.game, offset_col,offset_row)
                        self.game.furnace = furnace(self.game)
                
                self.map_data[offset_row][offset_col] = tile
                
                # If map data has no existing sprite yet
                # if sprite_tile == None:
                #     continue
                self.sprite_map[offset_row][offset_col] = sprite_tile #store addresses of each sprite object incase we want to index them later
    
    def load_text_map(self): # pragma: no cover
        for x in range(-1,2):
            for y in range(-1,2):
                if(x==0 and y==0):
                    self.concat_file_chunk(15,15,x,y)
                else:
                    self.concat_water_chunk(15,15,x,y)



    #returns dictionary for external processing
    def get_grid(self):# pragma: no cover
        return self.map_data
