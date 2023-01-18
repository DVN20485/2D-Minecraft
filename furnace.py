from re import TEMPLATE
from numpy import reciprocal, true_divide
import pygame as pg
import helper
from configurations import *
from Items.Items  import *

class furnace:
    def __init__(self, game): #initialises the crafting table. Currently only takes in coordinates
        self.game = game
        self.smelt_visible = False #ignore for now controller for UI
        self.smeltable_List = smeltableList() #list of item names of things that can be smelted
        self.smRecipe_List = []

    def on_interact(self):
        self.update_smRecipes()
    
    def set_visible(self, vis):
        self.smelt_visible = vis

    def get_visible(self):
        return self.smelt_visible

    def update_smRecipes(self): #finding out what the user can smelt. append them to the smRecipe_list
        self.smRecipe_List = [] #reset the list when called so dont have to check when a user can no longer smelt something
        
        try:
            wood_Owned = self.game.playerInven.invDict['Wood']
            
        except:
            wood_Owned = 0

        if(wood_Owned > 2):#player owns at least 3 wood
            for item in self.smeltable_List: #iterate though all smeltable items
                ore = getRecipe(item)[0][0] #get the ore needed, amount needed will always be 1 per 1 produced
                try:
                    ore_owned = self.game.playerInven.invDict[ore]
                except:
                    break
                if (ore_owned >= 1): #player owns atleast 1 of that ore
                    self.smRecipe_List.append(item) #smeltable item added to the list
        

    def smelt(self, key):
        if key == pg.K_6: #each statement correlates to a key pressed between 6 and 0 for now
            if(len(self.smRecipe_List) >= 1):
                self.give_item(self.smRecipe_List[0])
                self.update_smRecipes()
                return True
            
        if key == pg.K_7:
            if(len(self.smRecipe_List) >= 2):
                self.give_item(self.smRecipe_List[1])
                self.update_smRecipes()
                return True
            
        if key == pg.K_8:
            if(len(self.smRecipe_List) >= 3):
                self.give_item(self.smRecipe_List[2])
                self.update_smRecipes()
                return True
            
        if key == pg.K_9:
            if(len(self.smRecipe_List) >= 4):
                self.give_item(self.smRecipe_List[3])
                self.update_smRecipes()
                return True
            
        if key == pg.K_0:
            if(len(self.smRecipe_List) >= 5):
                self.give_item(self.smRecipe_List[4])
                self.update_smRecipes()
                return True
        return False
    
    def give_item(self, item): #called whe player selects item to smelt
        if item in self.smRecipe_List: #if the item is here we know he has the materials
            ore = getRecipe(item)[0][0]
            self.game.playerInven.removeItem(ore, 1)
            self.game.playerInven.removeItem("Wood", 3)
            self.game.playerInven.addItem(item, 1)
        else:
            print('Insufficient materials')
