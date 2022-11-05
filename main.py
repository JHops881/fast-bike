#!/usr/bin/env python
""" TODO document
"""

import pygame as pg 
import sys
from graphics import _rotate, GUIHealthBar, rotate_surface
from player import Player
from terrain import Terrain
from ceilingtile import CeilingTile
from floortile import FloorTile
from game_constants import BLACK, HEALTHBAR

__author__      = "Joseph Hopwood and Joshua Hopwood"
__credits__     = []
__version__     = "0.0.1"
__maintainer__  = "Joseph Hopwood"
__email__       = "jhopsmc@gmail.com"

# TODO move all of these constants to game_constants.py and refactor them to
# being capslock
mydisplay_width = 1920
mydisplay_height = 1080
mydisplay = pg.display.set_mode((mydisplay_width, mydisplay_height))

myclock = pg.time.Clock()

map_radius = 10
myscalefactor = 48
myrenderdistance = 100
myoffset = 36

myplayer = Player(0, 0, None, 32, 32, 0, 2, (1/15), 67, None, None)
test_floortiles = FloorTile.generate_map(map_radius)
test_ceilingtiles = [
    CeilingTile(-9, 7, 1, (False,False,False,False)),
    CeilingTile(-9, 5, 1, (True,True,True,True)),
    CeilingTile(9, 5, 1, (False,False,False,False))
]
test_terrains = [Terrain(4, -2, 1)]

healthbar = GUIHealthBar(myplayer, 20, 20, HEALTHBAR, mydisplay, (200, 40))

#+------------------------------+#| START GAME LOOP |#+------------------------------+#

if __name__ == "__main__":
    pg.init()
    while True:
        mydisplay.fill(BLACK)

        mysurface = pg.Surface((mydisplay_width, mydisplay_height), pg.SRCALPHA, 32)
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
            myplayer.theta-=2
        if keys[pg.K_q]:
            myplayer.theta+=2
        

        if keys[pg.K_w]:
            x, y = _rotate(myplayer.theta, (0,1))
            myplayer.x += x * myplayer.stats.movespeed
            myplayer.y += y * myplayer.stats.movespeed

        if keys[pg.K_s]:
            x, y = _rotate(myplayer.theta, (0,-1))
            myplayer.x += x * myplayer.stats.movespeed
            myplayer.y += y * myplayer.stats.movespeed
    
        if keys[pg.K_a]:
            x, y = _rotate(myplayer.theta, (-1,0))
            myplayer.x += x * myplayer.stats.movespeed
            myplayer.y += y * myplayer.stats.movespeed
    
        if keys[pg.K_d]:
            x, y = _rotate(myplayer.theta, (1,0))
            myplayer.x += x * myplayer.stats.movespeed
            myplayer.y += y * myplayer.stats.movespeed


        myplayer.constrain_theta()

        if keys[pg.K_z]:
            print(myplayer.theta)

        for d in test_floortiles:
            if d.is_visible(myplayer, myrenderdistance):
                d.draw(myplayer, mysurface, myscalefactor)

        for d in test_ceilingtiles:
            if d.is_visible(myplayer, myrenderdistance):
                d.draw_walls(myplayer, mysurface, myscalefactor, myoffset)
                d.draw(myplayer, mysurface, myscalefactor, myoffset)
        
        rotate_surface(myplayer, mysurface, mydisplay)
        
        for d in test_terrains:
            if d.is_visible(myplayer, myrenderdistance):
                d.draw(myplayer, mydisplay, myscalefactor)

        myplayer.draw(mydisplay)

        healthbar.draw()

        pg.display.update()
        myclock.tick(60) #This is refreshing the screen 60 fps

