import pygame
import sys
import random

class GoldenCatMinigame():
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.width, self.height = screen.get_size()

        # Carregar imagem do personagem
        self.character = pygame.transform.scale(pygame.image.load('assets/images/character.png').convert_alpha(), (64, 64))
        self.char_rect = self.character.get_rect(center=(self.width // 2, self.height // 2))
        self.char_mask = pygame.mask.from_surface(self.character)  # Criar máscara para colisão pixel-perfect

        # Carregar imagem da fruta
        self.fruits = []
        fruit_images = ['banana.png', 'cherry.png', 'pineapple.png', 'strawberry.png', 'grape.png', 'watermelon.png']
        self.fruit_names = ['banana', 'cherry', 'pineapple', 'strawberry', 'grape', 'watermelon']
        for fruit_image in fruit_images:
            img = pygame.transform.scale(pygame.image.load(f'assets/images/fruits/{fruit_image}').convert_alpha(), (64, 64))
            while True:
                rect = img.get_rect(center=(random.randint(50, self.width - 50), random.randint(50, self.height - 50)))
                if not self.is_fruit_colliding(rect):
                    break
            self.fruits.append({'image': img, 'rect': rect, 'in_box': False, 'name': self.fruit_names[fruit_images.index(fruit_image)]})

        # Carregar imagem da caixa
        self.box = pygame.transform.scale(pygame.image.load('assets/images/box.png').convert_alpha(), (64, 64))
        self.box_rect = self.box.get_rect(center=(self.width // 2, self.height // 2))

        # Carregar imagem do gato dourado
        self.golden_cat = pygame.transform.scale(pygame.image.load('assets/images/cat.png').convert_alpha(), (64, 64))
        self.cat_rect = self.golden_cat.get_rect(center=(random.randint(50, self.width - 50), random.randint(50, self.height - 50)))

        # Carregar sons
        self.sound_correct = pygame.mixer.Sound('assets/sounds/click_right.mp3')
        self.sound_wrong = pygame.mixer.Sound('assets/sounds/click_wrong.mp3')

        # Tocar música de fundo em loop
        pygame.mixer.music.load('assets/sounds/minigame_track.mp3')
        pygame.mixer.music.play(-1)

        # Carregar fonte para instruções
        self.font = pygame.font.Font('assets/fonts/Pixel.ttf', 24)
        self.font_color = (0, 150, 200)

        # Inicializar tempo de piscar
        self.blink_time = pygame.time.get_ticks()
        self.blink_interval = 500
        self.show_task_text = True

        # Selecionar aleatoriamente uma tarefa para o jogador
        self.current_task = self.generate_new_task()

        # Definir dimensões da caixa de texto da tarefa
        self.task_text_box_rect = pygame.Rect(25, 25, 400, 50)

        # Tarefas completas
        self.tasks_completed = 0

        # Inicializar atributos de coleta de fruta
        self.collected_fruit = None
        self.is_holding_fruit = False

        # Resultado do minigame
        self.minigame_result = False

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_SPACE:
                        if self.is_holding_fruit:
                            self.release_fruit()
                        else:
                            self.try_collect_fruit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.char_rect.x -= 5
            if keys[pygame.K_RIGHT]:
                self.char_rect.x += 5
            if keys[pygame.K_UP]:
                self.char_rect.y -= 5
            if keys[pygame.K_DOWN]:
                self.char_rect.y += 5
            self.char_rect.clamp_ip(self.screen.get_rect())

            # Atualizar a visibilidade da caixa de texto da tarefa
            current_time = pygame.time.get_ticks()
            if current_time - self.blink_time > self.blink_interval:
                self.blink_time = current_time
                self.show_task_text = not self.show_task_text

            # Verificar se todas as tarefas foram concluídas
            if self.tasks_completed == 6:
                self.minigame_result = True
                self.running = False

            # Desenhar o frame
            self.draw_frame()

            # Mostrar a tarefa atual
            if self.show_task_text and self.current_task:
                self.draw_text_box(self.current_task["description"], 25, 25, True)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.mixer.music.stop()
        return self.minigame_result

    def check_collision(self, mask1, rect1, mask2, rect2):
        """Verificar colisão pixel-perfect."""
        offset = (rect2.x - rect1.x, rect2.y - rect1.y)
        return mask1.overlap(mask2, offset) is not None

    def draw_text_box(self, texto, x, y, is_task_text):
        """Desenhar uma caixa de texto com bordas estilizadas."""
        if is_task_text and not self.show_task_text:
            return
        
        quest_box = pygame.Rect(x, y, len(str(texto)) * 24 + 20, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), quest_box)
        pygame.draw.rect(self.screen, self.font_color, quest_box, 6)
        pygame.draw.rect(self.screen, (200, 200, 0), quest_box, 3)
        texto_surface = self.font.render(texto, False, self.font_color)
        self.screen.blit(texto_surface, (quest_box.left + 10, quest_box.centery - quest_box.height / 4))

    def draw_frame(self):
        background = pygame.image.load('assets/images/background_1.png').convert_alpha()
        background = pygame.transform.scale(background, (400, 400))

        # Desenhar o fundo em mosaico
        for x in range(0, self.width, background.get_width()):
            for y in range(0, self.height, background.get_height()):
                self.screen.blit(background, (x, y))

        # Desenhar a caixa no centro da tela
        self.screen.blit(self.box, self.box_rect)

        # Desenhar as frutas
        for fruit in self.fruits:
            if self.collected_fruit != fruit and not fruit['in_box']:
                self.screen.blit(fruit['image'], fruit['rect'])

        # Desenhar o personagem
        self.screen.blit(self.character, self.char_rect) 

        # Desenhar a fruta segurada pelo personagem
        if self.is_holding_fruit and self.collected_fruit:
            fruit_rect = self.collected_fruit['rect'].copy()
            fruit_rect.center = (self.char_rect.center[0], self.char_rect.center[1] + 10)  # Centralizar a fruta nas mãos do personagem
            self.screen.blit(self.collected_fruit['image'], fruit_rect)

        # Desenhar o gato dourado
        self.screen.blit(self.golden_cat, self.cat_rect)

    def generate_new_task(self):
        """Gerar uma nova tarefa aleatória, incluindo 30% das tarefas para alimentar o gato."""
        available_fruits = [fruit for fruit in self.fruits if not fruit['in_box']]
        if not available_fruits:
            return None  # Se todas as frutas estiverem na caixa, não há nova tarefa

        choice_random = random.randint(1, 2)

        if choice_random == 1:  # 30% chance de alimentar o gato
            fruit = random.choice(available_fruits)
            task = {"description": f"Pick up the {fruit['name']} and feed it to the cat!", "target_fruit": fruit, "action": "feed_cat"}
        else:
            fruit = random.choice(available_fruits)
            task = {"description": f"Pick up the {fruit['name']} and place it in the box!", "target_fruit": fruit, "action": "place_in_box"}

        return task

    def try_collect_fruit(self):
        """Tentar pegar uma fruta."""
        for fruit in self.fruits:
            if self.char_rect.colliderect(fruit['rect']) and not self.is_holding_fruit and not fruit['in_box']:
                self.collected_fruit = fruit
                self.is_holding_fruit = True
                break

    def release_fruit(self):
        """Soltar a fruta, colocando-a na caixa ou alimentando o gato."""
        if self.is_holding_fruit and self.current_task:
            if self.current_task['action'] == 'place_in_box' and self.check_collision(pygame.mask.from_surface(self.character), self.char_rect, pygame.mask.from_surface(self.box), self.box_rect):
                if self.collected_fruit == self.current_task['target_fruit']:
                    self.collected_fruit['rect'].center = self.box_rect.center  # Colocar a fruta na caixa
                    self.collected_fruit['in_box'] = True  # Marcar a fruta como dentro da caixa
                    self.sound_correct.play()
                    self.tasks_completed += 1  # Marcar como tarefa concluída
                    self.current_task = self.generate_new_task()  # Gerar nova tarefa
                else:
                    self.sound_wrong.play()
            elif self.current_task['action'] == 'feed_cat' and self.check_collision(pygame.mask.from_surface(self.character), self.char_rect, pygame.mask.from_surface(self.golden_cat), self.cat_rect):
                if self.collected_fruit == self.current_task['target_fruit']:
                    self.sound_correct.play()
                    self.tasks_completed += 1  # Marcar como tarefa concluída
                    self.fruits.remove(self.collected_fruit)  # Remover a fruta da lista
                    self.current_task = self.generate_new_task()  # Gerar nova tarefa
                else:
                    self.sound_wrong.play()
            else:
                self.sound_wrong.play()
            
            self.is_holding_fruit = False
            self.collected_fruit = None

    def is_fruit_colliding(self, new_fruit_rect):
        """Verificar se a nova fruta colide com alguma fruta existente."""
        for fruit in self.fruits:
            if new_fruit_rect.colliderect(fruit['rect']):
                return True
        return False
