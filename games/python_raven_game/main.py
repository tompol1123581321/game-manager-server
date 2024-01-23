import concurrent.futures
import threading
import pygame
from constans import *
from utils import License_Manager, Time_Manager
from parts.menu import Menu
from parts.arrows.arrow_manager import Arrows
from parts.healthbar import Health
from parts.raven import Raven
from parts.score import Score
import sys
import argparse




parser=argparse.ArgumentParser()
parser.add_argument("--key1")
parser.add_argument("--key2")
parser.add_argument("--key3")

args=parser.parse_args()
# if not args.key1 or not args.key2 or not args.key3:
#         sys.exit("Auth keys were not received.")




# Using ThreadPoolExecutor to run license check in a separate thread
with concurrent.futures.ThreadPoolExecutor() as executor:
    print("gotten here")
    future = executor.submit(License_Manager.isLicensed,args.key1,args.key2,args.key3)
    print("gotten here2")

    for completed_future in concurrent.futures.as_completed([future]):
           is_license_valid = completed_future.result()
           print(is_license_valid)

# Proceed only if the license is valid
print(is_license_valid)
           
if not is_license_valid:
    sys.exit("License check failed. Exiting the game.")


exitFlag=threading.Event()

License_Manager.StartLicensePooler(exitFlag,args.key1,args.key2,args.key3)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),)
pygame.display.set_caption("Raven Flight")
font = pygame.font.Font('freesansbold.ttf', 32)


arrows = Arrows()
health_bar = Health()
score = Score(font)
raven = Raven()


def handle_fire_arrow():
    arrows.add_arrow(raven.current_position)


def reset():
    arrows.reset()
    health_bar.reset()
    score.reset()
    raven.reset()
    time_manager.reset()


menu = Menu(reset, font)
menu.show_initial_menu(screen)

time_manager = Time_Manager(
    handle_fire_arrow, raven.change_sprite_frame, score.increase_score)


run = True
while run and menu.run:
    if exitFlag.is_set():
        break

    screen.fill(BG)

    arrows.render_arrows(screen)
    health_bar.show_healthbars(screen)
    score.show_score(screen)
    raven.show_raven(screen)

    health_bar.check_collision_and_lower_hp(
        arrows.on_move_arrows(raven.current_position))
    raven.change_position()

    time_manager.tick()

    if health_bar.hps == 0:
        menu.show_played_menu(screen, score.score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            raven.change_directions(event)
    pygame.display.update()
pygame.quit()