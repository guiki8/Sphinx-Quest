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
            # Quests de dificuldade 1
            Quest(self.screen, {'num': 1, 'dific': 1, 'pergunta':'Complete the phrase: “___ I go to the bathroom?', 'r1':'A: Can', 'r2':'B: Could', 'r3':'C: I’m able to', 'r4':'D: Maybe', 'rcorreta': 1}),
            Quest(self.screen, {'num': 2, 'dific': 1, 'pergunta':'Which one of these things humans are able to do?', 'r1':'A: Fly', 'r2':'B: Breathe Underwater', 'r3':'C: Run a marathon', 'r4':'D: Survive without water', 'rcorreta': 3}),
            Quest(self.screen, {'num': 3, 'dific': 1, 'pergunta':'Which of the verbs down below best suits these phrases:   1. ___ you pass me the salt?   2. He ___ fly to London or Los Angeles.   3.I didn’t find the tools, ____ you help me?', 'r1':'A: Can', 'r2':'B: Be able to', 'r3':'C: Could', 'r4':'D: Should', 'rcorreta': 3}),
            
            # Quests de dificuldade 2
            Quest(self.screen, {'num': 4, 'dific': 2, 'pergunta':'Which of the phrases below is correct?:', 'r1':'A: Can, let the dog out?', 'r2':'B: Could you lend me a hand?', 'r3':'C: I wish, I can buy this car!', 'r4':'D: I wish, I be able to fly.', 'rcorreta': 2}),
            Quest(self.screen, {'num': 5, 'dific': 2, 'pergunta':'Which one of this phrases is a possibility?', 'r1':'A: I can’t dance very well.', 'r2':'B: I can dance very well.', 'r3':'C: Can I dance very well?', 'r4':'D: I dance very well.', 'rcorreta': 2}),
            Quest(self.screen, {'num': 6, 'dific': 2, 'pergunta':'Which of the phrases is correct:   1.I’s able to dance.,   2.We am able to finish this work in 2 hours!,   3. Are He able to graduate, with those grades?, 4.She’s able to run an entire marathon!', 'r1':'A: 1', 'r2':'B: 2', 'r3':'C: 3', 'r4':'D: 4', 'rcorreta': 4}),
            
            # Quests de dificuldade 3
            Quest(self.screen, {'num': 7, 'dific': 3, 'pergunta':'What type of verb is “be able to”?', 'r1':'A: Action', 'r2':'B: Auxiliary', 'r3':'C: Modal', 'r4':'D: Phrasal', 'rcorreta': 4}),
            Quest(self.screen, {'num': 8, 'dific': 3, 'pergunta':'Which of the phrases down below best illustrates the use of the verb “could”?', 'r1':'A: If she studied more she could have passed the exam', 'r2':'B: He could have chose a better career path.', 'r3':'C: He could have joined the team a year earlier', 'r4':'D: I could have understood the rules, if you explained them', 'rcorreta': 1}),
            Quest(self.screen, {'num': 9, 'dific': 3, 'pergunta':'In which context can we use can?', 'r1':'A: Own', 'r2':'B: Ability', 'r3':'C: Obligation', 'r4':'D: Future Intentions', 'rcorreta': 2})
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

                # Após completar as 3 quests fáceis, inicia o minigame
                if self.current_quest_index == 3:
                    time.sleep(0.5)
                    print('Iniciando o minigame')
                    self.fade_out(1000)  # Fade out in 1 second
                    minigame_result = FruitMinigame(self.screen).run()  # Inicia o mini game

                    if minigame_result == False:  # Se o jogador perder o minigame
                        print('Você perdeu o minigame! Fechando o jogo...')
                        pygame.quit()
                        sys.exit()
                    else:
                        print('Você venceu o minigame! Parando a música e continuando para as quests de dificuldade média...')
                        pygame.mixer.music.stop()  # Parando a música do minigame
                        self.fade_in(1000)  # Fade in in 1 second
                        self.current_quest_index += 1
            else:
                # Se todas as quests e minigames forem completados, encerra o jogo ou continue com outra lógica
                print('Todas as quests foram completadas!')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

Game().run()
