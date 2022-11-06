#!/usr/bin/env python
""" TODO file doc string
"""

import pygame as pg
from drawable import Drawable
from player import Player
from graphics import _rotate
from game_constants import CEILING_TILE_SPRITEMAP

__author__      = "Joseph Hopwood and Joshua Hopwood"
__credits__     = []
__version__     = "0.0.1"
__maintainer__  = "Joseph Hopwood"
__email__       = "jhopsmc@gmail.com"

class CeilingTile(Drawable):
    """ TODO document and refactor all the code below
    """

    def __init__(self, x: float, y: float, id: int, adjacent: tuple):
        super().__init__(x, y, id)
        self.adjacent = adjacent

    def is_visible(self, player: Player, renderdistance: int):
        if (((self.x + .5) - player.x)**2 + ((self.y + .5) - player.y)**2) < renderdistance:  
            return True
        else:
            return False

    def draw(self, player: Player, surface: pg.surface, scalefactor, offset) -> None:
        x = (self.x - player.x) * scalefactor + _rotate(player.theta, (0,offset))[0]
        y = ((self.y - player.y + 1) * scalefactor) * -1 - _rotate(player.theta, (0,offset))[1]
        p1 = (x + (surface.get_width() / 2), y + (surface.get_height() / 2))
        surface.blit(CEILING_TILE_SPRITEMAP[self.id], p1)

    def draw_walls(self, player: Player, surface: pg.surface, scalefactor, offset) -> None:
        if self.adjacent != (True,True,True,True):
            # --- # SOUTH SIDE # --- #
            #BOTOM LEFT OF CEIL
            x1s = (self.x - player.x) * scalefactor + _rotate(player.theta, (0,offset))[0]
            y1s = ((self.y - player.y + 1) * scalefactor) * -1 - _rotate(player.theta, (0,offset))[1]
            p1s = (x1s + (surface.get_width() / 2), y1s + (surface.get_height() / 2)+scalefactor)
            #BOTTOM RIGHT OF CEIL
            p2s = (p1s[0]+scalefactor, p1s[1])
            #BOTTOM LEFT OF FLOOR
            x4s = (self.x - player.x) * scalefactor 
            y4s = ((self.y - player.y + 1) * scalefactor) * -1
            p4s = (x4s + (surface.get_width() / 2), y4s + (surface.get_height() / 2)+scalefactor)
            #BORROM RIGHT OF FLOOR
            p3s = (p4s[0]+scalefactor, p4s[1])

            # --- # EAST SIDE # --- #
            #BRoC
            p1e = p2s
            #TRoC
            p2e = (p1e[0], p1e[1]-scalefactor)
            #TRoF
            p3e = (p3s[0], p3s[1]-scalefactor)
            #BRoF
            p4e = p3s

            # --- # NORTH SIDE # --- #
            #TRoC
            p1n = p2e
            #TLoC
            p2n = (p2e[0]-scalefactor, p2e[1])
            #TLoF
            p3n = (p3e[0]-scalefactor, p3e[1])
            #TRoF
            p4n = p3e

            # --- # WEST SIDE # --- #
            p1w = p2n
            p2w = p1s
            p3w = p4s
            p4w = p3n

            if player.theta == 0:
                if self.adjacent[2] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (105,85,85), (p1s,p2s,p3s,p4s)) #SOUTH DRAW

            elif 0 < player.theta < 90:
                if self.adjacent[2] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (105,85,85), (p1s,p2s,p3s,p4s)) #SOUTH DRAW
                if self.adjacent[1] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (85,65,65), (p1e,p2e,p3e,p4e)) #EAST DRAW

            elif player.theta == 90:
                if self.adjacent[1] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (85,65,65), (p1e,p2e,p3e,p4e)) #EAST DRAW

            elif 90 < player.theta < 180:
                if self.adjacent[1] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (85,65,65), (p1e,p2e,p3e,p4e)) #EAST DRAW
                if self.adjacent[0] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (145,125,125), (p1n,p2n,p3n,p4n)) #NORTH DRAW

            elif player.theta == 180:
                if self.adjacent[0] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (145,125,125), (p1n,p2n,p3n,p4n)) #NORTH DRAW

            elif 180 < player.theta < 270:
                if self.adjacent[0] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (145,125,125), (p1n,p2n,p3n,p4n)) #NORTH DRAW
                if self.adjacent[3] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (125,105,105), (p1w,p2w,p3w,p4w)) #WEST DRAW

            elif player.theta == 270:
                if self.adjacent[3] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (125,105,105), (p1w,p2w,p3w,p4w)) #WEST DRAW

            elif 270 < player.theta < 360:
                if self.adjacent[3] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (125,105,105), (p1w,p2w,p3w,p4w)) #WEST DRAW
                if self.adjacent[2] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (105,85,85), (p1s,p2s,p3s,p4s)) #SOUTH DRAW
