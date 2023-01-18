import random
import sys
import opensimplex
from os import path
import numpy as np

current = path.dirname(path.realpath(__file__))
parent = path.dirname(current)
sys.path.append(parent)
import configurations 

map_folder = path.dirname(__file__)

def generateMap(chunkPos, ts): #position (in chunk units, eg -9,2)
    sizeX = configurations.MAP_WIDTH
    sizeY = configurations.MAP_HEIGHT

    grid = np.ones((sizeX, sizeY), dtype=int)   #makes array of 1s as default map grid
    biomes = []  # biomes noise array
    bluenoiseTree = []  #trees noise array
    bluenoiseStone = [] #stones noise array

    biomes, bluenoiseTree, bluenoiseStone = GenerateBiome(sizeX, sizeY, chunkPos, ts) #generates biome and bluenoise arrays 
    
    #placing trees and rocks
    densityTree = 4
    densityStone = 6 #more spread
    random.seed(ts[8])  # seed for random

    for yc in range(sizeY):
        for xc in range(sizeX):
            if(biomes[yc][xc]==0.3): #shrubland
                densityTree= 4
                densityStone = 6
            elif(biomes[yc][xc]==0.5): #forest
                densityTree= 1
                densityStone = 20
            elif(biomes[yc][xc]==0.7): #mountain
                densityTree= 7
                densityStone = 3
            elif(biomes[yc][xc]==0.9): #desert
                densityTree= 10
                densityStone = 1
            elif(biomes[yc][xc] == 0.08): #water
                densityTree = 1000
                densityStone = 1000
                grid[yc][xc] = configurations.MAPID["Water"]

            #tree 
            interestedSection = bluenoiseTree[(yc - densityTree) if(yc - densityTree >= 0) else (0): (yc + 1),
                                              (xc - densityTree) if(xc - densityTree >= 0) else (0): (xc + 1)]
            max = interestedSection.max()
            if(bluenoiseTree[yc][xc] == max):
                grid[yc][xc] = configurations.MAPID["Tree"]

            #stone
            interestedSection = bluenoiseStone[(yc - densityStone) if(yc - densityStone >= 0) else (0): (yc + 1),
                                               (xc - densityStone) if(xc - densityStone >= 0) else (0): (xc + 1)]

            max = interestedSection.max()
            if(bluenoiseStone[yc][xc] == max):
                ironSpawn = random.randint(0,100) 

                if(ironSpawn > 70): #probability of spawning an iron instead of rock = 30%
                    grid[yc][xc] = configurations.MAPID["Iron"]
                else:
                    grid[yc][xc] = configurations.MAPID["Stone"]

    if(chunkPos == [0, 0]):
        #static spawns
        #the ground the player spawns on
        grid[sizeY//2][sizeX//2] = configurations.MAPID["Dirt"]
        # the workbench
        grid[sizeY//2][sizeX//2-1] = configurations.MAPID["CraftingTable"]
    return toString(grid)

def toString(grid):  # returns the 2D map as a string to print
    output = ""
    for rows in grid:
        for columns in rows:
            output = output + str(columns) + ","
        output = output.rstrip(output[-1])
        output = output + "\n"
    return output

# returns the 2D boolean map as a string to print for debugging
def toStringBooleanGrid(grid):
    output = ""
    for i, rows in enumerate(grid):
        for j, columns in enumerate(rows):
            if grid[j][i]:
                output = output + "0 "
            else:
                output = output + "1 "
        output = output + "\n"
    return output

#Biomes section 
def makeBiome(temp, rain): #read numpy documention to vectorize this 
        if(temp < 0.1):  # Water
            return 0.08
        if(temp < 0.12):  # Beach (for future use, right now set to water)
            return 0.08
        elif(temp < 0.4):  # shrubland temp
            if(rain < 0.5):
                return 0.3  # shrubland
            elif(rain < 0.8):
                return 0.5  # forest
            else:
                return 0.7  # mountain
        elif(temp < 0.6):  # forest temp
            if(rain < 0.3):
                return 0.3  # shrubland
            elif(rain < 0.8):
                return 0.5  # forest
            elif(rain < 0.9):
                return 0.7  # mountain
            else:
                return 0.08  # water
        elif(temp < 0.8):  # mountain temp
            if(rain < 0.2):  # desert
                return 0.9
            elif(rain < 0.4):  # forest
                return 0.5
            elif(rain < 0.9):  # mountain
                return 0.7
            else:
                return 0.08  # water
        else:  # desert temp
            if(rain < 0.5):
                return 0.9  # desert
            elif(rain < 0.8):
                return 0.7  # mountain
            elif(rain < 0.9):
                return 0.5  # forest
            else:
                return 0.08  # water

def Noise(nx, ny):
    return opensimplex.noise2array(nx, ny) / 2.0 + 0.5

def GenerateBiome(width, height, chunkPosition, ts):
    wavelength = 8.0  # how 'smooth' the noise is
    chunkPosition[0] *= -3.75/30  # scaling chunk
    chunkPosition[1] *= 3.75/30  # scaling chunk

    nx = np.linspace(0, width/wavelength, width, endpoint= False) - 0.5 - chunkPosition[0]
    ny = np.linspace(0, height/wavelength, height, endpoint= False) - 0.5 - chunkPosition[1]

    opensimplex.seed(int(ts[0]))               # set initial seed 
    temp = Noise(nx,ny)
    opensimplex.seed(int(ts[1]))                #new seed so noise doesnt correlate to eachother and form patterns 
                                                # generate second set of noise at different frequency to make final noise map more interesting
    temp += 0.5*Noise(2*nx, 2*ny)

    opensimplex.seed(int(ts[2]))                 #pattern resistance again
    # generate 3rd set of noise at different frequency
    temp += 0.25*Noise(4*nx, 4*ny)
    # divide by collective amplitudes to keep noise in range of 0.0-1.0
    temp = temp / (1 + 0.5 + 0.25)
    # raise to exponent to "drop" elevation and have some areas of flat land and water
    temp = temp ** 1.7

    opensimplex.seed(int(ts[3]))  # set initial seed                                                      
    rain = Noise(nx, ny) # generate one set of noise

    opensimplex.seed(int(ts[4]))                   #new seed so noise doesnt correlate to eachother and form patterns 
    # generate second set of noise at different frequency to make final noise map more interesting
    rain += 0.5*Noise(2*nx, 2*ny)

    opensimplex.seed(int(ts[5]))                   #pattern resistance again
    # generate 3rd set of noise at different frequency
    rain += 0.25 * Noise(4*nx, 4*ny)
    # divide by collective amplitudes to keep noise in range of 0.0-1.0
    rain = rain / (1 + 0.5 + 0.25)
    rain = rain ** 1.7

    opensimplex.seed(int(ts[6]))  # seed for Tree  
    bluenoiseTree = Noise(50*nx , 50*ny )
    
    opensimplex.seed(int(ts[7])) #seed for Stone 
    bluenoiseStone = Noise(50*nx, 50*ny)
    biomes = [[0 for i in range(width)] for j in range(height)]

    for y in range (height):
        for x in range(width):
            biomes[y][x] = makeBiome(temp[x,y], rain[x,y])  # adds biome 'tile' to array
    return biomes, bluenoiseTree, bluenoiseStone

#main methods
def main(currX, currY, ts, writeToFile="map.txt"):
    grid = generateMap([currX, currY], ts)  # generates a 30x30 map

    # with open(path.join(map_folder, writeToFile), "w", encoding='utf8') as f:
    #     f.write(grid)
    #     f.close()
    return grid