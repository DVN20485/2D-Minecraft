from os import path
import sys
from matplotlib.pyplot import savefig

#save file and module paths
current = path.dirname(path.realpath(__file__))
parent = path.dirname(current)
sys.path.append(parent)
save_folder = path.dirname(__file__)
 
def save_State(game, inventory): #called in player module on key press
    #current x and y of player
    playerX = game.player.x 
    playerY = game.player.y
    #world seed
    seed = game.map.seed
    #current inventory
    curInventory = (inventory)
    temp = ''
    #putting inventory into correct format when saved
    for items in curInventory.keys():
        temp += str(items)  + ',' + str(curInventory[items]) + ';'
    temp = temp[:-1]
    #create string that will be saved to .txt. first line position, 2nd line inventory, 3rd line will be seed when implemented
    playerStats = str(seed) + ',' + str(playerX) + ',' + str(playerY) + '\n' + temp

    #save to .txt
    saveFile = open(path.join(save_folder, "save.txt"),"w", encoding="utf-8")
    saveFile.writelines(playerStats)
    saveFile.close()

def load_State(player):#called in player module on key press
    #open save file
    saveFile = open(path.join(save_folder, "save.txt"),"r", encoding="utf-8")
    playerPOS = saveFile.readline() # x,y
    if(playerPOS != "\n" and playerPOS != ""):
        playerInven = saveFile.readline().split(';') # x,1;y,1;z,1 ...
        #set seed and player position as well as reset player inventory
       
        if(player.game.map.seed != int(playerPOS.split(',')[0])):
            player.game.map.seed = int(playerPOS.split(',')[0])
            player.game.update_map()
            
        player.x = int(playerPOS.split(',')[1])
        player.y = int(playerPOS.split(',')[2])
        
        player.game.playerInven.invDict = {}
        
        
        #assign inventory items
        if playerInven[0] != '':
            for item in playerInven:
                itemName = str(item.split(',')[0])
                itemQuant = int(item.split(',')[1])
                player.game.playerInven.addItem(itemName, itemQuant)
    saveFile.close()



    