from dis import dis
import pygame as pg
import math
import sys
pg.init()


main_clock = pg.time.Clock()

#--------------------------# FONT #--------------------------# 
myfont = pg.font.Font('cour.ttf', 20)
exporttext = myfont.render('/export: _', False, (255,255,255), None)

#--------------------------# FUNCTIONS #--------------------------# 

def was_clicked(x: float, y: float, w: float, h: float) -> bool:
    '''
    Given the dimensions and location of a rectangular zone in screen space, returns a bool of whether or 
    not the mouse cursor is whithin the zone's bounds.

    Parameters:
    x (float): the x coordinate of the upper left corner of the zone
    y (float): the y coordinate of the upper left corner of the zone
    w (float): the width of the zone
    h (float): the height of the zone

    Returns:
    bool: whether or not the mouse postion is whithin the bounds of the zone
    '''
    if x <= mouse_x <= x+w and y <= mouse_y <= y+h:
        return True
    else:
        return False



#--------------------------# DISPLAY #--------------------------# 
display_width = 1920
display_height = 1080
display = pg.display.set_mode((display_width, display_height))


#--------------------------# VIEWPORT #--------------------------# 
viewport_width, viewport_height = 1608, 952
viewport_x, viewport_y = 64, 64

#--------------------------# SELECTOR #--------------------------# 
selected_sprite = pg.image.load('selected.png')
selected_sprite_x, selected_sprite_y = 1712, 74
brush = 1

FloorTile_sprite_map = {
    1: pg.image.load('./textures/sand.png'),
    2: pg.image.load('./textures/rock.png'),
    3: pg.image.load('./textures/dirt.png'),
    4: pg.image.load('./textures/grass.png'),
    5: pg.image.load('./textures/water.png'),
}

selector_width, selector_height = 184, 440
selector_x, selector_y = 1702, 64

sand_x, sand_y = 1712, 74 #the w and h are both 48
rock_x, rock_y = 1770, 74
dirt_x, dirt_y = 1828, 74
grass_x, grass_y = 1712, 132
water_x, water_y = 1770, 132

#--------------------------# MAIN #--------------------------# 
while True:

    display.fill((45,49,45))
    pg.draw.rect(display, (0,0,0), (viewport_x, viewport_y, viewport_width, viewport_height)) #viewport
    display.blit(exporttext, (76,70))


    pg.draw.rect(display, (60,64,60), (selector_x, selector_y, selector_width, selector_height)) #selector
    display.blit(FloorTile_sprite_map[1], (sand_x, sand_y)) #sand in selector
    display.blit(FloorTile_sprite_map[2], (rock_x, rock_y)) #rock in selector
    display.blit(FloorTile_sprite_map[3], (dirt_x, dirt_y)) #dirt in selector
    display.blit(FloorTile_sprite_map[4], (grass_x, grass_y)) #grass in selector
    display.blit(FloorTile_sprite_map[5], (water_x, water_y))

    display.blit(selected_sprite, (selected_sprite_x, selected_sprite_y))

    mouse_x, mouse_y = pg.mouse.get_pos()
    keys = pg.key.get_pressed()

    for event in pg.event.get(): #This is checking for exit
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if was_clicked(sand_x, sand_y, 48, 48) == True:
                selected_sprite_x, selected_sprite_y = sand_x-2, sand_y-2
                brush = 1

            if was_clicked(rock_x, rock_y, 48, 48) == True:
                selected_sprite_x, selected_sprite_y = rock_x-2, rock_y-2
                brush = 2

            if was_clicked(dirt_x, dirt_y, 48, 48) == True:
                selected_sprite_x, selected_sprite_y = dirt_x-2, dirt_y-2
                brush = 3 

            if was_clicked(grass_x, grass_y, 48, 48) == True:
                selected_sprite_x, selected_sprite_y = grass_x-2, grass_y-2
                brush = 4

            if was_clicked(water_x, water_y, 48, 48) == True:
                selected_sprite_x, selected_sprite_y = water_x-2, water_y-2
                brush = 5

    if keys[pg.K_ESCAPE]:
        pg.quit()
        sys.exit()




    pg.display.update()
    main_clock.tick(30)