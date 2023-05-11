import pygame as pg
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pg.image.load('..\\zelda\\maskedninja\\graphics\\player\\down_idle\\1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.old_rect = self.hitbox.copy()
        self.pos_dt = pg.math.Vector2(self.hitbox.topleft)

        #graphic
        self.import_player_assets()
        self.status = "down"

        #movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        self.z = LAYERS["main"]

        #weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        #magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        #stats
        self.stats = {"health":100, "energy":60, "attack":10, "magic":4, "speed":350}
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.exp = 50
        self.speed = self.stats["speed"]
        self.lvl = 1

        #damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

    def import_player_assets(self):
        charackter_path = "..\\zelda\\maskedninja\\graphics\\player\\"
        self.animations = {"up":[], "down":[], "left":[],"right":[],
                           "right_idle": [], "left_idle":[], "up_idle":[],"down_idle":[],
                           "right_attack": [], "left_attack":[], "up_attack":[],"down_attack":[]}
        for animation in self.animations.keys():
            full_path = charackter_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pg.key.get_pressed()
        if not self.attacking:
            #movement
            if keys[pg.K_w]:
                self.direction.y =-1
                self.status = "up"
            elif keys[pg.K_s]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pg.K_d]:
                self.direction.x = 1
                self.status = "right"
            elif keys[pg.K_a]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0
            #attack
            if keys[pg.K_k]:
                self.attacking = True
                self.attack_time = pg.time.get_ticks()
                self.create_attack()
            #magic
            if keys[pg.K_l]:
                self.attacking = True
                self.attack_time = pg.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]["strength"] + self.stats["magic"]
                cost = list(magic_data.values())[self.magic_index]["cost"]
                self.create_magic(style, strength, cost)

            #dodac opcje zmieniania broni bezposrednio powiazana ze zdobytymi przedmiotami
            #trzeba pamietac o tym ze jedno krotkie klikniecie bedzie czytane przez gre jako przynajmniej kilka
            if keys[pg.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pg.time.get_ticks()
                if self.weapon_index <len(list(weapon_data.keys())) - 1:
                    self.weapon_index +=1
                else:
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            if keys[pg.K_TAB] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pg.time.get_ticks()
                if self.magic_index <len(list(magic_data.keys())) - 1:
                    self.magic_index +=1
                else:
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack","")

    def cooldowns(self):
        current_time = pg.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]["cooldown"]:
                self.attacking = False
                self.destroy_attack()
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self, dt):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        #flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats["attack"]
        weapon_damage = weapon_data[self.weapon]["damage"]
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats["magic"]
        spell_damage = magic_data[self.magic]["strength"]
        return base_damage + spell_damage

    def energy_recovery(self, dt):
        if self.energy < self.stats["energy"]:
            self.energy += 0.3 * self.stats["magic"] * dt
        else:
            self.energy = self.stats["energy"]

    def level_up(self):
        if self.exp >= self.lvl * LEVEL_CONST:
            diff = self.exp - (self.lvl * LEVEL_CONST)
            self.lvl +=1
            self.exp = diff

    def collision(self,direction):

        collision_sprites = pg.sprite.spritecollide(self, self.obstacle_sprites, False)
        if collision_sprites:
            if direction == "horizontal":
                for sprite in collision_sprites:
                    if self.hitbox.right >= sprite.hitbox.left and self.old_rect.right <= sprite.old_rect.left:
                        self.hitbox.right = sprite.hitbox.left
                        self.pos_dt.x = self.hitbox.x
                    elif self.hitbox.left <= sprite.hitbox.right and self.old_rect.left >= sprite.old_rect.right:
                        self.hitbox.left = sprite.hitbox.right
                        self.pos_dt.x = self.hitbox.x
            if direction == "vertical":
                for sprite in collision_sprites:
                    if self.hitbox.bottom >= sprite.hitbox.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.pos_dt.y = self.hitbox.y
                    elif self.hitbox.top <= sprite.hitbox.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.pos_dt.y = self.hitbox.y


    def update(self, dt):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate(dt)
        self.move(self.speed, dt)
        self.energy_recovery(dt)
        self.level_up()
