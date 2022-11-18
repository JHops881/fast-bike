#!/usr/bin/env python
""" Defines the graphical functions for the fast-bike game.

    __Table of contents__ *This table is out of date*
    | ORDER     |  SUBJECT      |
    -----------------------------
    | 1         | colors        |
    | 2         | misc          |
    | 3         | functions     |    
    | 4         | player        |
    | 5         | floortile     |    
    | 6         | wall          |
    | 7         | ceilingtile   |    
    | 8         | terrain       |
    | 9         | particle      |
    | 10        | projectile    |    
    | 11        | gui           | 
"""
import math
import pygame as pg

from drawable import Drawable
from player import Player

__author__      = "Joseph Hopwood and Joshua Hopwood"
__credits__     = []
__version__     = "0.0.1"
__maintainer__  = "Joseph Hopwood"
__email__       = "jhopsmc@gmail.com"

pg.init()

def _rotate(theta: float, v: tuple) -> tuple():
    """ Given a vector (v) and an angle in degrees (theta),
        a vector is returned that has been rotated by the angle.

        Parameters:
        - `theta` angle in degrees
        - `v` vector

        returns rotated vector of v by theta degrees
    """
    assert v != None and len(v) == 2, "invalid v input"

    # Angle is converted from degrees to radians
    theta = math.radians(theta)            
    A = math.cos(theta) * v[0] - math.sin(theta) * v[1]
    B = math.sin(theta) * v[0] + math.cos(theta) * v[1]
    return (A, B)

def rotate_surface(player: Player, surface: pg.surface, 
    display: pg.display) -> None:
    """ Rotates a pg.surface (surface) based on a Player's (player) angle: 
        stored in Player.theta. The surface is rotated from the center point of
        itself. It is then blit onto a pg.display (display) such that the 
        centerpoint of the surface and the display overlap.

        Parameters:
        - `player`  The Player that the user wishes to derive the angle in which
            the surface is rotated from.
        - `surface` The pg.surface that the user desires to rotate and blit
        - `display` The pg.display that the user wishes to have the rotated 
            pg.surface blit onto
    """
    s = surface.get_rect()
    rotated_surface = pg.transform.rotate(surface, -player.theta)
    r = rotated_surface.get_rect()
    display.blit(rotated_surface, 
            (0 - (r.centerx - s.centerx), 0 - (r.centery - s.centery)))