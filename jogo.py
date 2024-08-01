import pygame, sys
from scripts.menu import MenuEsfinge
from scripts.quest import Quest
pygame.init()

#Criação da tela
screen = pygame.display.set_mode((800, 600))
#Definição dos fps
clock = pygame.time.Clock()

quests = []
q1 = Quest(screen, {'num': 1 , 'dific': 2, 'pergunta':'Oq é oq é?', 'r1':'a', 'r2':'b', 'r3':'c', 'r4':'d'})
quests.append(q1)

#Loop while = 1 frame
while True:
    #Define o fps (120)
    clock.tick(120)
    #Preenche a tela com uma cor
    screen.fill((30, 30, 30))   

    q1.load_quest()

    #Registra os eventos
    for event in pygame.event.get():
        #Registra o evento de clicar no "x" da janela
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #Atualiza a tela
    pygame.display.update()