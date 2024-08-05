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

        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.clock = pygame.time.Clock()
        
        self.q1 = Quest(self.screen, {'num': 1 , 'dific': 2, 'pergunta':'Essa pergunta e boa?', 'r1':'A: sim', 'r2':'B: nao', 'r3':'C: talvez', 'r4':'D: sla porra'})

    def run(self):
        #Loop while = 1 frame
        while True:
            #Preenche a tela com uma cor
            self.screen.fill((30, 30, 30))

            self.q1.load_quest()
            self.q1.render()
            
            #Define o fps (120)
            self.clock.tick(60)

            #Registra os eventos
            for event in pygame.event.get():
                #Registra o evento de clicar no "x" da janela
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            #Atualiza a tela
            pygame.display.update()

Game().run()