import pygame, sys, time
from pygame import mixer
from scripts.utils import load_image, load_images, Animation

class Quest():
    def __init__(self, screen, info={}):
        self.info = info
        self.quest_num = info['num']
        self.dificuldade = info['dific']
        self.pergunta = info['pergunta']
        self.respostas = [info['r1'], info['r2'], info['r3'], info['r4']]
        self.screen = screen
        self.font_color = (0, 150, 200)  # Azul para o texto e borda interna
        self.outer_border_color = (200, 200, 0)  # Amarelo para a borda externa
        self.answer_border_color = (100, 100, 100)  # Preto para a borda das respostas
        self.font_size = 20
        self.fonte = pygame.font.Font('assets/fonts/Pixel.ttf', self.font_size)
        self.fonte_bold = pygame.font.Font('assets/fonts/PixelBold.ttf', self.font_size)
        self.font_width = self.font_size * 0.3

        # Tocar música de fundo em loop
        pygame.mixer.music.load('assets/sounds/minigame_track.mp3')
        pygame.mixer.music.play(-1)  # -1 faz a música tocar em loop indefinidamente

        self.assets = {
            'button': load_image('button/1.png'),
            'push_button': load_image('button/2.png'),
            'table': load_image('button/table.png'),
            'esfinge/idle': load_images('esfinge_sprites/idle')
        }

        self.esfinge_anim = Animation(self.assets['esfinge/idle'], img_dur=10, loop=True)
        self.buttons = [Button(self.screen, self.assets, (62 + i * 92, 372), i + 1, self.info) for i in range(4)]

    def break_text_into_lines(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = words[0]

        for word in words[1:]:
            if self.fonte.size(current_line + ' ' + word)[0] <= max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)

        return lines

    def load_quest(self):
        self.esfinge_anim.update()
        imagem_frame = self.esfinge_anim.img()
        self.screen.blit(pygame.transform.scale(imagem_frame, (500, 500)), (380, 20))
    
        max_width = 600
        linhas_pergunta = self.break_text_into_lines(self.pergunta, max_width)
        max_line_width = max(self.fonte.size(linha)[0] for linha in linhas_pergunta)
        
        quest_box_width = max(min(max_line_width, max_width), self.font_size * 10)
        quest_box_height = 25 * len(linhas_pergunta)
        
        quest_box = pygame.Rect(100, 50, quest_box_width, quest_box_height)
        pygame.draw.rect(self.screen, self.outer_border_color, quest_box.inflate(6, 6))
        pygame.draw.rect(self.screen, (255, 255, 255), quest_box)
        pygame.draw.rect(self.screen, self.font_color, quest_box, 3)
    
        for i, linha in enumerate(linhas_pergunta):
            texto = self.fonte.render(linha, False, self.font_color)
            self.screen.blit(texto, (quest_box.left + self.font_width, quest_box.top + i * self.font_size))
    
        resposta_box_y = quest_box.bottom + 20  # Espaço entre a caixa da pergunta e a primeira resposta
        for i in range(4):
            linhas_resposta = self.break_text_into_lines(self.info['r' + str(1 + i)], max_width)
            max_line_width = max(self.fonte.size(linha)[0] for linha in linhas_resposta)
            
            resposta_box_width = max(min(max_line_width, max_width), self.font_size * 10)
            resposta_box_height = 25 * len(linhas_resposta) + 20  # 20 é a altura adicional para espaçamento interno
    
            resposta_box = pygame.Rect(100, resposta_box_y, resposta_box_width, resposta_box_height)
            pygame.draw.rect(self.screen, (255, 255, 255), resposta_box)
            pygame.draw.rect(self.screen, self.answer_border_color, resposta_box, 3)
    
            for j, linha in enumerate(linhas_resposta):
                texto = self.fonte.render(linha, False, self.font_color)
                self.screen.blit(texto, (resposta_box.left + self.font_width, resposta_box.top + j * self.font_size))
    
            resposta_box_y += resposta_box_height + 10  # Espaço entre as caixas de resposta
    
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
        self.sound_correct = pygame.mixer.Sound('assets/sounds/click_right.mp3')
        self.sound_wrong = pygame.mixer.Sound('assets/sounds/click_wrong.mp3')

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
                        self.sound_correct.play()
                        return True
                    else:
                        print('errou')
                        self.sound_wrong.play()
                        return False

        if self.is_pressed:
            self.screen.blit(self.button_pressed_image, self.button_pos)
        else:
            self.screen.blit(self.button_image, self.button_pos)
        return None
