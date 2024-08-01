import pygame, sys
from scripts.menu import MenuEsfinge
pygame.init()

#Criação da tela
screen = pygame.display.set_mode((800, 600))
#Definição dos fps
clock = pygame.time.Clock()

#Loop while = 1 frame
while True:
    #Define o fps (120)
    clock.tick(120)
    #Preenche a tela com uma cor
    screen.fill((30, 30, 30))


    #Registra os eventos
    for event in pygame.event.get():
        #Registra o evento de clicar no "x" da janela
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #Atualiza a tela
    pygame.display.update()
    MenuEsfinge()