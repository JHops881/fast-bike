#!/usr/bin/env python
""" Holds the abstract base class for all drawable game objects not including
    the gui.

    Drawable game objects should inheret from `Drawable` and override the 
    methods `is_visible` and `draw`.
"""

import abc

__author__      = "Joseph Hopwood and Joshua Hopwood"
__credits__     = []
__version__     = "0.0.1"
__maintainer__  = "Joshua Hopwood"
__email__       = "joshhoppers@gmail.com"

class Drawable(metaclass=abc.ABCMeta):
    """
    Game elements that can be diplayed onto the screen.
    """

    def __init__(self, x:float, y:float, id:int):
        """
        Create a new drawable game object.
        - `x` the x position of the object
        - `y` the y position of the object
        """
        self.x = x
        self.y = y
        self.id = id

    @abc.abstractmethod
    def is_visible(self) -> bool:
        """
        Returns true if the game element is currently visable
        """
        raise NotImplementedError

    @abc.abstractmethod
    def draw(self):
        """
        Draws this game object to the screen
        """
        raise NotImplementedError
