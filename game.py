import pygame as pg
from UserInterface import User_Interface
from configurations import *
from sprites import *
from player import*
from map import*
from Inventory import *
from craftingTable import *
from camera import *
import graphics
from buttons import *


class Game(): # Main game class that creates all the assets and game window
    def __init__(self, *args, **kwargs): # Initialize game / args and kwargs for overloading 
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.playing = True
        graphics.load_imgs(self)
        self.user_interface = User_Interface(self, self.screen)
        self.seed = kwargs.get('seed', random.randint(0, 99999999)) #if no seed is specified, randomizes

    def new(self): # Create new instance of game
        self.all_sprites = pg.sprite.LayeredUpdates() # Sprite group container for ALL our sprites      
        self.map = Map(self, seed=self.seed) #set seed after loading a save state 
        self.player = Player(self, int(MAP_WIDTH/2), int(MAP_HEIGHT/2),self.user_interface) # Spawn player at center
        self.playerInven = Inventory()
        self.camera = Camera()
    
    def update_map(self):
        self.map = Map(self, seed=self.seed) #set seed after loading a save state 
        
    def menu(self):
        self.user_interface.main_menu(GAMESTATE['Main'])

    def run(self): # Game loop
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.player.events(self) # get player input and perform required actions
            self.update()
            if self.playing:
                self.draw()
        pg.quit()
        
    def update(self): # call updates here
        self.camera.update(self.player) # track player
        self.furnace.update_smRecipes()
        self.craftingTable.update_recipes()

    def draw(self): # Draw to the screen
        self.screen.fill(WHITE) # White background
        graphics.draw_grid(self) # draw grid
        graphics.draw_sprites(self)
        
        graphics.drawEquippedBlock(self)
        graphics.drawEquippedTool(self)
        graphics.drawInventory(self)     #calls the function to draw inventory
        graphics.draw_craft_ui(self)
        graphics.draw_furnace_ui(self)
        graphics.set_title(self)
        pg.display.flip()