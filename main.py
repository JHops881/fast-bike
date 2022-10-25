
import pygame as pg 
import numpy as np
import math
import sys
from EZConnect import EZConnect
import functions as func
import data
pg.init()


#+------------------------------+#| START GAME LOOP |#+------------------------------+#

while True:
    data.main_display.fill(data.BLACK)
    keys = pg.key.get_pressed()

    for event in pg.event.get(): #This is checking for exit
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    if keys[pg.K_ESCAPE]:
        pg.quit()
        sys.exit()


    
    if keys[pg.K_e]:
        data.main_player.theta-=2
    if keys[pg.K_q]:
        data.main_player.theta+=2

    if keys[pg.K_w]:
        x, y = func._rotate(data.main_player.theta, (0,1))
        data.main_player.x += x * data.main_player.movespeed
        data.main_player.y += y * data.main_player.movespeed

    if keys[pg.K_s]:
        x, y = func._rotate(data.main_player.theta, (0,-1))
        data.main_player.x += x * data.main_player.movespeed
        data.main_player.y += y * data.main_player.movespeed
 
    if keys[pg.K_a]:
        x, y = func._rotate(data.main_player.theta, (-1,0))
        data.main_player.x += x * data.main_player.movespeed
        data.main_player.y += y * data.main_player.movespeed
   
    if keys[pg.K_d]:
        x, y = func._rotate(data.main_player.theta, (1,0))
        data.main_player.x += x * data.main_player.movespeed
        data.main_player.y += y * data.main_player.movespeed

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


    func.draw_tiles(func.render_tiles(data.main_player, data.render_distance, func.all_tiles), data.main_player, data.main_display) 
    
    func.draw_player(data.main_player, data.main_display) #This object function draws our player
    func.draw_health(data.main_player, data.main_display)




    
    floor_surface = pg.Surface((data.floor_surface_width, data.floor_surface_height), pg.SRCALPHA, 32)
    floor_surface = floor_surface.convert_alpha()

    pg.draw.rect(floor_surface, data.RED, (
        (16 - data.main_player.x) * data.main_scale_factor,
        ((-5 - data.main_player.y) * data.main_scale_factor) * -1,
        1 * data.main_scale_factor,
        1 * data.main_scale_factor
        )
    )

    s = floor_surface.get_rect()
    dynamic_floor_surface = pg.transform.rotate(floor_surface, -data.main_player.theta)
    r = dynamic_floor_surface.get_rect()
    data.main_display.blit(dynamic_floor_surface, (0- (r.centerx - s.centerx),0 - (r.centery - s.centery)))
    





    pg.display.update()
    data.main_clock.tick(60) #This is refreshing the screen 60 fps


#+------------------------------+#| END GAME LOOP |#+------------------------------+#