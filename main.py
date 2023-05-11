import pygame as pg
from sys import exit
from settings import *
from button import Button
from level import Level
from debug import debug
import time

class Game:
    menu_state = "main"
    paused = True

    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("giera")
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(UI_FONT, 60)

        self.level = Level()

        cos = pg.image.load("..\\zelda\\maskedninja\\graphics\\button.png").convert_alpha()

        self.game_title = self.font.render("GAME TITLE", False, (111, 196, 169))
        self.start = Button(960, 257, cos, 2)
        self.how_to_play = Button(960, 464, cos, 1)
        self.settings_button = Button(960, 671, cos, 1)
        self.exit_game = Button(960, 878, cos, 1)
        self.back = Button(960, 1000, cos, 1)
        self.game_title_rect = self.game_title.get_rect(center=(980, 100))

        self.start = Button(960, 257, cos, 2)
        self.how_to_play = Button(960, 464, cos, 1)
        self.settings_button = Button(960, 671, cos, 1)
        self.exit_game = Button(960, 878, cos, 1)
        self.back = Button(960, 1000, cos, 1)

    def run(self):
        prev_time = time.time()
        while True:
            dt = time.time() - prev_time
            prev_time = time.time()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.paused = True
            if self.menu_state == "main":
                self.screen.fill((118, 148, 58))
                self.screen.blit(self.game_title, self.game_title_rect)
                if self.start.draw(self.screen):
                    self.paused = False
                if self.how_to_play.draw(self.screen):
                    self.menu_state = "how_to_play"
                if self.settings_button.draw(self.screen):
                    self.menu_state = "settings"
                if self.exit_game.draw(self.screen):
                    pg.quit()
                    exit()

            if not self.paused:
                self.screen.fill("blue")
                self.level.run(dt)
                self.exit_game.disactivate_button()          #tymczasowe naprawienie bledu powodujace ingerencje w menu
                self.how_to_play.disactivate_button()          #z poziomu gry (do zmiany)
                self.settings_button.disactivate_button()
                self.back.disactivate_button()
                self.start.disactivate_button()

            if self.menu_state == "settings":
                self.screen.fill(((126, 41, 135)))


                if self.back.draw(self.screen):
                    self.menu_state = "main"

            if self.menu_state == "how_to_play":
                self.screen.fill((219, 132, 161))


                if self.back.draw(self.screen):
                    self.menu_state = "main"

            if self.menu_state == "small_menu":
                self.screen.fill("black")

            debug(int(self.clock.get_fps()), 100)
            pg.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
