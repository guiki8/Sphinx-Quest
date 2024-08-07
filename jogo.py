import pygame, time, sys
from scripts.menu import MenuEsfinge
from scripts.quest import Quest
from scripts.utils import load_image, load_images
from scripts.minigame_1 import StarMinigame

# Definição dos fps
clock = pygame.time.Clock()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Sphinx Quest')

        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.clock = pygame.time.Clock()
        
        self.q1 = Quest(self.screen, {'num': 1 , 'dific': 2, 'pergunta':'Essa pergunta e boa?', 'r1':'A: sim', 'r2':'B: nao', 'r3':'C: talvez', 'r4':'D: sla porra', 'rcorreta': 4})

    def run(self):
        while True:
            self.screen.fill((30, 30, 30))
            self.clock.tick(60)

            quest1 = self.q1.load_quest()

            if quest1:
                time.sleep(1)
                print('prox minigame')
                mini_game = StarMinigame(self.screen)
                mini_game.run()  # Inicia o mini game
                return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            pygame.display.update()

Game().run()
