#!/usr/bin/env python
""" TODO implement and document
"""

from drawable import Drawable

__author__      = "Joseph Hopwood and Joshua Hopwood"
__credits__     = []
__version__     = "0.0.1"
__maintainer__  = "Joseph Hopwood"
__email__       = "jhopsmc@gmail.com"

class Projectile(Drawable):
    def __init__(self, x: float, y: float, id: int, theta: int):
        super().__init__(x, y, id)
        self.theta = theta