import pygame
from constans import *
from utils import get_image

sprite_sheet_image = pygame.image.load("/home/tomas/Documents/Projects/School/games/game_manager_app/game_manager_games/65a44be015dc9ffb905ac4b7/python_raven_game/Assets/Raven/Raven.png")


class Raven:
    def __init__(self):
        self.current_position = (0, 0)
        self.current_sprite_frame = 0
        self.movement_directions = {"right": False,
                                    "left": False, "up": False, "down": False}

    def change_sprite_frame(self):
        if self.current_sprite_frame == 7:
            self.current_sprite_frame = 0
        else:
            self.current_sprite_frame += 1

    def change_position(self):
        self.current_position = move_raven(
            self.movement_directions, self.current_position)

    def change_directions(self, event):
        self.movement_directions = handle_movement_input(
            event, self.movement_directions)

    def show_raven(self, screen):
        screen.blit(get_image(sprite_sheet_image, RAVEN_SPRITE_WIDTH, RAVEN_SPRITE_HEIGHT,
                    SCALE, BLACK, (self.current_sprite_frame, 2)), self.current_position)

    def reset(self):
        self.current_position = (0, 0)
        self.current_sprite_frame = 0
        self.movement_directions = {"right": False,
                                    "left": False, "up": False, "down": False}


def handle_movement_input(event, current_dirrections):
    keyboard_key = event.dict.get("key")
    movement_directions = current_dirrections
    if keyboard_key == pygame.K_DOWN:
        if event.type == pygame.KEYDOWN:
            movement_directions["down"] = True
        else:
            movement_directions["down"] = False

    elif keyboard_key == pygame.K_UP:
        if event.type == pygame.KEYDOWN:
            movement_directions["up"] = True
        else:
            movement_directions["up"] = False

    elif keyboard_key == pygame.K_RIGHT:
        if event.type == pygame.KEYDOWN:
            movement_directions["right"] = True
        else:
            movement_directions["right"] = False

    elif keyboard_key == pygame.K_LEFT:
        if event.type == pygame.KEYDOWN:
            movement_directions["left"] = True
        else:
            movement_directions["left"] = False
    return movement_directions


def move_raven(movement_directions, position):
    new_position = position
    if movement_directions["right"]:
        if position[0] < (SCREEN_WIDTH - RAVEN_SPRITE_WIDTH * SCALE) - MOVEMENT_SPEED:
            new_position = (position[0]+MOVEMENT_SPEED, position[1])
        else:
            new_position = (
                (SCREEN_WIDTH - RAVEN_SPRITE_WIDTH * SCALE), position[1])
    elif movement_directions["left"]:
        if position[0] < MOVEMENT_SPEED:
            new_position = (0, position[1])
        else:
            new_position = (position[0]-MOVEMENT_SPEED, position[1])

    elif movement_directions["down"]:
        if position[1] > (SCREEN_HEIGHT - RAVEN_SPRITE_HEIGHT * SCALE) - MOVEMENT_SPEED:
            new_position = (
                position[0],  (SCREEN_HEIGHT - RAVEN_SPRITE_HEIGHT * SCALE))
        else:
            new_position = (
                position[0], position[1]+MOVEMENT_SPEED)
    elif movement_directions["up"]:
        y_position = 0
        if position[1] < MOVEMENT_SPEED:
            y_position = 0
        else:
            y_position = position[1] - MOVEMENT_SPEED
        new_position = (
            position[0], y_position)
    return new_position
