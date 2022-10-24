
####################################################### IMPORTS ##############################################################
import pygame as pg 
import numpy as np
import random
import math
import sys
import pygame.gfxdraw as gfx
import PIL
from EZConnect import EZConnect
pg.init()
######################################################## DATA ##############################################################
BLACK = (0, 0, 0) #COLORS
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

floor_tile_sprite = pg.image.load('Sprite-0001.png')

class Tile:
    def __init__(self, x1, y1, x2, y2, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color

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

main_display_width = 1920
main_display_height = 1080
main_display = pg.display.set_mode((main_display_width, main_display_height))

floor_surface_width = 1920
floor_surface_height = 1080


main_clock = pg.time.Clock()

main_scale_factor = 48
render_distance = 100
map_radius = 20

######################################################## FUNCTIONS ##############################################################


def _rotate(theta, v):
    theta = math.radians(theta)
    A = math.cos(theta) * v[0] - math.sin(theta) * v[1]
    B = math.sin(theta) * v[0] + math.cos(theta) * v[1]
    return (A, B)

def _draw(tile, player, display):
    w = math.fabs(tile.x2 - tile.x1) * main_scale_factor
    h = math.fabs(tile.y2 - tile.y1) * main_scale_factor
    x = (tile.x1 - player.x) * main_scale_factor 
    y = ((tile.y1 - player.y) * main_scale_factor) * -1 
    p1 = _rotate(player.theta, (x,y))
    p1 = (p1[0] + (main_display_width / 2), p1[1] + (main_display_height / 2))
    p2 = _rotate(player.theta, (x+w,y))
    p2 = (p2[0] + (main_display_width / 2), p2[1] + (main_display_height / 2))
    p3 = _rotate(player.theta, (x+w, y+h))
    p3 = (p3[0] + (main_display_width / 2), p3[1] + (main_display_height / 2))
    p4 = _rotate(player.theta, (x, y+h))
    p4 = (p4[0] + (main_display_width / 2), p4[1] + (main_display_height / 2))
    pg.draw.polygon(display, tile.color, (p1, p2, p3, p4))
    #gfx.aapolygon(display, (p1, p2, p3, p4), RED)

def draw_tiles(tiles, player, display):
    for tile in tiles:
        _draw(tile, player, display)

def draw_player(player, display):
    pg.draw.rect(display, WHITE, ((main_display_width - player.width) / 2, (main_display_height - player.height) / 2, player.width, player.height))

def generate_tiles(r):
    tiles = []
    for y in range(r, -r, -1):
        for x in range(-r, r, 1):
            tiles.append(Tile(x, y, (x + 1), (y - 1), GRAY))
    return tiles

def render_tiles(player, renderdistance, tiles):
    _rendered_tiles = []
    for tile in tiles:
        if ((((tile.x1 + tile.x2) / 2) - player.x)**2 + (((tile.y1 + tile.y2) / 2) - player.y)**2) < renderdistance:
            _rendered_tiles.append(tile)
    return _rendered_tiles

all_tiles = generate_tiles(map_radius)

def draw_health(player, display):
    gfx.aapolygon(display, ((20, 20),(220, 20),(220, 60), (20, 60)), RED)
    x_offset = 0
    for hp in range(player.health + 1):
        pg.draw.rect(display, RED, (20 + x_offset, 20, 2, 40))
        x_offset = hp * 2


######################################################### GAME LOOP ############################################################


while True:
    main_display.fill(BLACK) #This fills the screen with the color
    keys = pg.key.get_pressed()

    for event in pg.event.get(): #This is checking for exit
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    if keys[pg.K_ESCAPE]:
        pg.quit()
        sys.exit()


    
    if keys[pg.K_e]:
        main_player.theta-=2
    if keys[pg.K_q]:
        main_player.theta+=2

    if keys[pg.K_w]:
        x, y = _rotate(main_player.theta, (0,1))
        main_player.x += x * main_player.movespeed
        main_player.y += y * main_player.movespeed

    if keys[pg.K_s]:
        x, y = _rotate(main_player.theta, (0,-1))
        main_player.x += x * main_player.movespeed
        main_player.y += y * main_player.movespeed
 
    if keys[pg.K_a]:
        x, y = _rotate(main_player.theta, (-1,0))
        main_player.x += x * main_player.movespeed
        main_player.y += y * main_player.movespeed
   
    if keys[pg.K_d]:
        x, y = _rotate(main_player.theta, (1,0))
        main_player.x += x * main_player.movespeed
        main_player.y += y * main_player.movespeed

    ### PROOF OF CONCEPT SERVER TILES!
    # with EZConnect('192.168.1.11', 4398) as t:
    #     resp, ping = t.req({
    #         'event': 'get_chunk',
    #         'coords': [int(main_player.x/8), int(main_player.y/8)]  
    #     })

    # serverTitles = []
    # for tile in resp['tiles']:
    #     serverTitles.append(Tile(tile['a'][0], tile['a'][1], (tile['a'][0]+ 1), (tile['a'][1] - 1), tile['color']))
    # draw_tiles(render_tiles(main_player, render_distance, serverTitles), main_player, main_display)
    ### END PROOF OF CONCEPT


    draw_tiles(render_tiles(main_player, render_distance, all_tiles), main_player, main_display) 
    
    draw_player(main_player, main_display) #This object function draws our player
    draw_health(main_player, main_display)





    floor_surface = pg.Surface((floor_surface_width, floor_surface_height), pg.SRCALPHA, 32)
    floor_surface = floor_surface.convert_alpha()

    pg.draw.rect(floor_surface, RED, (
        (16 - main_player.x) * main_scale_factor,
        ((-5 - main_player.y) * main_scale_factor) * -1,
        1 * main_scale_factor,
        1 * main_scale_factor
        )
    )

    s = floor_surface.get_rect()
    dynamic_floor_surface = pg.transform.rotate(floor_surface, -main_player.theta)
    r = dynamic_floor_surface.get_rect()
    main_display.blit(dynamic_floor_surface, (0- (r.centerx - s.centerx),0 - (r.centery - s.centery)))
    





    pg.display.update()
    main_clock.tick(60) #This is refreshing the screen 60 fps