
####################################################### IMPORTS ##############################################################

import pygame as pg 
import numpy as np
import math
import sys
pg.init()

####################################################### COLORS ##############################################################

BLACK = (0, 0, 0) #COLORS
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

######################################################## DISPLAY ##############################################################

main_display_width = 1920
main_display_height = 1080

main_display = pg.display.set_mode((main_display_width, main_display_height))
main_clock = pg.time.Clock()


main_tiles = [((0, 0), (100, 100), RED), ((100, 0), (200, 100), CYAN), ((200, 0), (300, 100), YELLOW)]

def draw_tiles(display, tiles):
    for tile in tiles:
        w = math.fabs(tile[1][0] - tile[0][0])
        h = math.fabs(tile[1][1] - tile[0][1])
        pg.draw.rect(display, tile[2], (tile[0][0], tile[0][1], w, h))
        


######################################################### PLAYER ############################################################

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def draw_player(self, display):
        pg.draw.rect(display, WHITE, (self.x, self.y, self.width, self.height))

main_player_width = 32
main_player_height = 32
main_player = Player((main_display_width - main_player_width) / 2, (main_display_height - main_player_height) / 2, main_player_width, main_player_height)


######################################################### GAME LOOP ############################################################

while True:
    main_display.fill(BLACK) #This fills the screen with the color

    draw_tiles(main_display, main_tiles)

    for event in pg.event.get(): #This is checking for exit
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    

    main_player.draw_player(main_display) #This object function draws our player

    pg.display.update()
    main_clock.tick(60) #This is refreshing the screen 60 fps