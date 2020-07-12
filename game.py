
import glob

import pygame
from pygame.locals import *
import sys
import random

WIDTH = 1920
HEIGHT = 1080
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 216, 0)
text = (207, 95, 63)

BACKGROUND = pygame.image.load("assets/img/bg2.png")

INTRO = pygame.image.load("assets/img/start.png")

WIN = pygame.image.load("assets/img/win.png")

screen = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)


class NoMiniGame:
    def __init__(self):
        self.x = 0
        self.y = 0

        self.close_x = 0
        self.close_y = 0
        self.close = pygame.image.load("assets/img/close.png")

        self.img = None
        self.path = path = "assets/img/nominigame"
        self.load_image()
        self.random_move()
        self.random_move_close()

    def load_image(self):
        imgs = glob.glob(self.path + "/*.png")
        # print(imgs)
        self.img = pygame.image.load(random.choice(imgs))

    def draw(self, screen):
        screen.blit(self.img, self.get_rect())

        screen.blit(self.close, self.get_rect_close())

    def move(self, x, y):
        self.x = x
        self.y = y

    def random_move(self):
        rect = self.get_rect()
        x_offset = WIDTH - rect.width
        y_offset = HEIGHT - rect.height
        if x_offset != 0:
            self.x = random.randrange(0, x_offset)
        if y_offset != 0:
            self.y = random.randrange(0, y_offset)

    def get_rect(self):
        image = self.img
        rect = image.get_rect()
        rect.x = self.x
        rect.y = self.y

        return rect

    def get_rect_close(self):
        image = self.close
        rect = image.get_rect()
        rect.x = self.close_x
        rect.y = self.close_y

        return rect

    def random_move_close(self):
        rect = self.get_rect()
        close_rect = self.get_rect_close()
        self.close_x = random.randrange(self.x, self.x + rect.width - close_rect.width)
        self.close_y = random.randrange(self.y, self.y + rect.height - close_rect.height)

    def check_close(self, x, y):
        rect = self.get_rect_close()
        return (self.close_x < x < self.close_x + rect.width) and (self.close_y < y < self.close_y + rect.height)

    def check_ad_click(self, x, y):
        rect = self.get_rect()
        return (self.x < x < self.x + rect.width) and (self.close_y < y < self.close_y + rect.height)


ads = [NoMiniGame()]
ad_streak = 0
ad_countdown_min = 2
ad_countdown_max = 5
ad_countdown = random.randrange(ad_countdown_min, ad_countdown_max)
count = 0

score = 10000

intro = True
win = False

if __name__ == "__main__":
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.init()
    clock = pygame.time.Clock()
    mainLoop = True
    font = pygame.font.SysFont("monospace", 50)
    screen.blit(BACKGROUND, BACKGROUND.get_rect())

    while mainLoop:
        pygame.event.pump()
        clock.tick(FPS)

        keys = pygame.key.get_pressed()
        mx, my = pygame.mouse.get_pos()

        if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
            pygame.quit()
            sys.exit(0)
        ev = pygame.event.get()

        if intro:
            ads = [NoMiniGame()]
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    intro = False
            screen.blit(INTRO, (0, 0, HEIGHT, WIDTH))
        else:
            if win and len(ads) == 0:
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        intro = True
                        win = False
                screen.blit(WIN, (0, 0, HEIGHT, WIDTH))
                label = font.render("SCORE = " + str(score), 1, text)
                screen.blit(label, (0, 0))

            else:
                screen.blit(BACKGROUND, (0, 0, HEIGHT, WIDTH))
                count += 1
                if count >= ad_countdown * (FPS / 3):
                    ads.append(NoMiniGame())
                    ad_countdown = random.randrange(ad_countdown_min, ad_countdown_max)
                    score -= 100
                    if len(ads) >= 20:
                        intro = True
                    count = 0

                # proceed events
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        for ad in ads:
                            if ad.check_close(mx, my):
                                ads.remove(ad)
                                break
                            elif ad.check_ad_click(mx, my):
                                ads.append(NoMiniGame())
                                ad_countdown = random.randrange(ad_countdown_min, ad_countdown_max)
                                score -= 100
                                if len(ads) >= 20:
                                    intro = True
                if len(ads) <= 1:
                    ad_streak += 1
                    if ad_streak > 10 * FPS:
                        win = True
                else:
                    ad_streak = 0

                for ad in ads:
                    ad.draw(screen)

        pygame.display.flip()

    pygame.quit()
