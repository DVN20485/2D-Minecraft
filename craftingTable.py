import pygame as pg
from configurations import *
from Items.Items  import *

class craftingTable:
    def __init__(self,game ,x, y): #initialises the crafting table. Currently only takes in coordinates
        self.game = game
        self.x = x
        self.y = y
        self.recipe_list = []
        self.craft_list =  craftableList()
        self.recipes_visible = False
    
    def on_interact(self): #the method to call from other classes in order to start interacting with the crafting table
        self.update_recipes() #upon interaction, the crafting table figures out what the player can craft with their current self.game
        self.recipes_visible = True

    def set_visible(self, vis):
        self.recipes_visible = vis
    
    def get_visible(self):
        return self.recipes_visible
       

    def update_recipes(self):
        for item in self.craft_list: #checking against the data for all craftable items in the game
            
            recipe = getRecipe(item) #recipe consists of the required materials and amounts
            craftable = True #defaults to assume the player has the required materials
            for r in recipe:
                try:
                    amount_needed = r[1]
                    amount_owned = self.game.playerInven.invDict[r[0]] #looks up how much of a required material the player has

                    if amount_owned < amount_needed:
                        craftable = False
                        break
                            
                except:
                        craftable = False #in case the player doesn't even have the materials
                        break
            try:            
                index = self.recipe_list.index(item) #sees if the item is already in the current list of recipes and gets its index
            except:
                index = -1
            
            if craftable == True and index == -1: #not in current recipe list
                self.recipe_list.append(item)
            if craftable == False and index != -1: #in current recipe list but player is lacking materials, so remove from list
                del self.recipe_list[index]
        
  
    def craft(self, key):
        if key == pg.K_1: #each statement correlates to a key pressed between 1 and 5 for now
            if(len(self.recipe_list) >= 1):
                self.give_item(self.recipe_list[0])
                self.update_recipes()
                return True
        if key == pg.K_2:
            if(len(self.recipe_list) >= 2):
                self.give_item(self.recipe_list[1])
                self.update_recipes()
                return True
        if key == pg.K_3:
            if(len(self.recipe_list) >= 3):
                self.give_item(self.recipe_list[2])
                self.update_recipes()
                return True
        if key == pg.K_4:
            if(len(self.recipe_list) >= 4):
                self.give_item(self.recipe_list[3])
                self.update_recipes()
                return True
        if key == pg.K_5:
            if(len(self.recipe_list) >= 5):
                self.give_item(self.recipe_list[4])
                self.update_recipes()
                return True
        return False
        

    def give_item(self, item): #To be called when the player selects an item to craft. Removes the materials from the player's self.game and adds the crafted item
        
        recipe = getRecipe(item)
        for ingredient in recipe:
            self.game.playerInven.removeItem(ingredient[0], ingredient[1])
        self.game.playerInven.addItem(item, 1)
        
