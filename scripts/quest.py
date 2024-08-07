import pygame, sys, time
from scripts.utils import load_image, load_images, Animation

class Quest():
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
        self.font_width = self.font_size * 0.3

        self.assets = {
            'button': load_image('button/1.png'),
            'push_button': load_image('button/2.png'),
            'table': load_image('button/table.png'),
            'esfinge/idle': load_images('esfinge_sprites/idle')
        }

        self.esfinge_anim = Animation(self.assets['esfinge/idle'], img_dur=10, loop=True)
        self.buttons = [Button(self.screen, self.assets, (62 + i * 92, 372), i + 1, self.info) for i in range(4)]

    def load_quest(self):
        self.esfinge_anim.update()
        imagem_frame = self.esfinge_anim.img()
        self.screen.blit(pygame.transform.scale(imagem_frame, (500, 500)), (380, 20))

        quest_box = pygame.Rect(100, 50, len(self.info['pergunta']) * (self.font_size - self.font_width) + self.font_width, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), quest_box)
        pygame.draw.rect(self.screen, self.font_color, quest_box, 3)
        texto = self.fonte.render(self.pergunta, False, self.font_color)
        self.screen.blit(texto, (quest_box.left + self.font_width, quest_box.centery - quest_box.height / 4))

        for i in range(4):
            quest_box = pygame.Rect(100, 110 + i * 60, len(self.info['r' + str(1 + i)]) * (self.font_size - self.font_width) + self.font_width, 50)
            pygame.draw.rect(self.screen, (255, 255, 255), quest_box)
            pygame.draw.rect(self.screen, self.font_color, quest_box, 3)
            texto = self.fonte.render(self.info['r' + str(1 + i)], False, self.font_color)
            self.screen.blit(texto, (quest_box.left + self.font_width, quest_box.centery - quest_box.height / 4))

        self.screen.blit(pygame.transform.scale(self.assets['table'], (400, 400)), (50, 200))

        for button in self.buttons:
            if button.update():
                return True
        return None



class Button():
    def __init__(self, screen, assets, pos=(0, 0), button_num=0, info={}):
        self.button_pos = pos
        self.screen = screen
        self.assets = assets
        self.button_size = (100, 100)
        self.button_image = pygame.transform.scale(self.assets['button'], self.button_size)
        self.button_pressed_image = pygame.transform.scale(self.assets['push_button'], self.button_size)
        self.button_num = button_num
        self.resp_correta = info['rcorreta']
        self.is_pressed = False

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(self.button_pos, self.button_size)

        if button_rect.collidepoint(self.mouse_pos):
            if pygame.mouse.get_pressed()[0]:  # Botão esquerdo do mouse pressionado
                self.is_pressed = True
            else:
                if self.is_pressed:
                    self.is_pressed = False
                    if self.button_num == self.resp_correta:
                        print('acertou!')
                        return True
                    else:
                        print('errou')
                        return False

        if self.is_pressed:
            self.screen.blit(self.button_pressed_image, self.button_pos)
        else:
            self.screen.blit(self.button_image, self.button_pos)
        return None
