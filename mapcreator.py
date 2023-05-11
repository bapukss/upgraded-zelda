import pygame as pg
from settings import *

class MapCreator(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS["main"]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-40,-10) ######-40,-10
        self.old_rect = self.hitbox.copy()

class Decorations(MapCreator):
    def __init__(self, pos, surf, groups, name, sprite_type="object"):
        super().__init__(pos,surf,groups)
        self.hitbox = self.rect.copy().inflate(-20,-self.rect.height*0.9) ####-20,-self.rect.height*0.9
        self.sprite_type = sprite_type
        self.old_rect = self.hitbox.copy()

class Trees(MapCreator):
    def __init__(self, pos, surf, groups,name):
        super().__init__(pos,surf,groups)
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75) #-self.rect.width * 0.2, -self.rect.height * 0.75
        self.old_rect = self.hitbox.copy()
