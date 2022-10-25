import pygame as pg 
import numpy as np
import pygame.gfxdraw as gfx
pg.init()


# RGB VALUED TUPLES ASSIGNED TO KEYWORDS FOR EASY USE #
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
# RGB VALUED TUPLES ASSIGNED TO KEYWORDS FOR EASY USE #



#+-------------------------+#| TILE DATA |#+-------------------------+#
class Tile:
    def __init__(self, x1, y1, x2, y2, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color

floor_tile_sprite = pg.image.load('Sprite-0001.png')

map_radius = 20
main_scale_factor = 48
render_distance = 100

floor_surface_width = 1920
floor_surface_height = 1080
#+-------------------------+#| TILE DATA |#+-------------------------+#



#+------------------------------+#| PLAYER DATA |#+------------------------------+#
class Player:
    def __init__(self, x, y, width, height, theta, movespeed, rotspeed, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.theta = theta
        self.movespeed = movespeed
        self.rotspeed = rotspeed
        self.health = health

main_player = Player(0, 0, 32, 32, 0, (1/15), 2, 67)
#+------------------------------+#| PLAYER DATA |#+------------------------------+#



#+------------------------------+#| DISPLAY/SCREEN DATA |#+------------------------------+#
main_display_width = 1920
main_display_height = 1080
main_display = pg.display.set_mode((main_display_width, main_display_height))

main_clock = pg.time.Clock()
#+------------------------------+#| DISPLAY/SCREEN DATA |#+------------------------------+#


