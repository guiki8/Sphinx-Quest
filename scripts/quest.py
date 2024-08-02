import pygame, sys
from scripts.utils import load_image, load_images

class Quest():
    #Definição dos atributos
    def __init__(self, screen, info={}):
        self.info = info
        self.quest_num = info['num']
        self.dificuldade = info['dific']
        self.pergunta = info['pergunta']
        self.respostas = [info['r1'], info['r2'], info['r3'], info['r4']]
        self.screen = screen
        self.font_color = (0, 150, 200)
        self.font_size = 25
        self.fonte = pygame.font.Font('assets/fonts/Pixel.ttf', self.font_size)
        self.fonte_bold = pygame.font.Font('assets/fonts/PixelBold.ttf', self.font_size)
        self.font_width = self.font_size*0.3

        self.assets = {
            'esfinge': load_image('esfinge_spr1.png'),
            'button': load_image('button/1.png'),
            'push_button': load_image('button/2.png')
        }

    def load_quest(self):
        #Carrega a esfinge na tela                                    (height, width) (pos x, pos y)
        self.screen.blit(pygame.transform.scale(self.assets['esfinge'], (400, 400)), (400, 50))

        #Cria quadrado branco onde fica a pergunta
        quest_box = pygame.Rect(100, 50, len(self.info['pergunta'])*(self.font_size - self.font_width) + self.font_width, 50)

        #Joga na tela o quadrado
        pygame.draw.rect(self.screen, (255, 255, 255), quest_box)

        #Joga na tela a borda do quadrado
        pygame.draw.rect(self.screen, self.font_color, quest_box, 3)

        #Gera o texto da pergunta
        texto = self.fonte.render(self.pergunta, False, self.font_color)

        #Joga na tela o texto centralizado com o quadrado
        self.screen.blit(texto, (quest_box.left + self.font_width, quest_box.centery - quest_box.height/4))
    
    def render(self):
        #Carrega o botão na tela 
        for i in range(4):
            button = Button(self.screen, self.assets, (i*150, 500))
            button.update()
            
class Button():
    def __init__(self, screen, assets, pos=(0, 0)):
        self.button_pos = pos
        self.screen = screen
        self.assets = assets

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        button_size = (100, 100)
        button_rect = pygame.Rect(self.button_pos, button_size)
        if button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.screen.blit(pygame.transform.scale(self.assets['push_button'], button_size), self.button_pos)
        else:
            self.screen.blit(pygame.transform.scale(self.assets['button'], button_size), self.button_pos)