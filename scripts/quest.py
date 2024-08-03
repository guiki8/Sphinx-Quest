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
            'push_button': load_image('button/2.png'),
            'table': load_image('button/table.png')
        }

    def load_quest(self):
        #Carrega a esfinge na tela                                    (height, width) (pos x, pos y)
        self.screen.blit(pygame.transform.scale(self.assets['esfinge'], (500, 500)), (380, 20))

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

        for i in range(4):
            #Mesma coisa da caixa de pergunta, porém para cada caixa de resposta (alterando a posição y individualmente)
            quest_box = pygame.Rect(100, 110+i*60, len(self.info['r'+str(1+i)])*(self.font_size - self.font_width) + self.font_width, 50)
            pygame.draw.rect(self.screen, (255, 255, 255), quest_box)
            pygame.draw.rect(self.screen, self.font_color, quest_box, 3)
            texto = self.fonte.render(self.info['r'+str(1+i)], False, self.font_color)
            self.screen.blit(texto, (quest_box.left + self.font_width, quest_box.centery - quest_box.height/4))

    
    def render(self):
        #Imprime a mesa na tela, redimensionando para o tamanho certo
        self.screen.blit(pygame.transform.scale(self.assets['table'], (400, 400)), (50,200))

        #Carrega os 4 botões na tela, alterando as posições x individuas
        for i in range(4):
            button = Button(self.screen, self.assets, (62+i*92, 372))
            button.update()
            
class Button():
    def __init__(self, screen, assets, pos=(0, 0)):
        self.button_pos = pos
        self.screen = screen
        self.assets = assets
        self.button_size = (100, 100)
        #Pega a imagem do botão e redimensiona para o tamanho correto
        self.button_image = pygame.transform.scale(self.assets['button'], self.button_size)

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()

        #Cria uma área retangular que representa o botão
        button_rect = pygame.Rect(self.button_pos, self.button_size)

        #Cria uma máscara do sprite do botão
        button_mask = pygame.mask.from_surface(self.button_image)

        #Posição do mouse em relação à máscara do botão
        pos_in_mask = self.mouse_pos[0] - self.button_pos[0], self.mouse_pos[1] - self.button_pos[1]

        #  Checa se o mouse está encima do botão, se o mouse está dentro da máscara do sprite e se o botão esquerdo é clicado
        if button_rect.collidepoint(self.mouse_pos) and button_mask.get_at(pos_in_mask) and pygame.mouse.get_pressed()[0]:
            #Troca o spride do botão para apertado
            self.button_image = pygame.transform.scale(self.assets['push_button'], self.button_size)
        else:
            self.button_image = pygame.transform.scale(self.assets['button'], self.button_size)

        #Imprime o botão na tela com o sprite renderizado
        self.screen.blit(self.button_image, self.button_pos)