from math import floor
import pygame as pg
import furnace as fn
from saveState.saveState import *
from configurations import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y,UI): # Parameters are game object, x & y grid coordinates
        self.groups = game.all_sprites # Create copy of sprite groups from game object
        pg.sprite.Sprite.__init__(self, self.groups) # Add player object to sprite groups
        self.game = game # Create copy of game object
        self.map = self.game.map
        self.UI = UI
        self.x = x
        self.y = y

        self.curr_directionX = 0
        self.curr_directionY = 1

        self.image = game.sprite_imgs["down"]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


    def move(self, img_dir, dx=0, dy=0):
        # Use correct image and set correct direction
        self.image = self.game.sprite_imgs[img_dir]
        self.image.set_colorkey(BLACK)
        self.curr_directionX = dx
        self.curr_directionY = dy

        old_x = self.x
        old_y = self.y
        curr_chunk_x = floor(old_x/30)
        curr_chunk_y = floor(old_y/30)
        # If the desired block is walkable then traverse to it
        if(self.map.isWalkable(self.x+dx,self.y+dy)):
            self.x += dx
            self.y += dy
        
        # debugging code to ignore collision
        # self.x += dx
        # self.y += dy

        if(curr_chunk_x != floor(self.x/30) or curr_chunk_y!=floor(self.y/30)): #if the player moves into a different chunk
            direction_x = self.x - old_x
            direction_y = self.y - old_y
            if direction_x != 0:                                                #if the player moves into a new chunk horizontally
                self.map.vert_triple_grid(self.x,self.y,direction_x)            #tell map to render unloaded chunks
            elif direction_y != 0:
                self.map.horizontal_triple_grid(self.x,self.y,direction_y)      #tell map to render unloaded chunks
                
        #     print("new chunk") #debugging code to show when a player enters a new chunk
        # else:
        #     print("same chunk")

        # object coords to screen coords
        self.rect.x, self.rect.y = self.x * TILESIZE, self.y * TILESIZE

        # close inventory display
        self.game.craftingTable.set_visible(False)
        self.game.furnace.set_visible(False)


    def events(self, game): # pragma: no cover
        for event in pg.event.get(): # Loop through every event
            if event.type == pg.QUIT: # If the player presses the x, stop running the game
                    game.playing = False
            if event.type == pg.KEYDOWN: # key press listener, only accepts 1 key press
                if event.key == pg.K_ESCAPE:
                    self.UI.Options(GAMESTATE["IG_Options"])
                if event.key == pg.K_f:
                    self.breakBlock()
                if event.key == pg.K_i:
                    game.playerInven.visible = not game.playerInven.visible
                if event.key == pg.K_e:
                    self.Interact()
                if event.key == pg.K_1:
                    self.craft(pg.K_1)
                if event.key == pg.K_2:
                    self.craft(pg.K_2)
                if event.key == pg.K_3:
                    self.craft(pg.K_3)
                if event.key == pg.K_4:
                    self.craft(pg.K_4)
                if event.key == pg.K_5:
                    self.craft(pg.K_5)
                if event.key == pg.K_6:
                    self.smelt(pg.K_6)
                if event.key == pg.K_7:
                    self.smelt(pg.K_7)
                if event.key == pg.K_8:
                    self.smelt(pg.K_8)
                if event.key == pg.K_9:
                    self.smelt(pg.K_9)
                if event.key == pg.K_0:
                    self.smelt(pg.K_0)
                if event.key == pg.K_t:
                    self.game.playerInven.equipTool()
                if event.key == pg.K_b:
                    self.game.playerInven.equipBlock()


        if game.playing == False:
            return

        keys = pg.key.get_pressed() # key press listener, accepts key down (holding down key)
        if keys[pg.K_a]:
            self.move("left", dx=-1)
        elif keys[pg.K_d]:
            self.move("right", dx=1)
        elif keys[pg.K_w]:
            self.move("up", dy=-1)
        elif keys[pg.K_s]:
            self.move("down", dy=1)

    def Interact(self):
        blockX =self.x + self.curr_directionX
        blockY =  self.y + self.curr_directionY
        blockInFront = self.map.get(blockX, blockY)
        if(blockInFront == MAPID["CraftingTable"]):
            self.game.craftingTable.on_interact()
            self.game.furnace.on_interact()
            self.game.furnace.smelt_visible = True
        elif(blockInFront==MAPID["Dirt"]): #place block if facing a dirt block
            self.placeBlock()
   
    def craft(self, key): # pragma: no cover
        blockX =self.x + self.curr_directionX
        blockY =  self.y + self.curr_directionY
        blockInFront = self.map.get(blockX, blockY)
        if(blockInFront == MAPID["CraftingTable"] and self.game.craftingTable.get_visible() == True):
            self.game.craftingTable.craft(key)

    def smelt(self, key): # pragma: no cover
        blockX =self.x + self.curr_directionX
        blockY =  self.y + self.curr_directionY
        blockInFront = self.map.get(blockX, blockY)
        if(blockInFront == MAPID["CraftingTable"] and self.game.furnace.get_visible() == True):
            self.game.furnace.smelt(key)
            
    def breakBlock(self): # pragma: no cover
        blockX =self.x + self.curr_directionX
        blockY =  self.y + self.curr_directionY
        blockInFront = self.map.get(blockX, blockY)
        # print("BLOCK IN FRONT:",blockInFront)
        if(blockInFront == MAPID["Tree"]):
            self.map.breakBlock(blockX,blockY)
            self.game.playerInven.addItem('Wood', 1)
        elif(blockInFront == MAPID["Stone"]):
            if self.game.playerInven.searchInventory("Wood pickaxe"):

                self.map.breakBlock(blockX, blockY)
                self.game.playerInven.addItem('Stone',1)
            else:
                print("get a wood pickaxe")
        elif(blockInFront == MAPID["Iron"]):
            if "pickaxe" in self.game.playerInven.tool and "Wood" not in self.game.playerInven.tool:
                self.map.breakBlock(blockX, blockY)
                self.game.playerInven.addItem('Iron Ore',1)
            else:
                print("get a stone pickaxe")
                
        # debugging
       # print("block x  " + str(blockX) + "  block y  " + str(blockY))

    #Place block in block infront of player (defaults to wood for now)
    def placeBlock(self):
        blockX =self.x + self.curr_directionX
        blockY =  self.y + self.curr_directionY
        blockInFront = self.map.get(blockX, blockY)

        inventory = self.game.playerInven
        selectedBlock = inventory.block
        if(selectedBlock!=''):
            spriteID  = MAPID[ITEMSOURCE[selectedBlock]]
            if(blockInFront ==MAPID["Dirt"]):
                if self.game.playerInven.searchInventory(selectedBlock):
                    self.map.createBlock(blockX, blockY,spriteID)
                    self.game.playerInven.removeItem(selectedBlock,1)
