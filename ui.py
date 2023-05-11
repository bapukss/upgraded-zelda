import pygame as pg
from settings import *

class UI:
    def __init__(self):

        #general info
        self.display_surface = pg.display.get_surface()
        self.font = pg.font.Font(UI_FONT, UI_FONT_SIZE)
        self.half_width = self.display_surface.get_size()[0] // 2
        self.health_bar_x = self.half_width - HEALTH_BAR_WIDTH // 2
        self.energy_bar_x = self.half_width - ENERGY_BAR_WIDTH // 2
        #bar setup
        self.health_bar_rect = pg.Rect(self.health_bar_x,990, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pg.Rect(self.energy_bar_x,1030, ENERGY_BAR_WIDTH, BAR_HEIGHT)
        #weapon dict
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon["graphic"]
            weapon = pg.image.load(path).convert_alpha()                  #chec wprowadzenia skalowania wielkosci
            self.weapon_graphics.append(weapon)                           #grafik wiaze sie z przebudowaniem tego
        #conver magic dict
        self.magic_graphics = []
        for magic in magic_data.values():
            magic = pg.image.load(magic["graphic"]).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current,max_amount,bg_rect,color):
        #bg
        pg.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        #converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        #bar
        pg.draw.rect(self.display_surface,color,current_rect)
        pg.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect,4)
        #health/energy text
        stat_surf = self.font.render(str(int(current)), False, TEXT_COLOR)
        x = bg_rect.centerx
        y = bg_rect.centery - 5
        health_rect = stat_surf.get_rect(center=(x,y))
        self.display_surface.blit(stat_surf,health_rect)

    def show_exp(self, exp, lvl):
        text_surf = self.font.render(str(int(exp))+"/"+ str(lvl*LEVEL_CONST), False,TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x,y))

        pg.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,0))
        self.display_surface.blit(text_surf,text_rect)
        pg.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 0),4)

    def show_lvl(self, lvl):
        lvl_surf = self.font.render(str(lvl), False, TEXT_COLOR)
        x = 20
        y = self.display_surface.get_size()[1] - 20
        lvl_rect = lvl_surf.get_rect(bottomleft=(x,y))

        pg.draw.rect(self.display_surface, UI_BG_COLOR, lvl_rect.inflate(20,0))
        self.display_surface.blit(lvl_surf, lvl_rect)
        pg.draw.rect(self.display_surface, UI_BORDER_COLOR, lvl_rect.inflate(20, 0), 4)

    def selection_box(self,left,top, has_switched):
        bg_rect = pg.Rect(left,top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pg.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pg.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 4)
        else:
            pg.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 4)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(1800, 800, has_switched)  # weapon
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self,magic_index,has_switched):
        bg_rect = self.selection_box(1800, 900, has_switched)  # magic
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats["health"], self.health_bar_rect, HEATH_COLOR)
        self.show_bar(player.energy, player.stats["energy"], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp, player.lvl)
        self.show_lvl(player.lvl)

        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)
