from dis import dis
import pygame as pg
import math
import sys
pg.init()


main_clock = pg.time.Clock()

#--------------------------# FONT #--------------------------# 
myfont = pg.font.Font('cour.ttf', 20)
myfont.bold = True

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

#--------------------------# SELECTOR #--------------------------# 
selected_sprite = pg.image.load('selected.png')
selected_sprite_x, selected_sprite_y = 1712, 74
brush = 1

FloorTile_sprite_map = {
    0: pg.image.load('./textures/none.png'),
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
#--------------------------# VIEWPORT #--------------------------# 
viewport_width, viewport_height = 1608, 952
viewport_x, viewport_y = 64, 64

view_scale_factor = 48
view_render_distance = (17.5,11)
class Anchor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
viewport_anchor = Anchor(0,0)

class FloorTile:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id

def render_map(tiles: list, anchor: Anchor, renderdistance: tuple) -> list:
    rendered_tiles = list()
    for tile in tiles:
        if math.fabs(anchor.x - (tile.x + .5)) <= renderdistance[0] and math.fabs(anchor.y - (tile.y + .5)) <= renderdistance[1]:
            rendered_tiles.append(tile)
    return rendered_tiles

def draw_view(tiles, anchor, viewsurface):
    for tile in tiles:
        x = (tile.x - anchor.x) * view_scale_factor 
        y = ((tile.y - anchor.y +1) * view_scale_factor) * -1
        p1 = (x + (viewport_width / 2), y + (viewport_height / 2))
        viewsurface.blit(FloorTile_sprite_map[tile.id], (p1))

def new_map(s):
    tiles = list()
    for x in range(s):
        for y in range(s):
            tiles.append(FloorTile(x, y, 0))
    return tiles

_map = new_map(100)
#--------------------------# CANVAS SIZE #--------------------------# 
canvas_size_text = myfont.render('Canvas Size', False, (0,0,0), None)

#--------------------------# EXPORT #--------------------------# 
exporttext = myfont.render('export', False, (255,255,255), None)


#--------------------------# MAIN #--------------------------# 
while True:

    display.fill((45,49,45))
    pg.draw.rect(display, (0,0,0), (viewport_x, viewport_y, viewport_width, viewport_height)) #viewport
    viewport_surface = pg.Surface((viewport_width, viewport_height), pg.SRCALPHA, 32)
    viewport_surface = viewport_surface.convert_alpha()
    
    draw_view(render_map(_map, viewport_anchor, view_render_distance), viewport_anchor, viewport_surface)
    display.blit(viewport_surface, (viewport_x, viewport_y))
    


    pg.draw.rect(display, (60,64,60), (selector_x, selector_y, selector_width, selector_height)) #selector
    display.blit(FloorTile_sprite_map[1], (sand_x, sand_y)) #sand in selector
    display.blit(FloorTile_sprite_map[2], (rock_x, rock_y)) #rock in selector
    display.blit(FloorTile_sprite_map[3], (dirt_x, dirt_y)) #dirt in selector
    display.blit(FloorTile_sprite_map[4], (grass_x, grass_y)) #grass in selector
    display.blit(FloorTile_sprite_map[5], (water_x, water_y))

    display.blit(selected_sprite, (selected_sprite_x, selected_sprite_y))


    pg.draw.rect(display, (120,130,120), (1702, 524, 184, 30)) # canvas size title
    display.blit(canvas_size_text, (1707, 529))
    pg.draw.rect(display, (90,94,90), (1702, 565, 50, 20)) #up button
    pg.draw.rect(display, (90,94,90), (1702, 595, 50, 20)) #down button



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

            if was_clicked(viewport_x, viewport_y, viewport_width, viewport_height) == True:
                for tile in _map:
                    x = (tile.x - viewport_anchor.x) * view_scale_factor
                    y = ((tile.y - viewport_anchor.y +1) * view_scale_factor) * -1
                    x, y = x + (viewport_width / 2) +64, y + (viewport_height / 2)+64
                    if was_clicked(x, y, 48, 48):
                        _map[_map.index(tile)].id = brush
    if keys[pg.K_ESCAPE]:
        pg.quit()
        sys.exit()



    # panning movement with wasd in viewport #
    if keys[pg.K_a]:
        viewport_anchor.x -= .4
    if keys[pg.K_d]:
        viewport_anchor.x += .4
    if keys[pg.K_w]:
        viewport_anchor.y += .4
    if keys[pg.K_s]:
        viewport_anchor.y -= .4
    # panning movement with wasd in viewport #

    pg.display.update()
    main_clock.tick(30)