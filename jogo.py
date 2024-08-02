import pygame, sys
from scripts.menu import MenuEsfinge
from scripts.quest import Quest
from scripts.utils import load_image, load_images

#Definição dos fps
clock = pygame.time.Clock()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Sphinx Quest')

        SCREEN_WIDTH = 960
        SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        #Dá um "zoom" na tela, pois os pixels são muito pequenos
        
        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        

    def run(self):
        #Loop while = 1 frame
        while True:
            #Define o fps (120)
            clock.tick(120)
            #Preenche a tela com uma cor
            quests = []
            q1 = Quest(self.screen, {'num': 1 , 'dific': 2, 'pergunta':'Essa pergunta e boa?', 'r1':'a', 'r2':'b', 'r3':'c', 'r4':'d'})
            quests.append(q1)
            self.screen.fill((30, 30, 30))

            q1.load_quest()

            #Registra os eventos
            for event in pygame.event.get():
                #Registra o evento de clicar no "x" da janela
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            #Atualiza a tela
            pygame.display.update()

Game().run()