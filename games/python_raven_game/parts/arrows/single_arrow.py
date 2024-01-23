from math import degrees, atan2
import pygame
import random
import uuid
from constans import *
from utils import check_collision, get_image

sprite_sheet_image = pygame.image.load("/home/tomas/Documents/Projects/School/games/game_manager_app/game_manager_games/65a44be015dc9ffb905ac4b7/python_raven_game/Assets/Arrow/Arr123.png")


class Arrow:
    def __init__(self, raven_position):
        self.current_position = get_random_arrow_start_position()

        self.axis_speed = get_arrow_axis_speed(
            raven_position, self.current_position)
        self.rotation = degrees(
            atan2(self.axis_speed[0], self.axis_speed[1])) + 90
        self.arrow_img = get_arrow(self.rotation)

    def move_arrow(self):
        self.current_position = get_arrow_position(
            self.axis_speed, self.current_position)

    def get_is_aget_is_arrow_out_of_bound(self):
        arrow_position: tuple = self.current_position
        return arrow_position[0] > SCREEN_WIDTH + 700 or arrow_position[0] < 0 - 700 or arrow_position[1] > SCREEN_HEIGHT + 700 or arrow_position[1] < 0 - 700

    def get_did_arrow_hit(self, raven_position):
        return check_collision(raven_position, self.current_position)


def get_arrow_position(axis_speed, current_arrow_position):

    new_position = (current_arrow_position[0] + axis_speed[0],
                    current_arrow_position[1] + axis_speed[1])
    return new_position


def get_arrow_axis_speed(raven_position, current_arrow_position):
    speed = MOVEMENT_SPEED * 2
    directions = (raven_position[0] + (RAVEN_SPRITE_WIDTH/2*SCALE) - current_arrow_position[0],
                  raven_position[1] + (RAVEN_SPRITE_HEIGHT/2*SCALE) - current_arrow_position[1])
    unit = pow(pow(speed, 2) /
               (pow(directions[0], 2)+pow(directions[1], 2)), 1/2)

    return (unit * directions[0], unit * directions[1])


def get_arrow(rotation):
    return get_image(sprite_sheet_image, ARROW_SPRITE_WIDTH, ARROW_SPRITE_HEIGHT, ARROW_SCALE, BLACK, (0, 0), rotation)


def get_random_arrow_start_position():
    side = random.choice([1, 2, 3, 4])
    if side == 1:
        return (0-ARROW_SPRITE_WIDTH * ARROW_SCALE,
                random.uniform(0, SCREEN_HEIGHT))
    if side == 2:
        return (random.uniform(0, SCREEN_WIDTH),
                0 + ARROW_SPRITE_HEIGHT * ARROW_SCALE)
    if side == 3:
        return (ARROW_SPRITE_WIDTH * ARROW_SCALE + SCREEN_WIDTH,
                random.uniform(0, SCREEN_HEIGHT))
    if side == 4:
        return (random.uniform(0, SCREEN_WIDTH),
                SCREEN_HEIGHT - ARROW_SPRITE_HEIGHT * ARROW_SCALE)
