import pygame
from constans import *
green = (0, 255, 0)


class Score:
    def __init__(self, font):
        self.font = font
        self.score = 0
        self.text = font.render(str(self.score), True, green, BG)
        self.is_new_scrore = False

    def increase_score(self):
        self.score += 1
        self.is_new_scrore = True

    def show_score(self, screen):
        if self.is_new_scrore:
            self.text = self.font.render(str(self.score), True, green, BG)
        screen.blit(self.text, (SCREEN_WIDTH - 60, 10))

    def reset(self):
        self.score = 0
        self.text = self.font.render(str(self.score), True, green, BG)
        self.is_new_scrore = False
