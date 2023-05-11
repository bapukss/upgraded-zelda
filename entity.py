import pygame as pg
from math import sin

class Entity(pg.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 7
        self.direction = pg.math.Vector2()

    def move(self, speed, dt):
        self.old_rect = self.hitbox.copy()
        if self.direction.magnitude() !=0:
            self.direction = self.direction.normalize()

        self.pos_dt.x = self.direction.x * speed * dt
        self.hitbox.x += round(self.pos_dt.x)
        self.collision("horizontal")
        self.pos_dt.y = self.direction.y * speed * dt
        self.hitbox.y += round(self.pos_dt.y)
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def wave_value(self):
        value = sin(pg.time.get_ticks())
        if value >= 0: return 255
        else: return 0
