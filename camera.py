import pygame as pg
from configurations import *

class Camera:
    def __init__(self):
        self.camera = pg.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT)
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
    
    def apply(self, entity): # apply viewing tranform by shifting entity
        return entity.rect.move(self.camera.topleft)

    def update(self, target): # get updated target (player) coords so target is centered on screen
        x = -target.rect.x + int(WIDTH/2)
        y = -target.rect.y + int(HEIGHT/2)
        self.camera = pg.Rect(x, y, self.width, self.height)