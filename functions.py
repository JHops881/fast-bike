
import pygame as pg 
import numpy as np
import math
import pygame.gfxdraw as gfx
import data
pg.init()



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



def _draw(tile: data.Tile, player: data.Player, display: pg.display) -> None:
    w = math.fabs(tile.x2 - tile.x1) * data.main_scale_factor
    h = math.fabs(tile.y2 - tile.y1) * data.main_scale_factor
    x = (tile.x1 - player.x) * data.main_scale_factor 
    y = ((tile.y1 - player.y) * data.main_scale_factor) * -1 
    p1 = _rotate(player.theta, (x,y))
    p1 = (p1[0] + (data.main_display_width / 2), p1[1] + (data.main_display_height / 2))
    p2 = _rotate(player.theta, (x+w,y))
    p2 = (p2[0] + (data.main_display_width / 2), p2[1] + (data.main_display_height / 2))
    p3 = _rotate(player.theta, (x+w, y+h))
    p3 = (p3[0] + (data.main_display_width / 2), p3[1] + (data.main_display_height / 2))
    p4 = _rotate(player.theta, (x, y+h))
    p4 = (p4[0] + (data.main_display_width / 2), p4[1] + (data.main_display_height / 2))
    pg.draw.polygon(display, tile.color, (p1, p2, p3, p4))
    #gfx.aapolygon(display, (p1, p2, p3, p4), RED)




def draw_tiles(tiles, player, display):
    for tile in tiles:
        _draw(tile, player, display)




def draw_player(player: data.Player, display: pg.display) -> None:
    """
    Draws the player in the center of the screen.

    Parameters:
    player (data.Player): desired player object to be drawn
    display (pg.display): The display that the player is to be drawn on
    
    Returns:
    None
    """
    pg.draw.rect(display, data.WHITE, ((data.main_display_width - player.width) / 2, (data.main_display_height - player.height) / 2, player.width, player.height))





def generate_tiles(r: int) -> list:
    """
    For a given radius (r), a list of data.Tile objects is returned. The data.Tile objects are arranged
    at coordinates such that they form a square with the given radius.

    Parameters:
    r (int): a radius that the user desired the square to have. Note that the radius should be passed in as squared value of
        what the user desired the raius of the square of data.Tile objects to be. For example, if the user desires the 
        square of data.Tile objects to have a radius of 8 data.Tile objects, the user should pass in 64 for r.

    Returns:
    tiles (list(data.Tile)): list of data.Tile obejects that are in a square. The data.Tile obejects are centered around (0,0)
    """
    tiles = list()
    for y in range(r, -r, -1):
        for x in range(-r, r, 1):
            tiles.append(data.Tile(x, y, (x + 1), (y - 1), data.GRAY))
    return tiles




all_tiles = generate_tiles(data.map_radius)




def render_tiles(player: data.Player, renderdistance: int, tiles: list) -> list:
    """
    Based on a player's (player) postion, render distance (renderdistance), and a list of all data.Tile objects loaded (tiles),
    a list of data.Tile objects is returned with same objects organized coordinately such that they form a circle around the player.
    Obviously, this circle of data.Tile objects has a radius that is roughly equal to the render distance.

    Parameters:
    player (data.Player): a player that the user desires to render the data.Tile objects about
    renderdistance (int): the radius in data.Tile units (1 unit = 1 data.Tile) that the user wishes to render data.Tile objects within
    tiles (list(data.Tile)): a list of all loaded data.Tile objects that will be iterated through to determine the redner data.Tile objects

    Returns:
    _rendered_tiles (list(data.Tile)): a list of data.Tile objects organized coordinately such that they form a circle around
        the player's (x,y) postion with a radius equal to renderdistance. 
    """
    _rendered_tiles = []
    for tile in tiles:
        if ((((tile.x1 + tile.x2) / 2) - player.x)**2 + (((tile.y1 + tile.y2) / 2) - player.y)**2) < renderdistance:
            _rendered_tiles.append(tile)
    return _rendered_tiles




def draw_health(player: data.Player, display: pg.display) -> None:
    gfx.aapolygon(display, ((20, 20),(220, 20),(220, 60), (20, 60)), data.RED)
    x_offset = 0
    for hp in range(player.health + 1):
        pg.draw.rect(display, data.RED, (20 + x_offset, 20, 2, 40))
        x_offset = hp * 2