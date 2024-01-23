import pygame

from constans import *


class Menu():
    def __init__(self, resetFunc, font):
        self.reset = resetFunc
        self.font = font
        self.text = self.font.render("Press any Key to Start", True, (0, 0, 0))
        self.run = True

    def show_initial_menu(self, screen):
        run = True
        while run:
            screen.fill(WHITE)
            textRect = self.text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(self.text, textRect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    run = False

    def show_played_menu(self, screen, points):
        run = True
        while run:
            screen.fill(WHITE)
            score = self.font.render(
                "Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            screen.blit(score, scoreRect)
            textRect = self.text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(self.text, textRect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    run = False
                    self.run = True
                    self.reset()
