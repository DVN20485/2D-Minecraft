from os import path
from configurations import *

game_folder = path.dirname(__file__) # Get current directory
map_folder = path.join(game_folder, "maps")
img_folder = path.join(game_folder, "img")

def get_texture_path(file_name):
        img_path = path.join(img_folder, file_name)
        return img_path