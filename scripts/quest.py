import pygame
class Quest():
    #Definição dos atributos
    def __init__(self,screen, info={}):
        self.info = info
        self.quest_num = info['num']
        self.dificuldade = info['dific']
        self.pergunta = info['pergunta']
        self.respostas = [info['r1'], info['r2'], info['r3'], info['r4']]
        self.screen = screen
        self.font_color = (0, 150, 200)
        self.font_size = 15
        self.fonte = pygame.font.SysFont('assets/pixelated.ttf', self.font_size, True, True)

    def load_quest(self):
        #Cria quadrado branco onde fica a pergunta
        quest_box = pygame.Rect(200, 200, len(self.info['pergunta'])*self.font_size, 50)

        #Joga na tela o quadrado
        pygame.draw.rect(self.screen, (255, 255, 255), quest_box)

        #Joga na tela a borda do quadrado
        pygame.draw.rect(self.screen, self.font_color, quest_box, 3)

        #Gera o texto da pergunta
        texto = self.fonte.render(self.pergunta, False, self.font_color)

        #Joga na tela o texto centralizado com o quadrado
        self.screen.blit(texto, (quest_box.centerx - quest_box.width/4, quest_box.centery - quest_box.height/4))