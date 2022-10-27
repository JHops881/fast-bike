
import pygame as pg 
import numpy as np
import math
import sys
from EZConnect import EZConnect
import graphics as gxm
pg.init()


#+------------------------------+#| START GAME LOOP |#+------------------------------+#

while True:
    gxm.main_display.fill(gxm.BLACK)

    floor_surface = pg.Surface((gxm.floor_surface_width, gxm.floor_surface_height), pg.SRCALPHA, 32)
    floor_surface = floor_surface.convert_alpha()


    keys = pg.key.get_pressed()

    for event in pg.event.get(): #This is checking for exit
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    if keys[pg.K_ESCAPE]:
        pg.quit()
        sys.exit()


    
    if keys[pg.K_e]:
        gxm.main_player.theta-=2
    if keys[pg.K_q]:
        gxm.main_player.theta+=2

    if keys[pg.K_w]:
        x, y = gxm._rotate(gxm.main_player.theta, (0,1))
        gxm.main_player.x += x * gxm.main_player.movespeed
        gxm.main_player.y += y * gxm.main_player.movespeed

    if keys[pg.K_s]:
        x, y = gxm._rotate(gxm.main_player.theta, (0,-1))
        gxm.main_player.x += x * gxm.main_player.movespeed
        gxm.main_player.y += y * gxm.main_player.movespeed
 
    if keys[pg.K_a]:
        x, y = gxm._rotate(gxm.main_player.theta, (-1,0))
        gxm.main_player.x += x * gxm.main_player.movespeed
        gxm.main_player.y += y * gxm.main_player.movespeed
   
    if keys[pg.K_d]:
        x, y = gxm._rotate(gxm.main_player.theta, (1,0))
        gxm.main_player.x += x * gxm.main_player.movespeed
        gxm.main_player.y += y * gxm.main_player.movespeed

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



   


    gxm.draw_FloorTiles(gxm.render_FloorTiles(gxm.main_player, gxm.render_distance, gxm.all_FloorTiles), gxm.main_player, floor_surface)
    
    gxm.rotate_surface(gxm.main_player, floor_surface, gxm.main_display)
    
    gxm.draw_Terrain(gxm.main_player, gxm.render_Terrain(gxm.main_player, gxm.render_distance, gxm.all_Terrain), gxm.main_display)

    gxm.draw_player(gxm.main_player, gxm.main_display) #This object function draws our player

    gxm.draw_health(gxm.main_player, gxm.main_display)




    pg.display.update()
    gxm.main_clock.tick(60) #This is refreshing the screen 60 fps


#+------------------------------+#| END GAME LOOP |#+------------------------------+#