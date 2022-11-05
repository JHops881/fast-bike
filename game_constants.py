#!/usr/bin/env python
""" Holds the constants for the fast-bike game.

    Constants should be declared in all caps and seperated into sections by
    similarity.
"""

import pygame as pg

__author__      = "Joseph Hopwood and Joshua Hopwood"
__credits__     = []
__version__     = "0.0.1"
__maintainer__  = "Joseph Hopwood"
__email__       = "jhopsmc@gmail.com"

# colors 
BLACK           = (0, 0, 0)
GRAY            = (127, 127, 127)
WHITE           = (255, 255, 255)
RED             = (255, 0, 0)
GREEN           = (0, 255, 0)
BLUE            = (0, 0, 255)
YELLOW          = (255, 255, 0)
CYAN            = (0, 255, 255)
MAGENTA         = (255, 0, 255)

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

# gui
HEALTHBAR = pg.image.load('./Sprites/GUI/healthbar100.png')