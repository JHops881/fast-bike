import pygame as pg
import math
import numpy as np
import pygame.gfxdraw as gfx
pg.init()




#                                 ------------ TABLE OF CONTENTS ------------
#                                       ORDER:                    SUBJECT:

#                                       1                         colors
#                                       2                         misc
#                                       3                         functions
#                                       4                         player
#                                       5                         floortile
#                                       6                         wall
#                                       7                         ceilingtile
#                                       8                         terrain
#                                       9                         particle
#                                       10                        projectile
#                                       11                        gui





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




main_display_width = 1920
main_display_height = 1080
main_display = pg.display.set_mode((main_display_width, main_display_height))

main_clock = pg.time.Clock()



map_radius = 20
main_scale_factor = 48
render_distance = 100

tile_surface_width = 1920
tile_surface_height = 1080




def _rotate(theta: float, v: tuple) -> tuple:
    """
    Given a vector (v) and an angle in degrees (theta),
    a vector is returned that has been rotated by the angle.

    Parameters:
    theta (float): angle in degrees
    v (tuple(float, float)): vector

    Returns:
    tuple(float, float): rotated vector of v by theta degrees
    """
    assert v != None and len(v) == 2, "invalid v input"

    theta = math.radians(theta) # Angle is converted from degrees to radians so it is usable by math module's trig functions             
    A = math.cos(theta) * v[0] - math.sin(theta) * v[1]
    B = math.sin(theta) * v[0] + math.cos(theta) * v[1]
    return (A, B)



#+--------------------------------------------------+#| PLAYER |#+-------------------------------------------------+#
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


def draw_player(player: Player, display: pg.display) -> None:
    """
    Draws the player in the center of the screen.

    Parameters:
    player (data.Player): desired player object to be drawn
    display (pg.display): The display that the player is to be drawn on
    
    Returns:
    None
    """
    pg.draw.rect(display, GREEN, ((main_display_width - player.width) / 2, (main_display_height - player.height) / 2, player.width, player.height))




def supervised_player_theta(player):
    if player.theta == 360:
        new_theta = 0
        return new_theta
    elif player.theta == -2:
        new_theta = 358
        return new_theta
    else:
        return player.theta



main_player = Player(0, 0, 32, 32, 0, (1/15), 2, 67)







#player ^
#+--------------------------------------------------+#| FLOOR TILE |#+-------------------------------------------------+#

FloorTile_sprite_map = {
    1: pg.image.load('./Sprites/FloorTile/sand.png')
}


class FloorTile:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id




def generate_FloorTiles(r: int) -> list:
    """
    For a given radius (r), a list of FloorTile objects is returned. The FloorTile objects are arranged
    at coordinates such that they from a square with the given "radius".

    Parameters:
    r (int): a radius that the user desired the square to have. Note that the radius should be passed in as squared value of
        what the user desired the true radius of the square of FloorTile objects to be. For example, if the user desires the 
        square of FloorTile objects to have a radius of 8 FloorTile objects, the user should pass in 64 for r.

    Returns:
    tiles (list(FloorTile)): list of FloorTile obejects that are in a square. The FloorTile obejects are centered around (0,0)
    """
    tiles = list()
    for y in range(r, -r, -1):
        for x in range(-r, r, 1):
            tiles.append(FloorTile(x, y, 1))
    return tiles




def render_FloorTiles(player: Player, renderdistance: int, tiles: list) -> list:
    """
    Based on a player's (player) postion, render distance (renderdistance), and a list of all FloorTile objects loaded (tiles),
    a list of FloorTile objects is returned with same objects organized coordinately such that they form a circle around the player.
    Obviously, this circle of FloorTile objects has a radius that is roughly equal to the render distance.

    Parameters:
    player (Player): a player that the user desires to render the FloorTile objects about
    renderdistance (int): the radius in FloorTile units (1 unit = 1 FloorTile) that the user wishes to render FloorTile objects within
    tiles (list(FloorTile)): a list of all loaded FloorTile objects that will be iterated through to determine the render FloorTile objects

    Returns:
    _rendered_tiles (list(FloorTile)): a list of FloorTile objects organized coordinately such that they form a circle around
        the player's (x,y) postion with a radius equal to renderdistance.
    """
    _rendered_tiles = list()
    for tile in tiles:
        if (((tile.x + .5) - player.x)**2 + ((tile.y + .5) - player.y)**2) < renderdistance:
            _rendered_tiles.append(tile)
    return _rendered_tiles




def draw_FloorTiles(tiles: list, player: Player, surface: pg.surface) -> None:
    """
    Draws list of FloorTile objects onto the surface. The FloorTile objects are drawn in screen space 
    such that they accuractely portray their postion relative to the player position.

    Paramters:
    tiles (list(FloorTile)): a list of FloorTile objects that are going to be drawn onto the surface
    player (Player): a Player that the user desires to the FloorTile objects to be drawn relative to
    surface (pg.surface): a pg.surface that the user wishes to draw the FloorTile objects onto

    Returns:
    None
    """
    for tile in tiles:
        x = (tile.x - player.x) * main_scale_factor 
        y = ((tile.y - player.y + 1) * main_scale_factor) * -1
        p1 = (x + (main_display_width / 2), y + (main_display_height / 2))
        surface.blit(FloorTile_sprite_map[tile.id], p1)




def rotate_surface(player: Player, surface: pg.surface, display: pg.display) -> None:
    """
    Rotates a pg.surface (surface) based on a Player's (player) angle: stored in Player.theta. The surface is rotated from the
    center point of itself. It is then blit onto a pg.display (display) such that the centerpoint of the surface and the display
    overlap.

    Parameters:
    player (Player): The Player that the user wishes to derive the angle in which the surface is rotated from.
    surface (pg.surface): The pg.surface that the user desires to rotate and blit
    display (pg.display): The pg.display that the user wishes to have the rotated pg.surface blit onto

    Returns:
    None
    """
    s = surface.get_rect()
    rotated_surface = pg.transform.rotate(surface, -player.theta)
    r = rotated_surface.get_rect()
    display.blit(rotated_surface, (0 - (r.centerx - s.centerx), 0 - (r.centery - s.centery)))




all_FloorTiles = generate_FloorTiles(map_radius)





#floor tile ^
#+--------------------------------------------------+#| WALL |#+-------------------------------------------------+#
class Wall:
    def __init__(self, x1, y1, x2, y2, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color

def draw_Walls(tiles: list, player: Player, surface: pg.surface) -> None:
    for ceil in tiles:

        # --- # SOUTH SIDE # --- #
        #BOTOM LEFT OF CEIL
        x1s = (ceil.x - player.x) * main_scale_factor + _rotate(player.theta, (0,offset))[0]
        y1s = ((ceil.y - player.y + 1) * main_scale_factor) * -1 - _rotate(player.theta, (0,offset))[1]
        p1s = (x1s + (main_display_width / 2), y1s + (main_display_height / 2)+main_scale_factor)
        #BOTTOM RIGHT OF CEIL
        p2s = (p1s[0]+main_scale_factor, p1s[1])
        #BOTTOM LEFT OF FLOOR
        x4s = (ceil.x - player.x) * main_scale_factor 
        y4s = ((ceil.y - player.y + 1) * main_scale_factor) * -1
        p4s = (x4s + (main_display_width / 2), y4s + (main_display_height / 2)+main_scale_factor)
        #BORROM RIGHT OF FLOOR
        p3s = (p4s[0]+main_scale_factor, p4s[1])
        # --- # SOUTH SIDE # --- #
        

        # --- # EAST SIDE # --- #
        #BRoC
        p1e = p2s
        #TRoC
        p2e = (p1e[0], p1e[1]-main_scale_factor)
        #TRoF
        p3e = (p3s[0], p3s[1]-main_scale_factor)
        #BRoF
        p4e = p3s
        # --- # EAST SIDE # --- #


        # --- # NORTH SIDE # --- #
        #TRoC
        p1n = p2e
        #TLoC
        p2n = (p2e[0]-main_scale_factor, p2e[1])
        #TLoF
        p3n = (p3e[0]-main_scale_factor, p3e[1])
        #TRoF
        p4n = p3e
        # --- # NORTH SIDE # --- #


        # --- # WEST SIDE # --- #
        p1w = p2n
        p2w = p1s
        p3w = p4s
        p4w = p3n

        # --- # WEST SIDE # --- #
        if player.theta == 0:
            pg.draw.polygon(surface, (105,85,85), (p1s,p2s,p3s,p4s)) #SOUTH DRAW
        elif 0 < player.theta < 90:
            pg.draw.polygon(surface, (105,85,85), (p1s,p2s,p3s,p4s)) #SOUTH DRAW
            pg.draw.polygon(surface, (85,65,65), (p1e,p2e,p3e,p4e)) #EAST DRAW
        elif player.theta == 90:
            pg.draw.polygon(surface, (85,65,65), (p1e,p2e,p3e,p4e)) #EAST DRAW
        elif 90 < player.theta < 180:
            pg.draw.polygon(surface, (85,65,65), (p1e,p2e,p3e,p4e)) #EAST DRAW
            pg.draw.polygon(surface, (145,125,125), (p1n,p2n,p3n,p4n)) #NORTH DRAW
        elif player.theta == 180:
            pg.draw.polygon(surface, (145,125,125), (p1n,p2n,p3n,p4n)) #NORTH DRAW
        elif 180 < player.theta < 270:
            pg.draw.polygon(surface, (145,125,125), (p1n,p2n,p3n,p4n)) #NORTH DRAW
            pg.draw.polygon(surface, (125,105,105), (p1w,p2w,p3w,p4w)) #WEST DRAW
        elif player.theta == 270:
            pg.draw.polygon(surface, (125,105,105), (p1w,p2w,p3w,p4w)) #WEST DRAW
        elif 270 < player.theta < 360:
            pg.draw.polygon(surface, (125,105,105), (p1w,p2w,p3w,p4w)) #WEST DRAW
            pg.draw.polygon(surface, (105,85,85), (p1s,p2s,p3s,p4s)) #SOUTH DRAW

        

#wall ^
#+--------------------------------------------------+#| CEILING TILE |#+-------------------------------------------------+#

offset = 36
CeilingTile_sprite_map = {
    1: pg.image.load('./Sprites/CeilingTile/none.png')
}


class CeilingTile:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id




def render_CeilingTiles(player: Player, renderdistance: int, tiles: list) -> list:
    """
    Based on a player's (player) postion, render distance (renderdistance), and a list of all CeilingTile objects loaded (tiles),
    a list of CeilingTile objects is returned with same objects organized coordinately such that they form a circle around the player.
    Obviously, this circle of CeilingTile objects has a radius that is roughly equal to the render distance.

    Parameters:
    player (Player): a player that the user desires to render the CeilingTile objects about
    renderdistance (int): the radius in CeilingTile units (1 unit = 1 CeilingTile) that the user wishes to render CeilingTile objects within
    tiles (list(CeilingTile)): a list of all loaded CeilingTile objects that will be iterated through to determine the render CeilingTile objects

    Returns:
    _rendered_tiles (list(CeilingTile)): a list of CeilingTile objects organized coordinately such that they form a circle around
        the player's (x,y) postion with a radius equal to renderdistance.
    """
    _rendered_tiles = list()
    for tile in tiles:
        if (((tile.x + .5) - player.x)**2 + ((tile.y + .5) - player.y)**2) < renderdistance:
            _rendered_tiles.append(tile)
    return _rendered_tiles




def draw_CeilingTiles(tiles: list, player: Player, surface: pg.surface) -> None:
    """
    Draws list of CeilingTile objects onto the surface. The CeilingTile objects are drawn in screen space 
    such that they accuractely portray their postion relative to the player position with a small offset to
    give perspective.

    Paramters:
    tiles (list(CeilingTile)): a list of CeilingTile objects that are going to be drawn onto the surface
    player (Player): a Player that the user desires to the CeilingTile objects to be drawn relative to
    surface (pg.surface): a pg.surface that the user wishes to draw the CeilingTile objects onto

    Returns:
    None
    """
    for tile in tiles:

        x = (tile.x - player.x) * main_scale_factor + _rotate(player.theta, (0,offset))[0]
        y = ((tile.y - player.y + 1) * main_scale_factor) * -1 - _rotate(player.theta, (0,offset))[1]
        p1 = (x + (main_display_width / 2), y + (main_display_height / 2))
        surface.blit(CeilingTile_sprite_map[tile.id], p1)

testtile = [CeilingTile(-9, 7, 1), CeilingTile(-9, 5, 1), CeilingTile(9, 5, 1)]

#ceiling tile ^
#+--------------------------------------------------+#| TERRAIN |#+-------------------------------------------------+#
cactus = pg.image.load("./Sprites/Environment/cactus.png")




class Terrain:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite




def draw_Terrain(player: Player, terrains: list, display: pg.display) -> None:
    """
    For a given list of Terrain (terrains), the sprite for each Terrain object is blit onto the pg.display (display)
    correctly relative to the Player (player).

    Parameters:
    player (Player): The player that the Terrain object sprites are to be drawn relative to.
    terrains (list(Terrain)): A list of Terrain objects that the user desires to have sprites blit for
    display (pg.display): the pg.display that the sprites will be blit onto

    Returns:
    None
    """
    for terrain in terrains:
        x = (terrain.x - player.x) * main_scale_factor
        y = ((terrain.y - player.y + 1) * main_scale_factor) * -1
        x, y = _rotate(player.theta, (x,y))
        x -= 48
        y -= 96
        p1 = (x + (main_display_width / 2), y + (main_display_height / 2))
        display.blit(terrain.sprite, p1)



#TODO: doctstring 
def render_Terrain(player: Player, renderdistance: int, terrains: list) -> list:
    _rendered_terrains = list()
    for terrain in terrains:
        if (((terrain.x + .5) - player.x)**2 + ((terrain.y + .5) - player.y)**2) < renderdistance:
            _rendered_terrains.append(terrain)
    return _rendered_terrains



ts = Terrain(4, -2, cactus)
all_Terrain = [ts]





#terrain ^
#+--------------------------------------------------+#| PARTICLE |#+-------------------------------------------------+#
class Particle:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite





#particle ^
#+--------------------------------------------------+#| PROJECTILE |#+-------------------------------------------------+#
class Particle:
    def __init__(self, x, y, sprite, theta):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.theta = theta




#projectile ^
#+--------------------------------------------------+#| GUI |#+-------------------------------------------------+#
def draw_health(player: Player, display: pg.display) -> None:
    gfx.aapolygon(display, ((20, 20),(220, 20),(220, 60), (20, 60)), RED)
    x_offset = 0
    for hp in range(player.health + 1):
        pg.draw.rect(display, RED, (20 + x_offset, 20, 2, 40))
        x_offset = hp * 2
