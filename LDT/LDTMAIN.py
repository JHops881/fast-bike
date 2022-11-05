import pygame as pg
import math
import sys
import csv
pg.init()


main_clock = pg.time.Clock()

DARK = (20,30,20)
SEMI_DARK = (45,49,45)
SEMI_MID = (60,64,60)
MID = (90,94,90)
SEMI_LIGHT = (120,130,120)
LIGHT = (170,180,170)

#-----------------------------------# FONT #-----------------------------------# 
myfont = pg.font.Font('cour.ttf', 20)
myfont.bold = True

#---------------------------------# FUNCTIONS #--------------------------------# 

def mouse_pos_within(x: float, y: float, w: float, h: float) -> bool:
    '''
    Given the dimensions and location of a rectangular zone in screen space,
    returns a bool of whether or not the mouse cursor is whithin the zone's 
    bounds.

    Parameters:
    x (float): the x coordinate of the upper left corner of the zone
    y (float): the y coordinate of the upper left corner of the zone
    w (float): the width of the zone
    h (float): the height of the zone

    Returns:
    bool: whether or not the mouse postion is whithin the bounds of the zone
    '''
    mx, my = pg.mouse.get_pos()
    if x <= mx <= x+w and y <= my <= y+h:
        return True
    else:
        return False



#----------------------------------# DISPLAY #---------------------------------#
display_width = 1920
display_height = 1080
display = pg.display.set_mode((display_width, display_height))

#-------------------------------# SELECTOR #-----------------------------------# 
selected_sprite = pg.image.load('selected.png')
selected_sprite_x, selected_sprite_y = 1712, 74
brush = 1

FloorTile_sprite_map = {
    0: pg.transform.scale(pg.image.load('./textures/none.png'), (48,48)),
    1: pg.transform.scale(pg.image.load('./textures/sand.png'), (48,48)),
    2: pg.transform.scale(pg.image.load('./textures/rock.png'), (48,48)),
    3: pg.transform.scale(pg.image.load('./textures/dirt.png'), (48,48)),
    4: pg.transform.scale(pg.image.load('./textures/grass.png'), (48,48)),
    5: pg.transform.scale(pg.image.load('./textures/water.png'), (48,48)),
}

selector_width, selector_height = 184, 440
selector_x, selector_y = 1702, 64

sand_x, sand_y = 1712, 74 #the w and h are both 48
rock_x, rock_y = 1770, 74
dirt_x, dirt_y = 1828, 74
grass_x, grass_y = 1712, 132
water_x, water_y = 1770, 132



def draw_selector_block():
    pg.draw.rect(display, (SEMI_MID),
        (selector_x, selector_y, selector_width, selector_height)
    )
    display.blit(FloorTile_sprite_map[1], (sand_x, sand_y))
    display.blit(FloorTile_sprite_map[2], (rock_x, rock_y))
    display.blit(FloorTile_sprite_map[3], (dirt_x, dirt_y))
    display.blit(FloorTile_sprite_map[4], (grass_x, grass_y))
    display.blit(FloorTile_sprite_map[5], (water_x, water_y))

    display.blit(selected_sprite, (selected_sprite_x, selected_sprite_y))



#--------------------------------# VIEWPORT #----------------------------------#  
viewport_width, viewport_height = 1608, 952
viewport_x, viewport_y = 64, 64

view_scale_factor = 48


class Anchor:

    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

viewport_anchor = Anchor(0,0,.4)




class FloorTile:

    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id




class CeilingTile:

    def __init__(self, x, y, id, adjacent):
        self.x = x
        self.y = y
        self.id = id
        self.adjacent = adjacent




def visible_tiles(tiles: list, anchor: Anchor, renderdistance: tuple) -> list:
    visible_tiles_list = list()
    for tile in tiles:
        is_visible_x = (math.fabs(anchor.x - (tile.x +.5)) <= renderdistance[0])
        is_visible_y = (math.fabs(anchor.y - (tile.y +.5)) <= renderdistance[1])
        if is_visible_x and is_visible_y:
            visible_tiles_list.append(tile)
    return visible_tiles_list




def draw_view(tiles, anchor, viewsurface):
    for tile in tiles:
        x = (tile.x - anchor.x) * view_scale_factor
        y = ((tile.y - anchor.y +1) * view_scale_factor) * -1
        p1 = (x + (viewport_width / 2), y + (viewport_height / 2))
        t = pg.transform.scale(
            FloorTile_sprite_map[tile.id], (view_scale_factor,view_scale_factor)
        )
        viewsurface.blit(t, (p1))




def new_map(s:int) -> list:
    """
    Returns a new list of FloorTile Objects that are organized with
    coordinates such that 
    """
    s = math.floor(s)
    if s % 2 > 0:
        s-=1
    tiles = list()
    for x in range(int(-s/2), int(s/2)):
        for y in range(int(-s/2), int(s/2)):
            tiles.append(FloorTile(x, y, 0))
    return tiles


_map = new_map(100)

#-------------------------------# CANVAS SIZE #--------------------------------# 
canvas_size_title_x, canvas_size_title_y = 1702, 524
canvas_size_title_width, canvas_size_title_height = 184, 30

canvas_size_text = myfont.render('Canvas Size', False, DARK, None)
canvas_size_text_x, canvas_size_text_y = 1707, 529

canvas_size_up_x, canvas_size_up_y = 1702, 565
canvas_size_up_width, canvas_size_up_height = 50, 20
canvas_size_down_x, canvas_size_down_y = 1702, 595
canvas_size_down_width, canvas_size_down_height = 50, 20

canvas_size_num_title_x, canvas_size_num_title_y = 1762, 565
canvas_size_num_title_width, canvas_size_num_title_height = 70, 50



def draw_canvas_size_block():

    pg.draw.rect(display, SEMI_LIGHT,
        (canvas_size_title_x, canvas_size_title_y,
        canvas_size_title_width, canvas_size_title_height))

    display.blit(canvas_size_text, (canvas_size_text_x, canvas_size_text_y))

    pg.draw.rect(display, MID,
        (canvas_size_up_x, canvas_size_up_y,
        canvas_size_up_width, canvas_size_up_height))
        
    pg.draw.rect(display, MID,
        (canvas_size_down_x, canvas_size_down_y,
        canvas_size_down_width, canvas_size_down_height))

    pg.draw.rect(display, MID,
        (canvas_size_num_title_x, canvas_size_num_title_y,
        canvas_size_num_title_width, canvas_size_num_title_height))

#----------------------------------# EXPORT #----------------------------------# 
exporttext = myfont.render('Export', False, LIGHT, None)
export_x, export_y, export_width, export_height = 1702, 670, 94, 30




def draw_export_block():

    pg.draw.rect(display, DARK,
        (export_x, export_y, export_width, export_height))

    display.blit(exporttext,(export_x+5, export_y+5))



#-----------------------------------# MAIN #-----------------------------------#
while True: 
    #APPLICATION BACKGROUD COLOR
    display.fill(SEMI_DARK) 

    #VIEWPORT SURFACE INITIALIZING
    viewport_surface = pg.Surface((viewport_width,
        viewport_height))

    #INITIALIZING THE TILES THAT ARE VISIBLE IN THE VIEWPORT
    tiles_in_viewport = visible_tiles(_map, viewport_anchor,
        ((viewport_width/2)/view_scale_factor + 1,
        (viewport_height/2)/view_scale_factor + 1)) 

    #DRAWING VISIBLE TILES ON VIEWPORT
    draw_view(tiles_in_viewport, viewport_anchor, viewport_surface) 

    #DRAWING VIEWPORT ON DISPLAY
    display.blit(   
        viewport_surface, (viewport_x, viewport_y)) 
    

    draw_selector_block()
    draw_canvas_size_block()
    draw_export_block()


    mouse_x, mouse_y = pg.mouse.get_pos()
    keys = pg.key.get_pressed()


    if mouse_pos_within(viewport_x, viewport_y,
        viewport_width, viewport_height):

        # if the the mouse pos is within the viewport window,
        # the X and the y coordinate of the pointer will be displayed
        # on the top left above the viewport window.
        for tile in tiles_in_viewport:
            x = (tile.x - viewport_anchor.x) * view_scale_factor
            y = ((tile.y - viewport_anchor.y +1) * view_scale_factor) * -1
            x, y = x + (viewport_width / 2) +64, y + (viewport_height / 2)+64

            if mouse_pos_within(x, y, view_scale_factor, view_scale_factor):
                pos_text = 'X: ' + str(tile.x) + ' Y: ' + str(tile.y)

                display.blit((myfont.render(pos_text,
                    False, LIGHT, None)), (64, 20))





    for event in pg.event.get():
        
        #When the mouse is LEFT clicked... then
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            
            #if the mouse is within the bounds of the viewport... then
            if mouse_pos_within(viewport_x, viewport_y, 
                viewport_width, viewport_height): 
                
                # assigns the tile clicked an id corresponding to the one
                # selected (the image in the selector), id is stored in brush
                for tile in tiles_in_viewport:
                    x = (tile.x - viewport_anchor.x) * view_scale_factor
                    y = ((tile.y - viewport_anchor.y +1) *view_scale_factor) *-1
                    x = x + (viewport_width / 2) + 64
                    y = y + (viewport_height / 2) + 64

                    if mouse_pos_within(x, y,
                        view_scale_factor, view_scale_factor):

                        _map[_map.index(tile)].id = brush

            #if the mouse is within the bounds of the selector block... then
            elif mouse_pos_within(selector_x, selector_y,
                    selector_width, selector_height): 

                # if the mouse is within the bounds of the 
                # sand texture, select it.
                if mouse_pos_within(sand_x, sand_y, 48, 48):
                    selected_sprite_x, selected_sprite_y = sand_x-2, sand_y-2
                    brush = 1

                # if the mouse is within the bounds of the
                # rock texture, select it.
                elif mouse_pos_within(rock_x, rock_y, 48, 48):
                    selected_sprite_x, selected_sprite_y = rock_x-2, rock_y-2
                    brush = 2

                # if the mouse is within the bounds of the
                # dirt texture, select it. 
                elif mouse_pos_within(dirt_x, dirt_y, 48, 48):
                    selected_sprite_x, selected_sprite_y = dirt_x-2, dirt_y-2
                    brush = 3
                
                # if the mouse is within the bounds of the
                # grass texture, select it.
                elif mouse_pos_within(grass_x, grass_y, 48, 48):
                    selected_sprite_x, selected_sprite_y = grass_x-2, grass_y-2
                    brush = 4

                # if the mouse is within the bounds of the 
                # water texture, select it.
                elif mouse_pos_within(water_x, water_y, 48, 48):
                    selected_sprite_x, selected_sprite_y = water_x-2, water_y-2
                    brush = 5
            

            # if the mouse is within the bounds of the export button
            elif mouse_pos_within(export_x, export_y,
                export_width, export_height):

                with open('./output/export.csv', 'w') as file:
                    writer = csv.writer(file)
                    for tile in _map:
                        if tile.id != 0:
                            line = (tile.x,tile.y,tile.id)
                            writer.writerow(line)

                file.close()
                exporttext = myfont.render('Done.', False, LIGHT, None)


        #When the mouse is RIGHT clicked... then
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:

            #if the mouse is within the bounds of the viewport... then
            if mouse_pos_within(viewport_x, viewport_y,
                viewport_width, viewport_height):

                #assigns the tile to id 0 which is the none tile: a fancy
                #way of saying that the tile/texture is erased
                for tile in tiles_in_viewport:
                    x = (tile.x - viewport_anchor.x) * view_scale_factor
                    y = ((tile.y - viewport_anchor.y +1) *view_scale_factor) *-1
                    x = x + (viewport_width / 2) + 64
                    y = y + (viewport_height / 2) + 64

                    if mouse_pos_within(x, y,
                        view_scale_factor, view_scale_factor):

                        _map[_map.index(tile)].id = 0



        elif event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    if keys[pg.K_ESCAPE]:
        pg.quit()
        sys.exit()



    # panning movement with wasd in viewport
    if keys[pg.K_a]:
        viewport_anchor.x -= viewport_anchor.speed
    if keys[pg.K_d]:
        viewport_anchor.x += viewport_anchor.speed
    if keys[pg.K_w]:
        viewport_anchor.y += viewport_anchor.speed
    if keys[pg.K_s]:
        viewport_anchor.y -= viewport_anchor.speed
    
    #zooming in and out with the up and down arrow keys
    if keys[pg.K_UP]:
        view_scale_factor += 1
    if keys[pg.K_DOWN]:
        view_scale_factor -= 1
    

    pg.display.update()
    main_clock.tick(30)