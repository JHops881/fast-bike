#!/usr/bin/env python
""" Implements the player for the fast-bike game

    The player is a speciale case of a sprite.
"""

import pygame as pg
from drawable import Drawable

__author__      = "Joseph Hopwood and Joshua Hopwood"
__credits__     = []
__version__     = "0.0.1"
__maintainer__  = "Joseph Hopwood"
__email__       = "jhopsmc@gmail.com"

class Player(Drawable):
    """ TODO give class desc
    """

    class Stats:
        """ TODO give class desc
        """
        def __init__(self, movespeed:float, health:int):
            self.movespeed = movespeed
            self.health = health

    class Inventory:
        """ TODO give class desc
        """
        def __init__(self, stored:list, hotbar:list):
            self.stored = stored
            self.hotbar = hotbar

    def __init__(self, x:float, y:float, id:int, width:int,height:int,theta:int,
    rotspeed:int, movespeed:float, health:int, stored:list, hotbar:list):
        """ TODO give method desc
        """
        super().__init__(x, y, id)
        self.width = width
        self.height = height
        self.theta = theta
        self.rotspeed = rotspeed
        self.stats = self.Stats(movespeed, health)
        self.inventory = self.Inventory(stored, hotbar)

    def draw(self, display: pg.display) -> None:
        """ Draws the player in the center of the screen.

            Parameters:
            - `player` desired player object to be drawn
            - `display` The display that the player is to be drawn on
        """
        pg.draw.rect(display,(0,255,0), ((display.get_width() - self.width) / 2,
        (display.get_height() - self.height) / 2, self.width, self.height))

    def constrain_theta(self):
        """ TODO give method desc
        """
        if self.theta != 360 and self.theta != -2:
            pass
        elif self.theta == 360:
            self.theta = 0
        elif self.theta == -2:
            self.theta = 358
        else:
            pass

    def is_visible(self) -> bool:
        """ TODO give method desc
            TODO implment method... ill give you a hint, is the player ever NOT
            visable? 
        """
        pass