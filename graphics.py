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




class Drawable:

    def __init__(self, x:float, y:float, id:int,):
        self.x = x
        self.y = y
        self.id = id

    def is_visible(self):
        pass

    def draw(self):
        pass




class Player(Drawable):

    class Stats:

        def __init__(self, movespeed:float, health:int):
            self.movespeed = movespeed
            self.health = health

    class Inventory:

        def __init__(self, stored:list, hotbar:list):
            self.stored = stored
            self.hotbar = hotbar

    def __init__(self, x:float, y:float, id:int, width:int, height:int, theta:int,
    rotspeed:int, movespeed:float, health:int, stored:list, hotbar:list):
        super().__init__(x, y, id)
        self.width = width
        self.height = height
        self.theta = theta
        self.rotspeed = rotspeed
        self.stats = self.Stats(movespeed, health)
        self.inventory = self.Inventory(stored, hotbar)

    def draw(self, display:pg.display) -> None:
        """
        Draws the player in the center of the screen.

        Parameters:
        player (data.Player): desired player object to be drawn
        display (pg.display): The display that the player is to be drawn on
    
        Returns:
        None
        """
        pg.draw.rect(display, GREEN, ((display.get_width() - self.width) / 2,
        (display.get_height() - self.height) / 2, self.width, self.height))

    def constrain_theta(self):
        if self.theta != 360 and self.theta != -2:
            pass
        elif self.theta == 360:
            self.theta = 0
        elif self.theta == -2:
            self.theta = 358
        else:
            pass




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




floortile_sprite_map = {
    1: pg.transform.scale(pg.image.load('./Sprites/FloorTile/grass.png'), (48,48))
}
class FloorTile(Drawable):

    def generate_map(r: int) -> list:
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

    def is_visible(self, player: Player, renderdistance: int) -> bool:
        if (((self.x + .5) - player.x)**2 + ((self.y + .5) - player.y)**2) < renderdistance:
            return True
        else:
            return False

    def draw(self, player: Player, surface: pg.surface, scalefactor) -> None:
        x = (self.x - player.x) * scalefactor 
        y = ((self.y - player.y + 1) * scalefactor) * -1
        p1 = (x + (surface.get_width() / 2), y + (surface.get_height() / 2))
        surface.blit(floortile_sprite_map[self.id], p1)




ceilingtile_sprite_map = {
    1: pg.image.load('./Sprites/CeilingTile/none.png')
}
class CeilingTile(Drawable):

    def __init__(self, x: float, y: float, id: int, adjacent: tuple):
        super().__init__(x, y, id)
        self.adjacent = adjacent

    def is_visible(self, player: Player, renderdistance: int):
        if (((self.x + .5) - player.x)**2 + ((self.y + .5) - player.y)**2) < renderdistance:  
            return True
        else:
            return False

    def draw(self, player: Player, surface: pg.surface, scalefactor, offset) -> None:
        x = (self.x - player.x) * scalefactor + _rotate(player.theta, (0,offset))[0]
        y = ((self.y - player.y + 1) * scalefactor) * -1 - _rotate(player.theta, (0,offset))[1]
        p1 = (x + (surface.get_width() / 2), y + (surface.get_height() / 2))
        surface.blit(ceilingtile_sprite_map[self.id], p1)

    def draw_walls(self, player: Player, surface: pg.surface, scalefactor, offset) -> None:
        if self.adjacent != (True,True,True,True):
            # --- # SOUTH SIDE # --- #
            #BOTOM LEFT OF CEIL
            x1s = (self.x - player.x) * scalefactor + _rotate(player.theta, (0,offset))[0]
            y1s = ((self.y - player.y + 1) * scalefactor) * -1 - _rotate(player.theta, (0,offset))[1]
            p1s = (x1s + (surface.get_width() / 2), y1s + (surface.get_height() / 2)+scalefactor)
            #BOTTOM RIGHT OF CEIL
            p2s = (p1s[0]+scalefactor, p1s[1])
            #BOTTOM LEFT OF FLOOR
            x4s = (self.x - player.x) * scalefactor 
            y4s = ((self.y - player.y + 1) * scalefactor) * -1
            p4s = (x4s + (surface.get_width() / 2), y4s + (surface.get_height() / 2)+scalefactor)
            #BORROM RIGHT OF FLOOR
            p3s = (p4s[0]+scalefactor, p4s[1])

            # --- # EAST SIDE # --- #
            #BRoC
            p1e = p2s
            #TRoC
            p2e = (p1e[0], p1e[1]-scalefactor)
            #TRoF
            p3e = (p3s[0], p3s[1]-scalefactor)
            #BRoF
            p4e = p3s

            # --- # NORTH SIDE # --- #
            #TRoC
            p1n = p2e
            #TLoC
            p2n = (p2e[0]-scalefactor, p2e[1])
            #TLoF
            p3n = (p3e[0]-scalefactor, p3e[1])
            #TRoF
            p4n = p3e

            # --- # WEST SIDE # --- #
            p1w = p2n
            p2w = p1s
            p3w = p4s
            p4w = p3n

            if player.theta == 0:
                if self.adjacent[2] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (105,85,85), (p1s,p2s,p3s,p4s)) #SOUTH DRAW

            elif 0 < player.theta < 90:
                if self.adjacent[2] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (105,85,85), (p1s,p2s,p3s,p4s)) #SOUTH DRAW
                if self.adjacent[1] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (85,65,65), (p1e,p2e,p3e,p4e)) #EAST DRAW

            elif player.theta == 90:
                if self.adjacent[1] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (85,65,65), (p1e,p2e,p3e,p4e)) #EAST DRAW

            elif 90 < player.theta < 180:
                if self.adjacent[1] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (85,65,65), (p1e,p2e,p3e,p4e)) #EAST DRAW
                if self.adjacent[0] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (145,125,125), (p1n,p2n,p3n,p4n)) #NORTH DRAW

            elif player.theta == 180:
                if self.adjacent[0] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (145,125,125), (p1n,p2n,p3n,p4n)) #NORTH DRAW

            elif 180 < player.theta < 270:
                if self.adjacent[0] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (145,125,125), (p1n,p2n,p3n,p4n)) #NORTH DRAW
                if self.adjacent[3] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (125,105,105), (p1w,p2w,p3w,p4w)) #WEST DRAW

            elif player.theta == 270:
                if self.adjacent[3] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (125,105,105), (p1w,p2w,p3w,p4w)) #WEST DRAW

            elif 270 < player.theta < 360:
                if self.adjacent[3] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (125,105,105), (p1w,p2w,p3w,p4w)) #WEST DRAW
                if self.adjacent[2] == True:
                    pass
                else:
                    pg.draw.polygon(surface, (105,85,85), (p1s,p2s,p3s,p4s)) #SOUTH DRAW




terrain_sprite_map = {
    1: pg.image.load("./Sprites/Environment/cactus.png")
}
class Terrain(Drawable):

    def is_visible(self, player: Player, renderdistance: int):
        if (((self.x + .5) - player.x)**2 + ((self.y + .5) - player.y)**2) < renderdistance:
            return True
        else:
            return False

    def draw(self, player, display: pg.display, scalefactor: int) -> None:
        x = (self.x - player.x) * scalefactor
        y = ((self.y - player.y + 1) * scalefactor) * -1
        x, y = _rotate(player.theta, (x,y))
        x -= (terrain_sprite_map[self.id].get_width() / 2)
        y -= terrain_sprite_map[self.id].get_height()
        p1 = (x + (display.get_width() / 2), y + (display.get_height() / 2))
        display.blit(terrain_sprite_map[self.id], p1)




class Particle(Drawable):
    pass




class Projectile(Drawable):
    def __init__(self, x: float, y: float, id: int, theta: int):
        super().__init__(x, y, id)
        self.theta = theta


# GUI Section ---------------------------------------------------------------------------------------------------------

healthbar = pg.image.load('./Sprites/GUI/healthbar100.png')

class GUIElement:

    def __init__(self, player, disx, disy, image, display, scale:tuple):
        self.player = player
        self.disx = disx
        self.disy = disy
        self.image = image
        self.display = display
        self.scale = scale
    
    def draw(self):
        self.display.blit(pg.transform.scale((self.image), self.scale), (self.disx, self.disy))




class GUIHealthBar(GUIElement):

    def draw(self):
        super().draw()
