import pygame as pg 
import numpy as np
import math
import sys
from EZConnect import EZConnect
import graphics as glib
pg.init()



mydisplay_width = 1920
mydisplay_height = 1080
mydisplay = pg.display.set_mode((mydisplay_width, mydisplay_height))

myclock = pg.time.Clock()

map_radius = 10
myscalefactor = 48
myrenderdistance = 100
myoffset = 36

myplayer = glib.Player(0, 0, None, 32, 32, 0, 2, (1/15), 67, None, None)
test_floortiles = glib.FloorTile.generate_map(map_radius)
test_ceilingtiles = [
    glib.CeilingTile(-9, 7, 1, (False,False,False,False)),
    glib.CeilingTile(-9, 5, 1, (True,True,True,True)),
    glib.CeilingTile(9, 5, 1, (False,False,False,False))
]
test_terrains = [glib.Terrain(4, -2, 1)]

healthbar = glib.GUIHealthBar(myplayer, 20, 20, glib.healthbar, mydisplay, (200, 40))

#+------------------------------+#| START GAME LOOP |#+------------------------------+#

while True:
    mydisplay.fill(glib.BLACK)

    mysurface = pg.Surface((mydisplay_width, mydisplay_height), pg.SRCALPHA, 32)
    mysurface = mysurface.convert_alpha()

    keys = pg.key.get_pressed()

    for event in pg.event.get(): #This is checking for exit
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    if keys[pg.K_ESCAPE]:
        pg.quit()
        sys.exit()


    
    if keys[pg.K_e]:
        myplayer.theta-=2
    if keys[pg.K_q]:
        myplayer.theta+=2
    

    if keys[pg.K_w]:
        x, y = glib._rotate(myplayer.theta, (0,1))
        myplayer.x += x * myplayer.stats.movespeed
        myplayer.y += y * myplayer.stats.movespeed

    if keys[pg.K_s]:
        x, y = glib._rotate(myplayer.theta, (0,-1))
        myplayer.x += x * myplayer.stats.movespeed
        myplayer.y += y * myplayer.stats.movespeed
 
    if keys[pg.K_a]:
        x, y = glib._rotate(myplayer.theta, (-1,0))
        myplayer.x += x * myplayer.stats.movespeed
        myplayer.y += y * myplayer.stats.movespeed
   
    if keys[pg.K_d]:
        x, y = glib._rotate(myplayer.theta, (1,0))
        myplayer.x += x * myplayer.stats.movespeed
        myplayer.y += y * myplayer.stats.movespeed


    myplayer.constrain_theta()

    if keys[pg.K_z]:
        print(myplayer.theta)




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



   


    for d in test_floortiles:
        if d.is_visible(myplayer, myrenderdistance):
            d.draw(myplayer, mysurface, myscalefactor)

    for d in test_ceilingtiles:
        if d.is_visible(myplayer, myrenderdistance):
            d.draw_walls(myplayer, mysurface, myscalefactor, myoffset)
            d.draw(myplayer, mysurface, myscalefactor, myoffset)
    
    glib.rotate_surface(myplayer, mysurface, mydisplay)
    
    for d in test_terrains:
        if d.is_visible(myplayer, myrenderdistance):
            d.draw(myplayer, mydisplay, myscalefactor)

    myplayer.draw(mydisplay)

    healthbar.draw()

    pg.display.update()
    myclock.tick(60) #This is refreshing the screen 60 fps


#+------------------------------+#| END GAME LOOP |#+------------------------------+#