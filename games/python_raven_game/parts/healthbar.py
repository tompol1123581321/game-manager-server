import pygame
from constans import *

from utils import get_image

health_point_image = pygame.image.load("/home/tomas/Documents/Projects/School/games/game_manager_app/game_manager_games/65a44be015dc9ffb905ac4b7/python_raven_game/Assets/Health/hearth.png")


class Health:
    def __init__(self):
        self.hps = 3
        self.hp_image = get_hp_image()

    def check_collision_and_lower_hp(self, did_collide):
        if did_collide and self.hps > 0:
            self.hps -= 1

    def show_healthbars(self, screen):
        for i in range(self.hps):
            screen.blit(self.hp_image, (60 * i, 10))

    def reset(self):
        self.hps = 3
        self.hp_image = get_hp_image()


def get_hp_image():
    return get_image(health_point_image, 50, 50, 1, BLACK, (0, 0))
