#!/usr/bin/env python
""" TODO document
"""

import pygame as pg 
import sys
from graphics import _rotate, rotate_surface
from game_constants import *
from gui_elements import *

__author__      = "Joseph Hopwood and Joshua Hopwood"
__credits__     = []
__version__     = "0.0.2"
__maintainer__  = "Joseph Hopwood"
__email__       = "jhopsmc@gmail.com"


#+-------------------------+#| START GAME LOOP |#+----------------------------+#

if __name__ == "__main__":
    pg.init()
    while True:
        DISPLAY.fill(BLACK)

        mysurface = pg.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pg.SRCALPHA, 32)
        mysurface = mysurface.convert_alpha()

        keys = pg.key.get_pressed()

        for event in pg.event.get(): #This is checking for exit
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        if keys[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()


        
        if keys[pg.K_e]:
            PLAYER.theta-=2
        if keys[pg.K_q]:
            PLAYER.theta+=2
        

        if keys[pg.K_w]:
            x, y = _rotate(PLAYER.theta, (0,1))
            PLAYER.x += x * PLAYER.stats.movespeed
            PLAYER.y += y * PLAYER.stats.movespeed

        if keys[pg.K_s]:
            x, y = _rotate(PLAYER.theta, (0,-1))
            PLAYER.x += x * PLAYER.stats.movespeed
            PLAYER.y += y * PLAYER.stats.movespeed
    
        if keys[pg.K_a]:
            x, y = _rotate(PLAYER.theta, (-1,0))
            PLAYER.x += x * PLAYER.stats.movespeed
            PLAYER.y += y * PLAYER.stats.movespeed
    
        if keys[pg.K_d]:
            x, y = _rotate(PLAYER.theta, (1,0))
            PLAYER.x += x * PLAYER.stats.movespeed
            PLAYER.y += y * PLAYER.stats.movespeed


        PLAYER.constrain_theta()

        if keys[pg.K_z]:
            print(PLAYER.theta)

        for d in TEST_FLOORTILES:
            if d.is_visible(PLAYER, RENDERDISTANCE):
                d.draw(PLAYER, mysurface, SCALEFACTOR, FLOOR_TILE_SPRITEMAP)

        for d in TEST_CEILINGTILES:
            if d.is_visible(PLAYER, RENDERDISTANCE):
                d.draw_walls(PLAYER, mysurface, SCALEFACTOR, OFFSET)
                d.draw(PLAYER, mysurface, SCALEFACTOR, OFFSET, CEILING_TILE_SPRITEMAP)
        
        rotate_surface(PLAYER, mysurface, DISPLAY)
        
        for d in TEST_TERRAINS:
            if d.is_visible(PLAYER, RENDERDISTANCE):
                d.draw(PLAYER, DISPLAY, SCALEFACTOR, TERRAIN_SPRITEMAP)

        PLAYER.draw(DISPLAY)

        hpbar.draw()

        pg.display.update()
        CLOCK.tick(60) #This is refreshing the screen 60 fps

