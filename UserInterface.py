import pygame as pg
from configurations import *
from sprites import *
from player import*
from graphics import *
from saveState.saveState import *

from buttons import *


class User_Interface:
	def __init__(self, game, screen):  # parameters for help page class
		self.game = game
		self.screen = screen
		self.start_btn = Button(self.game,(WIDTH/10), (HEIGHT*3)/4, "start_button") 
		self.load_btn = Button(self.game,(WIDTH/10)+200, (HEIGHT*3)/4, "load_button")
		self.credits_btn = Button(self.game,(WIDTH/10)+400, (HEIGHT*3)/4, "credits_button")
		self.exit_btn = Button(self.game,(WIDTH/10)+600, (HEIGHT*3)/4, "exit_button")
		self.back_btn = Button(self.game,(50), (HEIGHT)-70, "back_button")
  
		# create sprite button groups for the in game GUI
		self.save_btn = Button(self.game,(WIDTH*3)/7, (HEIGHT/6)+100, "save_button")
		self.help_btn = Button(self.game,(WIDTH*3)/7 , (HEIGHT/6)+300, "help_button")
		self.ig_load_btn = Button(self.game,(WIDTH*3)/7 , (HEIGHT/6)+200, "load_button")
		self.ig_exit_btn =  Button(self.game,(WIDTH*3)/7 , (HEIGHT/6)+400, "exit_button")
  

	def main_menu(self,next_loop):
		while next_loop == 0:
			self.screen.fill((39, 51, 39))
			#create buttons using Button class
			# get position of mouse
			pos = pg.mouse.get_pos()
			self.start_btn.draw(self.screen)
			self.load_btn.draw(self.screen)
			self.credits_btn.draw(self.screen)
			self.exit_btn.draw(self.screen)
			# check if button is being clicked with left click
			for event in pg.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					if  self.start_btn.rect.collidepoint(pos):
						if pg.mouse.get_pressed()[0] == 1:
							next_loop = GAMESTATE["Game"]
							self.game.run()
					if  self.load_btn.rect.collidepoint(pos):
						if pg.mouse.get_pressed()[0] == 1:
							load_State(self.game.player)
							next_loop = GAMESTATE["Game"]
							self.game.run()
					if  self.credits_btn.rect.collidepoint(pos):
						if pg.mouse.get_pressed()[0] == 1:
							next_loop = GAMESTATE["Credits"]
							self.credits_screen(GAMESTATE["Credits"])

					if  self.exit_btn.rect.collidepoint(pos):
						if pg.mouse.get_pressed()[0] == 1:
							self.playing = False
							self.running = False
							pg.quit()

				if event.type == pg.QUIT:
					self.playing = False
					self.running = False
					pg.quit()
				if event.type == pg.KEYUP:
					if event.key == pg.K_ESCAPE:
						self.game.playing = False
						
			pg.display.update()

#unused but keeping in case we have multiple save files in future
	def load_game_screen(self, next_loop):
		while next_loop == 2:
			self.screen.fill((39, 51, 39))
			pos = pg.mouse.get_pos()
			self.back_btn.draw(self.screen)
			for event in pg.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					if  self.back_btn.rect.collidepoint(pos):
						if pg.mouse.get_pressed()[0] == 1:
							next_loop = GAMESTATE["Main"]
							self.main_menu(GAMESTATE["Main"])
				if event.type == pg.QUIT:
					self.game.playing = False
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						next_loop = GAMESTATE["Main"]
						self.main_menu(GAMESTATE["Main"])
						
			pg.display.update()
   
	def credits_screen(self, next_loop):
		while next_loop == 3:
			self.screen.fill((39, 51, 39))
			text = self.game.sprite_imgs["credits_info"]
			self.game.screen.blit(text, (WIDTH/3,HEIGHT/4))
			pos = pg.mouse.get_pos()
			self.back_btn.draw(self.screen)
			for event in pg.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					if  self.back_btn.rect.collidepoint(pos):
						if pg.mouse.get_pressed()[0] == 1:
							next_loop = GAMESTATE["Main"]
							self.main_menu(GAMESTATE["Main"])
				if event.type == pg.QUIT:
					print("quit")
					self.playing = False
					self.running = False
					pg.quit()
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						next_loop = GAMESTATE["Main"]
						self.main_menu(GAMESTATE["Main"])
						
			pg.display.update()
	
	def Options(self, next_loop): # in game options menu 
		while next_loop == 4:
			menu = self.game.sprite_imgs["options_menu"]
			menu = pg.transform.scale(menu, ((WIDTH*3)/7,(HEIGHT*4)/6))
			self.game.screen.blit(menu, (WIDTH/4+60,HEIGHT/8))
			pos = pg.mouse.get_pos()					

			self.help_btn.draw(self.screen)
			self.save_btn.draw(self.screen)
			self.ig_load_btn.draw(self.screen)
			self.ig_exit_btn.draw(self.screen)
		
	
			for event in pg.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					if  self.help_btn.rect.collidepoint(pos):
						if pg.mouse.get_pressed()[0] == 1:
							next_loop = GAMESTATE["Help"]
							self.help_page(GAMESTATE["Help"])
					# save and load buttons
					if self.save_btn.rect.collidepoint(pos):
						if pg.mouse.get_pressed()[0] == 1:
							print('saved!')
							save_State(self.game, self.game.playerInven.invDict)
							next_loop = GAMESTATE["Game"]

					if self.ig_load_btn.rect.collidepoint(pos):
						if pg.mouse.get_pressed()[0] == 1:
							print('loaded')
							load_State(self.game.player)	
							next_loop = GAMESTATE["Game"]

					if  self.ig_exit_btn.rect.collidepoint(pos):
						if pg.mouse.get_pressed()[0] == 1:
							next_loop = GAMESTATE["Main"]
							self.main_menu("Main")
							self.game.playing = False
       
				if event.type == pg.QUIT:
					self.game.playing = False
					self.game.running = False
					pg.quit()
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						next_loop = GAMESTATE["Game"]
			pg.display.update()
	
	def help_page(self, next_loop):
		while next_loop == 5:
			help = self.game.sprite_imgs["help_bg"]
			help = pg.transform.scale(help, ((WIDTH*3)/7,(HEIGHT*4)/6))
			self.game.screen.blit(help, (WIDTH/4+60,HEIGHT/8))
			text = self.game.sprite_imgs["help_info"]
			self.game.screen.blit(text, (WIDTH/3+30,HEIGHT/4))
			pos = pg.mouse.get_pos()					
			self.help_back = Button(self.game,(WIDTH/3) +50, (HEIGHT*1.9)/3, "back_button")

   
			self.help_back.draw(self.screen)
			for event in pg.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					if  self.help_back.rect.collidepoint(pos):
						if pg.mouse.get_pressed()[0] == 1:
							next_loop= GAMESTATE["IG_Options"]
							self.Options(GAMESTATE["IG_Options"])
   
	
				if event.type == pg.QUIT:
					self.game.playing = False
					self.game.running = False
					pg.quit()
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						next_loop= GAMESTATE["Game"]
			pg.display.update()
	 