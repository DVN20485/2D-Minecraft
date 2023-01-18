import pygame as pg
from configurations import *
import helper
from UserInterface import *

def load_imgs(game):
    game.sprite_imgs = {
        # sprites
        "tree": pg.image.load(helper.get_texture_path(TREE)).convert(),
        "stone": pg.image.load(helper.get_texture_path(STONE)).convert(),
        "dirt": pg.image.load(helper.get_texture_path(DIRT)).convert(),
        "water": pg.image.load(helper.get_texture_path(WATER)).convert(),
        "ironore": pg.image.load(helper.get_texture_path(IRON_ORE)).convert(),
        "craft": pg.image.load(helper.get_texture_path(CRAFT)).convert(),
        "woodpick": pg.image.load(helper.get_texture_path(WOOD_PICK)).convert(),
        "stonepick": pg.image.load(helper.get_texture_path(STONE_PICK)).convert(),
        # player sprites
        "up": pg.image.load(helper.get_texture_path(UP)).convert(),
        "down": pg.image.load(helper.get_texture_path(DOWN)).convert(),
        "left": pg.image.load(helper.get_texture_path(LEFT)).convert(),
        "right": pg.image.load(helper.get_texture_path(RIGHT)).convert(),
        # sprites for buttons and UI related :)
        "start_button": pg.image.load(helper.get_texture_path(START_BTN)).convert(),
        "load_button": pg.image.load(helper.get_texture_path(LOAD_BTN)).convert(),
        "credits_button": pg.image.load(helper.get_texture_path(CREDITS_BTN)).convert(),
        "exit_button": pg.image.load(helper.get_texture_path(EXIT_BTN)).convert(),
        "back_button": pg.image.load(helper.get_texture_path(BACK_BTN)).convert(),
        "save_button": pg.image.load(helper.get_texture_path(SAVE_BTN)).convert(),
        "help_button": pg.image.load(helper.get_texture_path(HELP_BTN)).convert(),
      
        # interface
        "options_menu":  pg.image.load(helper.get_texture_path(OPTIONS_MENU)),
        "help_bg":  pg.image.load(helper.get_texture_path(HELP)),
        "help_info": pg.image.load(helper.get_texture_path(HELP_INFO)),
        "credits_info": pg.image.load(helper.get_texture_path(CREDITS_INFO)),
        
        "menu": pg.image.load(helper.get_texture_path(MENU)),
        "tile": pg.image.load(helper.get_texture_path(TILE_IMG)),
        "hand": pg.image.load(helper.get_texture_path(HAND)),
        "woodI": pg.image.load(helper.get_texture_path(WOODI)),
        "stoneI": pg.image.load(helper.get_texture_path(STONEI)),
        "bucket": pg.image.load(helper.get_texture_path(BUCKET)),
        "BoWI": pg.image.load(helper.get_texture_path(BUCKETWATERI)),
        "ironpick": pg.image.load(helper.get_texture_path(IPICK)),
        "stonepick": pg.image.load(helper.get_texture_path(SPICK)),
        "woodpick": pg.image.load(helper.get_texture_path(WPICK)),
    }

def draw_sprites(game):
    startx, starty = -int(MAP_WIDTH/2) + game.player.x, game.player.y - int(MAP_HEIGHT/2)
    endx, endy = int(MAP_WIDTH/2) + game.player.x, game.player.y + int(MAP_HEIGHT/2)

    for x in range(startx, endx):
        for y in range(starty, endy):
            if y in game.map.sprite_map and x in game.map.sprite_map[y]:
                sprite = game.map.sprite_map[y][x]
                game.screen.blit(sprite.image, game.camera.apply(sprite))
    
    game.screen.blit(game.player.image, game.camera.apply(game.player))


def draw_grid(game): # Function to draw grid onto screen by drawing lines
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(game.screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(game.screen, BLACK, (0, y), (WIDTH, y))
        

def drawInventory(game):    #shows/hides the inventory visual interface
    if game.playerInven.visible: # if true should draw the inventory
        
        #display inventory tag and image
        font = pg.font.SysFont('comicsans', 17, True)
        menu = game.sprite_imgs["menu"]
        tX = WIDTH - 130
        tY = HEIGHT - 400
        game.screen.blit(menu, (tX,tY))
        title = 'Inventory'
        title = font.render(title , 1, (0,0,0))
        game.screen.blit(title, (tX+10,tY+5))
        ycord = tY+10

        #display materials
        font = pg.font.SysFont('comicsans', 11)
        for key in game.playerInven.invDict:
            ycord += 25 

            itemName = str(key + ':')
            itemName = font.render(itemName, 1,  (0,0,0))
            game.screen.blit(itemName, (tX+10, ycord))

            itemQuant = str(game.playerInven.invDict[key])
            itemQuant = font.render(itemQuant, 1,  (0,0,0))
            game.screen.blit(itemQuant, (tX+90, ycord))

def drawEquippedBlock(game):

    tile = game.sprite_imgs["menu"]
    tX = WIDTH - 48
    tY = HEIGHT - 48
    tile = pg.transform.scale(tile, (48,48))
    game.screen.blit(tile, (tX, tY))
    
   

    Block = ''
    
    if(game.playerInven.block == 'Wood'):
        
        Block = game.sprite_imgs["woodI"]

    if(game.playerInven.block == 'Stone'):
        
        Block = game.sprite_imgs["stoneI"]

    if(game.playerInven.block == 'Bucket of Water'):
        
        Block = game.sprite_imgs["BoWI"]
    
    if(game.playerInven.block == 'Crafting Table'):
        
        Block = game.sprite_imgs["craft"]
 
    if(Block != ''):
        Block = pg.transform.scale(Block, (40,40))
        game.screen.blit(Block, (tX+5, tY+5))

def drawEquippedTool(game):

    tile = game.sprite_imgs["menu"]
    tX = WIDTH - 96
    tY = HEIGHT - 48
    tile = pg.transform.scale(tile, (48,48))
    game.screen.blit(tile, (tX, tY))
    
    Tool = ''
    
    if(game.playerInven.tool == 'Wood pickaxe'):
        
        Tool = game.sprite_imgs["woodpick"]

    elif(game.playerInven.tool == 'Stone pickaxe'):
        
        Tool = game.sprite_imgs["stonepick"]

    elif(game.playerInven.tool == 'Iron pickaxe'):
        
        Tool = game.sprite_imgs["ironpick"]

    elif(game.playerInven.tool == 'Bucket'):
        
        Tool = game.sprite_imgs["bucket"]
 
    if(Tool != ''):
        Tool = pg.transform.scale(Tool, (40,40))
        game.screen.blit(Tool, (tX+5, tY+5))

def draw_craft_ui(game):
    
    if game.craftingTable.recipes_visible: # if true should draw the crafting ui
            #print("interacted. Display:"+ str(recipes_visible))
            #display "recipes" tag and window
            font = pg.font.SysFont('comicsans', 17, True)
            menu = game.sprite_imgs["menu"]
            game.screen.blit(menu, (10,300))
            title = 'Recipes'
            title = font.render(title , 1, (0,0,0))
            game.screen.blit(title, (20,305))
            ycord = 305

            #display materials
            font = pg.font.SysFont('comicsans', 11)
            item_counter = 1
            #page_counter = 0
            for item in game.craftingTable.recipe_list:
                ycord += 25 
                if(item_counter > 5):
                    break
                itemName = str(str(item_counter) + " - " + item)
                itemName = font.render(itemName, 1,  (0,0,0))
                game.screen.blit(itemName, (20, ycord))
                item_counter += 1
                
                #itemQuant = str(playerInven.invDict[key])
                #itemQuant = font.render(itemQuant, 1,  (0,0,0))
                #self.game.screen.blit(itemQuant, (450, ycord))

def draw_furnace_ui(game):
        if game.furnace.smelt_visible: # if true should draw the self.game
                #print("interacted. Display:"+ str(recipes_visible))
                #display self.game tag and image
                font = pg.font.SysFont('comicsans', 17, True)
                menu = game.sprite_imgs["menu"]
                game.screen.blit(menu, (10,0))
                title = 'Furnace'
                title = font.render(title , 1, (0,0,0))
                game.screen.blit(title, (20,5))
                ycord = 5

                #display materials
                font = pg.font.SysFont('comicsans', 11)
                item_counter = 6 #temporary fix to display current smelt key (9)
                for item in game.furnace.smRecipe_List:
                    ycord += 25 
                    if(item_counter>10):
                        break
                    itemName = str(str(item_counter) + " - " + item)
                    itemName = font.render(itemName, 1,  (0,0,0))
                    game.screen.blit(itemName, (20, ycord))
                    item_counter += 1
                    

def set_title(game):
    pg.display.set_caption("POS("+str(game.player.x)+","+str(game.player.y)+")   FPS:"+ str(int(game.clock.get_fps()))) # display player position as title