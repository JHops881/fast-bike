#!/usr/bin/env python
""" TODO file doc string
"""

import pygame as pg
from drawable import Drawable
from player import Player
from graphics import _rotate
from game_constants import TERRAIN_SPRITEMAP

__author__      = "Joseph Hopwood and Joshua Hopwood"
__credits__     = []
__version__     = "0.0.1"
__maintainer__  = "Joseph Hopwood"
__email__       = "jhopsmc@gmail.com"

class Terrain(Drawable):
    """ TODO document and refactor code below
    """
    def is_visible(self, player: Player, renderdistance: int):
        if (((self.x + .5) - player.x)**2 + ((self.y + .5) - player.y)**2) < renderdistance:
            return True
        else:
            return False

    def draw(self, player, display: pg.display, scalefactor: int) -> None:
        x = (self.x - player.x) * scalefactor
        y = ((self.y - player.y + 1) * scalefactor) * -1
        x, y = _rotate(player.theta, (x,y))
        x -= (TERRAIN_SPRITEMAP[self.id].get_width() / 2)
        y -= TERRAIN_SPRITEMAP[self.id].get_height()
        p1 = (x + (display.get_width() / 2), y + (display.get_height() / 2))
        display.blit(TERRAIN_SPRITEMAP[self.id], p1)