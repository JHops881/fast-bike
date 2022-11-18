#!/usr/bin/env python
""" Holds the constants for the fast-bike game.

    Constants should be declared in all caps and seperated into sections by
    similarity.
"""

import pygame as pg
from player import Player
from floortile import FloorTile
from ceilingtile import CeilingTile
from terrain import Terrain


__author__      = "Joseph Hopwood and Joshua Hopwood"
__credits__     = []
__version__     = "0.0.2"
__maintainer__  = "Joseph Hopwood"
__email__       = "jhopsmc@gmail.com"

# colors 
BLACK           = (0,   0,   0  )
GRAY            = (127, 127, 127)
WHITE           = (255, 255, 255)
RED             = (255, 0,   0  )
GREEN           = (0,   255, 0  )
BLUE            = (0,   0,   255)
YELLOW          = (255, 255, 0  )
CYAN            = (0,   255, 255)
MAGENTA         = (255, 0,   255)


DISPLAY_WIDTH   = 1920
DISPLAY_HEIGHT  = 1080
DISPLAY         = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))


CLOCK           = pg.time.Clock()


MAP_RADIUS      = 10
SCALEFACTOR     = 48
RENDERDISTANCE  = 100
OFFSET          = 36


PLAYER          = Player(0, 0, None, 32, 32, 0, 2, (1/15), 67, None, None)


TEST_TERRAINS   = [Terrain(4, -2, 1)]


TEST_FLOORTILES   = FloorTile.generate_map(MAP_RADIUS)


TEST_CEILINGTILES = [
    CeilingTile(-9, 7, 1, (False,False,False,False)),
    CeilingTile(-9, 5, 1, (True,True,True,True)),
    CeilingTile(9, 5, 1, (False,False,False,False))
]







# spritemaps
FLOOR_TILE_SPRITEMAP = {
    1: pg.transform.scale(
        pg.image.load('./Sprites/FloorTile/grass.png'), (48,48)
    )
}

CEILING_TILE_SPRITEMAP = {
    1: pg.image.load('./Sprites/CeilingTile/none.png')
}

TERRAIN_SPRITEMAP = {
    1: pg.image.load("./Sprites/Environment/cactus.png")
}

HEALTHBAR = pg.image.load('./Sprites/GUI/healthbar100.png')


