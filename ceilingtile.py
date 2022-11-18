#!/usr/bin/env python
""" 
Holds the CeilingTile class along with all relevant information and metadata.

CelingTiles are the tiles that the player does not walk on.
"""

import pygame       as pg
from   drawable import Drawable
from   player   import Player
from   graphics import _rotate


__author__      = "Joseph Hopwood and Joshua Hopwood"
__credits__     = []
__version__     = "0.0.2"
__maintainer__  = "Joseph Hopwood"
__email__       = "jhopsmc@gmail.com"



class CeilingTile(Drawable):
    """
    `CeilingTile` is a child of the parent class `Drawable`. `CeilingTile`s are
    drawn on the screen with an offset to give the illusion of a vertical height
    map. `CeilingTile`s are accompanied with drawn wall polygons to create an 
    orthographically projected 3d block.
    """

    def __init__(self, x: float, y: float, id: int, adjacent: tuple):
        super().__init__(x, y, id)
        self.adjacent = adjacent



    def is_visible(self, player: Player, renderdistance: int) -> bool:
        """
        Determines whether a `CeilingTile` should be projected or not depending
        on a decided distance from the player on the screen.
        
        Parameters:
        - `player` who the user wants to base the visibility about.
        - `renderdistance` the squared value of what the user decides
            the distance of visible tiles should be.
            
        Returns:
        - a bool of whether or not the `CeilingTile` is within
            the `renderdistance`. 
        """
        dist = (((self.x + .5) - player.x)**2 + ((self.y + .5) - player.y)**2)
        if dist < renderdistance:  
            return True
        
        else:
            return False




    def draw(              self, 
            player      :  Player,
            surface     :  pg.surface,
            scalefactor :  int,
            offset      :  int,
            map         :  dict
        )-> None:
        
        x = (    (self.x - player.x)
               *  scalefactor
               +  _rotate(player.theta,(0,offset))[0]
        )
        
        y = (    (self.y - player.y + 1)
               *  scalefactor
               *  -1
               -  _rotate(player.theta,(0,offset))[1]
        )
        
        p1 = (
            x + (surface.get_width()  / 2),
            y + (surface.get_height() / 2)  
        )
        
        surface.blit(map[self.id], p1)




    def draw_walls(         self,
            player       :  Player,
            surface      :  pg.surface,
            scalefactor  :  int,
            offset       :  int
        )-> None:
        
        # We want to first check if there are other blocks on all four sides of
        # this block, if there is we return nothing and dont draw its walls.
        # this is an optimization added so we dont do a bunch of math for
        # nothing and needlessly tax the CPU
        if self.adjacent == (True,True,True,True):
            return None
        
        # for a wall polygon, the points (p) are in these respective places
        #
        #      p1----------p2                 -Suffix Key-
        #       |          |                    s: south
        #       |          |                    e: east
        #       |          |                    n: north
        #      p4----------p3                   w: west
        
        #----------------------------------------------------------------------#
        # We start by finding the points for the SOUTH wall polygon
        # The first point we find is the top left point of the polygon
            #( or the bottom left point of the ceiling tile)
        x1s = (    (self.x - player.x)
                *   scalefactor
                +   _rotate(player.theta,(0,offset))[0])
        
        y1s = (    (self.y - player.y + 1)
                *   scalefactor
                *   -1
                -   _rotate(player.theta, (0,offset))[1])

        p1s = (                                                 #Point 1
            x1s + (surface.get_width()  / 2),
            y1s + (surface.get_height() / 2) + scalefactor)
        
        p2s = (p1s[0] + scalefactor, p1s[1])                    #Point 2
        
        x4s = (self.x - player.x) * scalefactor 
        y4s = ((self.y - player.y + 1) * scalefactor) * -1
        p4s = (                                                 #Point 4
            x4s + (surface.get_width()  / 2),
            y4s + (surface.get_height() / 2) + scalefactor)
        
        p3s = (p4s[0]+scalefactor, p4s[1])                      #Point 3
        #----------------------------------------------------------------------#
        p1e = p2s
        p2e = (p1e[0], p1e[1]-scalefactor)
        p3e = (p3s[0], p3s[1]-scalefactor)
        p4e = p3s
        #----------------------------------------------------------------------#
        p1n = p2e
        p2n = (p2e[0]-scalefactor, p2e[1])
        p3n = (p3e[0]-scalefactor, p3e[1])
        p4n = p3e
        #----------------------------------------------------------------------#
        p1w = p2n
        p2w = p1s
        p3w = p4s
        p4w = p3n


        # This section, in summary, is just checking the players camera angle
        # to draw only the walls that would be visible to the player given 
        # their current angle.
        
        # Additionally, it checks for an adjacent block on the sides decides
        # to draw the wall polygons on; if there is an adjacent block it will
        # not draw.
        if player.theta == 0:
            if self.adjacent[2]:
                pass
            else:
                # draw the south wall
                pg.draw.polygon(surface, (105,85,85), (p1s,p2s,p3s,p4s))


        elif 0 < player.theta < 90:
            if self.adjacent[2]:
                pass
            else:
                # draw the south wall
                pg.draw.polygon(surface, (105,85,85), (p1s,p2s,p3s,p4s))
            if self.adjacent[1]:
                pass
            else:
                # draw the east wall
                pg.draw.polygon(surface, (85,65,65), (p1e,p2e,p3e,p4e))


        elif player.theta == 90:
            if self.adjacent[1]:
                pass
            else:
                # draw the east wall
                pg.draw.polygon(surface, (85,65,65), (p1e,p2e,p3e,p4e))


        elif 90 < player.theta < 180:
            if self.adjacent[1]:
                pass
            else:
                #draw the east wall
                pg.draw.polygon(surface, (85,65,65), (p1e,p2e,p3e,p4e))
            if self.adjacent[0]:
                pass
            else:
                #draw the north wall
                pg.draw.polygon(surface, (145,125,125), (p1n,p2n,p3n,p4n)) 


        elif player.theta == 180:
            if self.adjacent[0]:
                pass
            else:
                #draw the north wall
                pg.draw.polygon(surface, (145,125,125), (p1n,p2n,p3n,p4n))


        elif 180 < player.theta < 270:
            if self.adjacent[0]:
                pass
            else:
                #draw the north wall
                pg.draw.polygon(surface, (145,125,125), (p1n,p2n,p3n,p4n))
            if self.adjacent[3]:
                pass
            else:
                #draw the west wall
                pg.draw.polygon(surface, (125,105,105), (p1w,p2w,p3w,p4w))


        elif player.theta == 270:
            if self.adjacent[3]:
                pass
            else:
                #draw the west wall
                pg.draw.polygon(surface, (125,105,105), (p1w,p2w,p3w,p4w))


        elif 270 < player.theta < 360:
            if self.adjacent[3]:
                pass
            else:
                #draw the west wall
                pg.draw.polygon(surface, (125,105,105), (p1w,p2w,p3w,p4w))
            if self.adjacent[2]:
                pass
            else:
                #draw the south wall
                pg.draw.polygon(surface, (105,85,85), (p1s,p2s,p3s,p4s))
