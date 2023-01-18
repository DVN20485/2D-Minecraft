from game import *

def main():
	g = Game() # initialize pygame etc and import sprite images into pg  / call g = Game(seed=1234) for set seed
	g.new() # initialize all game objects (player, map, inventory, etc)
	g.menu() # show game menu


if __name__ == "__main__":
    main()
