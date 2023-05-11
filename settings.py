import pygame as pg
#SCREEN
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
TILESIZE = 64

#lvl/exp
LEVEL_CONST = 150


HITBOX_OFFSET = 0   

#ui
BAR_HEIGHT = 30
HEALTH_BAR_WIDTH = 300
ENERGY_BAR_WIDTH = 210
ITEM_BOX_SIZE = 80
UI_FONT = "..\\zelda\\maskedninja\\graphics\\font\\NormalFont.ttf"
UI_FONT_SIZE = 30
UI_STATS_SIZE = 25

#general colors
WATER_COLOR = "#71dde"
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#EEEEEE"

#ui colors
HEATH_COLOR = "red"
ENERGY_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"

#LAYERS
LAYERS = {
    "skybox": 1,
    "ground":2,
    "main":3,
    "rain":4
}

weapon_data = {
    "sword" : {"cooldown":100, "damage": 15, "graphic":"..\\zelda\\maskedninja\\graphics\\weapons\\sword\\full.png"},
    "lance" : {"cooldown":400, "damage": 30, "graphic":"..\\zelda\\maskedninja\\graphics\\weapons\\lance\\full.png"},
    "axe" : {"cooldown":300, "damage": 20, "graphic":"..\\zelda\\maskedninja\\graphics\\weapons\\axe\\full.png"},
    "rapier" : {"cooldown":50, "damage": 8, "graphic":"..\\zelda\\maskedninja\\graphics\\weapons\\rapier\\full.png"},
    "sai" : {"cooldown":80, "damage": 10, "graphic":"..\\zelda\\maskedninja\\graphics\\weapons\\sai\\full.png"}
}

magic_data = {
    "flame":{"strength":5, "cost":20, "graphic":"..\\zelda\\maskedninja\\graphics\\particles\\flame\\fire.png"},
    "heal":{"strength":20, "cost":10, "graphic":"..\\zelda\\maskedninja\\graphics\\particles\\heal\\heal.png"},
}
#enemy
monster_data = {
    "racoon":{"health":100, "exp":150, "damage":40, "attack_type":"claw", "attack_sound":"..\\zelda\\maskedninja\\audio\\attack\\Fireball.wav","speed":200, "resistance":3, "attack_radius":120, "notice_radius":400},
    "spirit":{"health":100, "exp":110, "damage":8, "attack_type":"thunder", "attack_sound":"..\\zelda\\maskedninja\\audio\\attack\\Fireball.wav","speed":400, "resistance":3, "attack_radius":60, "notice_radius":350},
    "bamboo":{"health":70, "exp":120, "damage":6, "attack_type":"leaf_attack", "attack_sound":"..\\zelda\\maskedninja\\audio\\attack\\Fireball.wav","speed":300, "resistance":3, "attack_radius":50, "notice_radius":300}
}
