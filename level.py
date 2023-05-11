import pygame as pg
from settings import *
from player import Player
from mapcreator import MapCreator, Decorations, Trees
from pytmx.util_pygame import load_pygame
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from random import randint
from magic import MagicPlayer

class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pg.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pg.sprite.Group()

        self.tmx_data = load_pygame("..\\zelda\\maskedninja\\map\\mapa1.tmx")

        #attack sprites
        self.current_attack = None
        self.attack_sprites = pg.sprite.Group()
        self.attackable_sprites = pg.sprite.Group()

        #sprite setup
        self.create_map()

        #user interface
        self.ui = UI()

        #particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        # background
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "data"):
                for x,y,surf in layer.tiles():
                    if layer.name == "skybox":
                        pass
                    else:
                        pos = (x*TILESIZE,y*TILESIZE)
                        MapCreator(pos=pos, surf=surf, groups=self.visible_sprites, z=LAYERS["ground"])
        #decorations
        for obj in self.tmx_data.get_layer_by_name("Decorations"):
            Decorations((obj.x,obj.y), obj.image, [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],obj.name,"grass")
        #Trees
        for obj in self.tmx_data.get_layer_by_name("Trees"):
            Trees((obj.x,obj.y), obj.image,[self.visible_sprites, self.obstacle_sprites],obj.name)
        #Collision tiles
        for x,y,surf in self.tmx_data.get_layer_by_name("skybox").tiles():
            MapCreator((x*TILESIZE,y*TILESIZE), pg.Surface((TILESIZE,TILESIZE)),self.obstacle_sprites)
        for obj in self.tmx_data.objects:
            if obj.name == "Player":
                pos = obj.x, obj.y
                self.player = Player(pos,self.visible_sprites, self.obstacle_sprites, self.create_attack, self.destroy_attack,self.create_magic)
        for obj in self.tmx_data.objects:
            if obj.name == "Enemy":
                pos = obj.x, obj.y
                Enemy("racoon", pos, [self.visible_sprites, self.attackable_sprites, ], self.obstacle_sprites, self.damage_player, self.trigger_death_particles, self.add_exp, self.player)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self,style,strength,cost):
        if style == "heal":
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == "flame":
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pg.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "grass":
                            pos = target_sprite.rect.center
                            offset = pg.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos-offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pg.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

    def add_exp(self, amount):
        self.player.exp += amount

    def run(self, dt):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update(dt)
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)

class YSortCameraGroup(pg.sprite.Group):
    def __init__(self):

        #general setup
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1] //2
        self.offset = pg.math.Vector2()

    def custom_draw(self,player):

        # getting offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_pos = sprite.rect.topleft - self.offset
                    self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,"sprite_type") and sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
