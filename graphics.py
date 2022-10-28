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

floor_surface_width = 1920
floor_surface_height = 1080




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




#wall ^
#+--------------------------------------------------+#| CEILING TILE |#+-------------------------------------------------+#
class CeilingTile:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite





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
