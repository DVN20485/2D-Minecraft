import pygame as pg
from configurations import *
from sprites import *
from player import*
from map import*
from Inventory import*
from craftingTable import *
from camera import *
import graphics


#button class
class Button():
	def __init__(self, game, x, y, image):
		self.image = game.sprite_imgs[image]
		self.image = pg.transform.scale(self.image, ((WIDTH/5),(HEIGHT/10)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
  
	def draw(self, surface):
		#draw button on screen

		self.image.set_colorkey(BLACK)  
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return