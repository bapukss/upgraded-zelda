import pygame as pg
from settings import *

class Weapon(pg.sprite.Sprite):
    def __init__(self, player, groups, z=LAYERS["main"]):
        super().__init__(groups)
        self.sprite_type = "weapon"
        direction = player.status.split("_")[0]
        self.z = z
        #graphic
        full_path = f"..\\zelda\\maskedninja\\graphics\\weapons\\{player.weapon}/{direction}.png"
        self.image = pg.image.load(full_path).convert_alpha()

        #placement
        if direction == "right":
            self.rect = self.image.get_rect(midleft=player.rect.midright+pg.math.Vector2(0,16))
        elif direction == "left":
            self.rect = self.image.get_rect(midright=player.rect.midleft + pg.math.Vector2(0, 16))
        elif direction == "down":
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pg.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop+pg.math.Vector2(-10, 0))
