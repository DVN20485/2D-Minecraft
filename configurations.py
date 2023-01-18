# Game configurations
WIDTH = 768
HEIGHT = 768
TITLE = "2D MineCraft"
FPS = 10 # FPS cap

TILESIZE = 64
GRIDWIDTH = WIDTH/TILESIZE # = 30
GRIDHEIGHT = HEIGHT/TILESIZE # = 30

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (59, 66, 82)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0,0, 255)
BROWN = (157, 110, 69)
RED = (255, 0, 0)
DIRTGREEN = (157, 225, 69)


# # Legend Deprecated
ID = {  "PLAYER": RED,
        "WALL": GREEN,
        "TREE": BROWN,
        "STONE": GREY,
        "WATER": BLUE,
        "DIRT" : DIRTGREEN,
        "CRAFT" : YELLOW
}

# Sprite images
UP = "up.png"
DOWN = "down.png"
LEFT = "left.png"
RIGHT = "right.png"
DIRT = "grass.png"
STONE = "stone.png"
TREE = "tree.png"
WATER = "water.png"
IRON_ORE = "ironore.png"
WOOD_PICK = "wood_pick.png"
STONE_PICK = "stone_pick.png"
MENU = "menu.png"
CRAFT = "craft.png"

#equipped item sprites
TILE_IMG = "pickTile.png"
HAND = "hand.png"
WOODI = "WoodInv.png"
STONEI = "StoneInv.png"
BUCKET = "Bucket.png"
BUCKETWATERI = "BoWInv.png"
WPICK = "woodPick.png"
SPICK = "stonePick.png"
IPICK = "ironPick.png"

HELP = "help_bg.png"
# UI images
CREDITS_INFO = "credits_info.png"
HELP_INFO = "help_info.png"
OPTIONS_MENU = "optionsmenu.png"
# button images
START_BTN = "start.png"
LOAD_BTN = "load.png"
CREDITS_BTN ="credit.png"
EXIT_BTN = "exit.png"
SAVE_BTN= "save.png"
HELP_BTN = "help.png"

BACK_BTN = "back.png"

GAMESTATE ={
    "Main":0,
    "Game":1,
    "Load_menu":2,
    "Credits":3,   
    "IG_Options": 4,
    "Help":5
}

MAPID = {
    "Wall":-1,
    "Player":0,
    "Dirt":1,
    "Tree":2,
    "Stone":3,
    "Iron":4,
    #insert more here (remember to add corresponding value key pair in SPRITENAME)
    "CraftingTable":9,
    "Water":10
}

SPRITENAME = {
    -1:"Wall",
    0 :"Player",
    1:"Dirt",
    2:"Tree",
    3:"Stone",
    4:"Iron",
    #insert more here
    9:"CraftingTable",
    10:"Water"
}

ITEMSOURCE={
    "Wood": "Tree",
    "Stone": "Stone",
    "Iron Ore" : "Iron",
    "Crafting Table":"CraftingTable"
}


# Map
MAP = "map.txt"
MAP_WIDTH = 30
MAP_HEIGHT = 30



