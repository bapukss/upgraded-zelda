import pygame as pg
from settings import *
from entity import Entity
from support import *

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp,player, z=LAYERS["main"]):
        #general setup
        super().__init__(groups)
        self.z = z
        self.sprite_type = "enemy"
        self.player = player

        #graphic setup
        self.import_graphics(monster_name)
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index]

        #movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,-10) #######0,-10
        self.old_rect = self.hitbox.copy()
        self.pos_dt = pg.math.Vector2(self.hitbox.topleft)

        self.obstacle_sprites = obstacle_sprites
        #stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info["health"]
        self.exp = monster_info["exp"]
        self.speed = monster_info["speed"]
        self.attack_damage = monster_info["damage"]
        self.resistance = monster_info["resistance"]
        self.attack_radius = monster_info["attack_radius"]
        self.notice_radius = monster_info["notice_radius"]
        self.attack_type = monster_info["attack_type"]

        #player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

        #invi timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300


    def import_graphics(self,name):
        self.animations = {"idle":[], "move":[], "attack":[]}
        main_path = f"..\\zelda\\maskedninja\\graphics\\monsters\\{name}\\"
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        enemy_vec = pg.math.Vector2(self.rect.center)
        player_vec = pg.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance >0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pg.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack == True:
            if self.status != "attack":
                self.frame_index = 0
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def actions(self,player):
        if self.status == "attack":
            self.attack_time = pg.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == "move":
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pg.math.Vector2()

    def animate(self, dt):
        animation = self.animations[self.status]
        self.frame_index += (self.animation_speed - 0.5) * dt
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pg.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player,attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pg.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.add_exp(self.exp)

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def collision(self,direction):

        collision_sprites = pg.sprite.spritecollide(self, self.obstacle_sprites, False)

        if self.hitbox.colliderect(self.player.hitbox):
            collision_sprites.append(self.player)

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
        self.hit_reaction()
        self.move(self.speed, dt)
        self.animate(dt)
        self.cooldowns()


    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
        self.check_death()
        self.collision(player)
