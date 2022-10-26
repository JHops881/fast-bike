
from smtplib import SMTPRecipientsRefused
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




def draw_player(player: data.Player, display: pg.display) -> None:
    """
    Draws the player in the center of the screen.

    Parameters:
    player (data.Player): desired player object to be drawn
    display (pg.display): The display that the player is to be drawn on
    
    Returns:
    None
    """
    pg.draw.rect(display, data.GREEN, ((data.main_display_width - player.width) / 2, (data.main_display_height - player.height) / 2, player.width, player.height))




def generate_FloorTiles(r: int) -> list:
    """
    For a given radius (r), a list of data.FloorTile objects is returned. The data.FloorTile objects are arranged
    at coordinates such that they from a square with the given "radius".

    Parameters:
    r (int): a radius that the user desired the square to have. Note that the radius should be passed in as squared value of
        what the user desired the true radius of the square of data.FloorTile objects to be. For example, if the user desires the 
        square of data.FloorTile objects to have a radius of 8 data.FloorTile objects, the user should pass in 64 for r.

    Returns:
    tiles (list(data.FloorTile)): list of data.FloorTile obejects that are in a square. The data.FloorTile obejects are centered around (0,0)
    """
    tiles = list()
    for y in range(r, -r, -1):
        for x in range(-r, r, 1):
            tiles.append(data.FloorTile(x, y, data.floor_tile_sprite))
    return tiles




def render_FloorTiles(player: data.Player, renderdistance: int, tiles: list) -> list:
    """
    Based on a player's (player) postion, render distance (renderdistance), and a list of all data.FloorTile objects loaded (tiles),
    a list of data.FloorTile objects is returned with same objects organized coordinately such that they form a circle around the player.
    Obviously, this circle of data.FloorTile objects has a radius that is roughly equal to the render distance.

    Parameters:
    player (data.Player): a player that the user desires to render the data.FloorTile objects about
    renderdistance (int): the radius in data.FloorTile units (1 unit = 1 data.FloorTile) that the user wishes to render data.FloorTile objects within
    tiles (list(data.FloorTile)): a list of all loaded data.FloorTile objects that will be iterated through to determine the render data.FloorTile objects

    Returns:
    _rendered_tiles (list(data.FloorTile)): a list of data.FloorTile objects organized coordinately such that they form a circle around
        the player's (x,y) postion with a radius equal to renderdistance.
    """
    _rendered_tiles = list()
    for tile in tiles:
        if (((tile.x + .5) - player.x)**2 + ((tile.y + .5) - player.y)**2) < renderdistance:
            _rendered_tiles.append(tile)
    return _rendered_tiles




#TODO: Redo documentation 
def draw_FloorTiles(tiles: list, player: data.Player, surface: pg.surface) -> None:
    """
    Draws list of data.FloorTile objects onto the surface. The data.FloorTile objects are drawn in screen space 
    such that they accuractely portray their postion relative to the player position.

    Paramters:
    tiles (list(data.FloorTile)): a list of data.FloorTile objects that are going to be drawn onto the surface
    player (data.Player): a data.Player that the user desires to the data.FloorTile objects to be drawn relative to
    surface (pg.surface): a pg.surface that the user wishes to draw the data.FloorTile objects onto
    """
    for tile in tiles:
        x = (tile.x - player.x) * data.main_scale_factor 
        y = ((tile.y - player.y + 1) * data.main_scale_factor) * -1
        p1 = (x + (data.main_display_width / 2), y + (data.main_display_height / 2))
        surface.blit(tile.texture, p1)


all_FloorTiles = generate_FloorTiles(data.map_radius)






def draw_PassiveSprites(player, sprites, display):
    for sprite in sprites:
        x = (sprite.x - player.x) * data.main_scale_factor 
        y = ((sprite.y - player.y + 1) * data.main_scale_factor) * -1
        p1 = (x + (data.main_display_width / 2), y + (data.main_display_height / 2))
        display.blit(sprite.sprite, p1)




def render_PassiveSprite(player: data.Player, renderdistance: int, sprites: list) -> list:
    _rendered_sprites = list()
    for sprite in sprites:
        if (((sprite.x + .5) - player.x)**2 + ((sprite.y + .5) - player.y)**2) < renderdistance:
            _rendered_sprites.append(sprite)
    return _rendered_sprites





def draw_health(player: data.Player, display: pg.display) -> None:
    gfx.aapolygon(display, ((20, 20),(220, 20),(220, 60), (20, 60)), data.RED)
    x_offset = 0
    for hp in range(player.health + 1):
        pg.draw.rect(display, data.RED, (20 + x_offset, 20, 2, 40))
        x_offset = hp * 2