import pygame as pg

import settings
from support import import_folder
from random import choice
from settings import *

class AnimationPlayer():
    def __init__(self):
        self.frames = {
            # magic
            'flame': import_folder('..\\zelda\\maskedninja\\graphics\\particles\\flame\\frames'),
            'aura': import_folder('..\\zelda\\maskedninja\\graphics\\particles\\aura'),
            'heal': import_folder('..\\zelda\\maskedninja\\graphics\\particles\\heal\\frames'),

            # attacks
            'claw': import_folder('..\\zelda\\maskedninja\\graphics\\particles\\claw'),
            'slash': import_folder('..\\zelda\\maskedninja\\graphics\\particles\\slash'),
            'sparkle': import_folder('..\\zelda\\maskedninja\\graphics\\particles\\sparkle'),
            'leaf_attack': import_folder('..\\zelda\\maskedninja\\graphics\\particles\\leaf_attack'),
            'thunder': import_folder('..\\zelda\\maskedninja\\graphics\\particles\\thunder'),

            # monster deaths
            'squid': import_folder('..\\zelda\\maskedninja\\graphics\\particles\\smoke_orange'),
            'racoon': import_folder('..\\zelda\\maskedninja\\graphics\\particles\\racoon'),
            'spirit': import_folder('..\\zelda\\maskedninja\\graphics\\particles\\nova'),
            'bamboo': import_folder('..\\zelda\\maskedninja\\graphics\\particles\\bamboo'),

            # leafs
            'leaf': (
                import_folder('..\\zelda\\maskedninja\\graphics\\particles\\leaf1'),
                import_folder('..\\zelda\\maskedninja\\graphics\\particles\\leaf2'),
                import_folder('..\\zelda\\maskedninja\\graphics\\particles\\leaf3'),
                import_folder('..\\zelda\\maskedninja\\graphics\\particles\\leaf4'),
                import_folder('..\\zelda\\maskedninja\\graphics\\particles\\leaf5'),
                import_folder('..\\zelda\\maskedninja\\graphics\\particles\\leaf6'),
                self.reflect_images(import_folder('..\\zelda\\maskedninja\\graphics\\particles\\leaf1')),
                self.reflect_images(import_folder('..\\zelda\\maskedninja\\graphics\\particles\\leaf2')),
                self.reflect_images(import_folder('..\\zelda\\maskedninja\\graphics\\particles\\leaf3')),
                self.reflect_images(import_folder('..\\zelda\\maskedninja\\graphics\\particles\\leaf4')),
                self.reflect_images(import_folder('..\\zelda\\maskedninja\\graphics\\particles\\leaf5')),
                self.reflect_images(import_folder('..\\zelda\\maskedninja\\graphics\\particles\\leaf6'))
            )
        }
    def reflect_images(self, frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pg.transform.flip(frame,True,False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, group):
        animation_frames = choice(self.frames["leaf"])
        ParticleEffect(pos, animation_frames, group)

    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)

class ParticleEffect(pg.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups, z=LAYERS["main"]):
        super().__init__(groups)
        self.z = z
        self.sprite_type = "magic"
        self.frame_index = 0
        self.animation_speed = 9
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)
