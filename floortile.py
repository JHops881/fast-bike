#!/usr/bin/env python
""" TODO file doc string
"""

import pygame as pg
from drawable import Drawable
from player import Player

__author__      = "Joseph Hopwood and Joshua Hopwood"
__credits__     = []
__version__     = "0.0.1"
__maintainer__  = "Joseph Hopwood"
__email__       = "jhopsmc@gmail.com"


class FloorTile(Drawable):

    def generate_map(r: int) -> list:
        """
        For a given radius (r), a list of FloorTile objects is returned. The
        FloorTile objects are arranged at coordinates such that they from a 
        square with the given "radius".
        Parameters:
        - `r` a radius that the user desired the square to have.
        Returns 
        - a list of FloorTile obejects that are in a square. The 
            FloorTile obejects are centered around (0,0)
        """
        tiles = list()
        for y in range(r, -r, -1):
            for x in range(-r, r, 1):
                tiles.append(FloorTile(x, y, 1))
        return tiles

    def is_visible(self, player: Player, renderdistance: int) -> bool:
        """
        Tells us whether or not the FloorTile object is visble to the player
        """
        if (((self.x + .5) - player.x)**2
            + ((self.y + .5) - player.y)**2) < renderdistance:
            return True
        else:
            return False

    def draw(self, player:Player, surface:pg.surface,
             scalefactor:int, map:dict) -> None:
        
        x  = (self.x - player.x) * scalefactor 
        y  = ((self.y - player.y + 1) * scalefactor) * -1
        p1 = (
            x + (surface.get_width()  / 2),
            y + (surface.get_height() / 2)
        )
        surface.blit(map[self.id], p1)