import pygame, time, sys
from pygame import mixer
from scripts.menu import MenuEsfinge
from scripts.quest import Quest
from scripts.utils import load_image, load_images
from scripts.minigame_1 import FruitMinigame

class Game:
    def __init__(self):
        pygame.init()
        mixer.init()
        pygame.display.set_caption('Sphinx Quest')

        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.clock = pygame.time.Clock()
        
        # Inicializa as quests
        self.quests = [
            Quest(self.screen, {'num': 1, 'dific': 1, 'pergunta':'Complete a frase: “___ I go to the bathroom?', 'r1':'A: Can', 'r2':'B: Could', 'r3':'C: I’m able to', 'r4':'D: Maybe', 'rcorreta': 1}),
            Quest(self.screen, {'num': 2, 'dific': 2, 'pergunta':'Qual das frases abaixo está correta:', 'r1':'A: Can, let the dog out?', 'r2':'B: Could you lend me a hand?', 'r3':'C: I wish, I can buy this car!', 'r4':'D: I wish, I be able to fly.', 'rcorreta': 2}),
            Quest(self.screen, {'num': 3, 'dific': 3, 'pergunta':'Que tipo de verbo é “be able to”?', 'r1':'A: Action', 'r2':'B: Auxiliary', 'r3':'C: Modal', 'r4':'D: Phrasal', 'rcorreta': 4})
        ]

        self.current_quest_index = 0

    def fade_out(self, duration):
        fade_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        fade_surface.fill((0, 0, 0))
        for alpha in range(0, 255):
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(duration // 255)

    def fade_in(self, duration):
        fade_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        fade_surface.fill((0, 0, 0))
        for alpha in range(255, 0, -1):
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(duration // 255)

    def run(self):
        while True:
            self.screen.fill((30, 30, 30))
            self.clock.tick(120)

            # Verifica se ainda há quests a serem completadas
            if self.current_quest_index < len(self.quests):
                current_quest = self.quests[self.current_quest_index]

                # Se a quest for completada corretamente, avança para a próxima
                if current_quest.load_quest():
                    time.sleep(0.5)
                    self.current_quest_index += 1
            else:
                # Quando todas as quests são completadas, inicia o minigame
                time.sleep(1)
                print('prox minigame')
                self.fade_out(1000)  # Fade out in 1 second
                mini_game = FruitMinigame(self.screen)
                mini_game.run()  # Inicia o mini game
                self.fade_in(1000)  # Fade in in 1 second
                return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

Game().run()
