import pygame
import sys
import random

class TargetMinigame():
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.width, self.height = screen.get_size()

        # Carregar imagem do personagem
        self.character = pygame.transform.scale(pygame.image.load('assets/images/character.png').convert_alpha(), (64, 64))
        self.char_rect = self.character.get_rect(center=(self.width // 2, self.height // 2))
        self.char_mask = pygame.mask.from_surface(self.character)  # Criar máscara para colisão pixel-perfect

        # Carregar imagem da pedra
        self.rock_img = pygame.transform.scale(pygame.image.load('assets/images/targets/rock.png').convert_alpha(), (128, 128))
        self.rock_shot_img = pygame.transform.scale(pygame.image.load('assets/images/targets/ammo.png').convert_alpha(), (32, 32))  # Imagem da pedra atirada
        self.rocks_on_ground = []  # Lista para armazenar pedras no chão
        self.collected_rocks = []  # Lista para armazenar pedras coletadas

        # Carregar imagens dos alvos
        self.targets = []
        colors = ['blue', 'green', 'red', 'yellow']
        for color in colors:
            target_img = pygame.transform.scale(pygame.image.load(f'assets/images/targets/{color}_target.png').convert_alpha(), (96, 96))
            target_rect = target_img.get_rect(center=(random.randint(50, self.width - 50), random.randint(50, self.height - 50)))
            target_mask = pygame.mask.from_surface(target_img)  # Criar máscara para cada alvo
            shape = 'square' if color in ['blue', 'yellow'] else 'round'
            self.targets.append({'image': target_img, 'rect': target_rect, 'mask': target_mask, 'color': color, 'shape': shape})

        # Carregar sons
        self.sound_correct = pygame.mixer.Sound('assets/sounds/click_right.mp3')
        self.sound_wrong = pygame.mixer.Sound('assets/sounds/click_wrong.mp3')

        # Tocar música de fundo em loop
        pygame.mixer.music.load('assets/sounds/minigame_track.mp3')
        pygame.mixer.music.play(-1)  # -1 faz a música tocar em loop indefinidamente

        self.last_direction = 'down'  # Inicializar com uma direção padrão

        # Carregar imagem da seta
        self.arrow = pygame.transform.scale(pygame.image.load('assets/images/arrow.png').convert_alpha(), (32, 32))

        # Carregar fonte para contagem de pedras e instruções da tarefa
        self.font = pygame.font.Font('assets/fonts/Pixel.ttf', 24)
        self.font_color = (0, 150, 200)  # Cor padrão da fonte
        self.font_size = 25
        self.font_width = 8

        # Inicializar tempo de piscar
        self.blink_time = pygame.time.get_ticks()
        self.blink_interval = 500  # Intervalo de piscar em milissegundos
        self.show_task_text = True

        # Selecionar aleatoriamente uma tarefa para o jogador
        self.current_task = self.generate_new_task()

        # Definir dimensões da caixa de texto da tarefa
        self.task_text_box_rect = pygame.Rect(25, 25, 400, 50)

        # Tasks completas
        self.tasks_completed = 0
        self.game_conclued = 0

    def run(self):
       while self.running:
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()
               if event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_ESCAPE:
                       self.running = False
                   if event.key == pygame.K_SPACE and self.collected_rocks:  # Atirar uma pedra
                       self.shoot_rock()
           keys = pygame.key.get_pressed()
           if keys[pygame.K_LEFT]:
               self.char_rect.x -= 5
               self.last_direction = 'left'
           if keys[pygame.K_RIGHT]:
               self.char_rect.x += 5
               self.last_direction = 'right'
           if keys[pygame.K_UP]:
               self.char_rect.y -= 5
               self.last_direction = 'up'
           if keys[pygame.K_DOWN]:
               self.char_rect.y += 5
               self.last_direction = 'down'
           # Restringir movimento aos limites da tela
           self.char_rect.clamp_ip(self.screen.get_rect())
           # Spawn de pedras no chão
           if random.random() < 0.01:  # Chance aleatória para spawn de uma pedra
               rock_rect = self.rock_img.get_rect(center=(random.randint(50, self.width - 50), random.randint(50, self.height - 50)))
               rock_mask = pygame.mask.from_surface(self.rock_img)  # Criar máscara para a pedra
               self.rocks_on_ground.append({'image': self.rock_img, 'rect': rock_rect, 'mask': rock_mask})
           # Verificar colisão com pedras e coletá-las
           for rock in self.rocks_on_ground[:]:
               if self.check_collision(self.char_mask, self.char_rect, rock['mask'], rock['rect']):
                   self.collected_rocks.append(rock)  # Adicionar às pedras coletadas
                   self.rocks_on_ground.remove(rock)  # Remover das pedras no chão
           # Atualizar a visibilidade da caixa de texto da tarefa
           current_time = pygame.time.get_ticks()
           if current_time - self.blink_time > self.blink_interval:
               self.blink_time = current_time
               self.show_task_text = not self.show_task_text
           if self.game_conclued == 1:
               return True
           if self.game_conclued == 2:
               return False
           self.draw_frame()
           pygame.display.flip()
           self.clock.tick(60)

    def check_collision(self, mask1, rect1, mask2, rect2):
        """Verificar colisão pixel-perfect."""
        offset = (rect2.x - rect1.x, rect2.y - rect1.y)
        return mask1.overlap(mask2, offset) is not None

    def check_task_completion(self, target):
        """Verificar se a tarefa foi completada corretamente."""
        if "target_color" in self.current_task:
            if target['color'] == self.current_task["target_color"]:
                self.sound_correct.play()
                self.tasks_completed += 1
                if self.tasks_completed == 3:
                    self.game_conclued = 1
                else:
                    self.current_task = self.generate_new_task()  # Gerar nova tarefa
            else:
                self.sound_wrong.play()
                self.game_conclued = 2
        elif "target_shape" in self.current_task:
            if self.current_task["target_shape"] == target['shape']:
                self.sound_correct.play()
                self.current_task = self.generate_new_task()  # Gerar nova tarefa
            else:
                self.sound_wrong.play()

    def shoot_rock(self):
        rock = self.collected_rocks.pop(0)  # Remover a primeira pedra coletada da lista
        rock_rect = self.rock_shot_img.get_rect(center=self.char_rect.center)  # Começar a pedra na posição do personagem
        rock_mask = pygame.mask.from_surface(self.rock_shot_img)
    
        direction = self.last_direction  # Obter a última direção de movimento
    
        # Determinar o passo de movimento para a pedra
        step_x, step_y = 0, 0
        if direction == 'left':
            step_x = -5
        elif direction == 'right':
            step_x = 5
        elif direction == 'up':
            step_y = -5
        elif direction == 'down':
            step_y = 5
    
        # Movimentar a pedra na direção correta
        while rock_rect.colliderect(self.screen.get_rect()):
            self.draw_frame()  # Desenhar tudo antes de mover a pedra
            rock_rect.move_ip(step_x, step_y)  # Mover pedra na última direção
            self.screen.blit(self.rock_shot_img, rock_rect)
            pygame.display.flip()
            self.clock.tick(60)
            for target in self.targets:
                if self.check_collision(rock_mask, rock_rect, target['mask'], target['rect']):
                    self.check_task_completion(target)  # Verificar se o alvo atingido corresponde à tarefa
                    # Reposicionar o alvo atingido em uma nova posição aleatória
                    target['rect'].center = (random.randint(50, self.width - 50), random.randint(50, self.height - 50))
                    return  # Parar a função após um acerto

    def draw_arrow(self):
        """Desenhar a seta ao lado do personagem."""
        if self.last_direction == 'left':
            arrow_rotated = pygame.transform.rotate(self.arrow, 90)
            arrow_pos = (self.char_rect.left - 32, self.char_rect.centery - 16)
        elif self.last_direction == 'right':
            arrow_rotated = pygame.transform.rotate(self.arrow, -90)
            arrow_pos = (self.char_rect.right, self.char_rect.centery - 16)
        elif self.last_direction == 'up':
            arrow_rotated = self.arrow
            arrow_pos = (self.char_rect.centerx - 16, self.char_rect.top - 32)
        else:  # direction == 'down'
            arrow_rotated = pygame.transform.rotate(self.arrow, 180)
            arrow_pos = (self.char_rect.centerx - 16, self.char_rect.bottom)

        self.screen.blit(arrow_rotated, arrow_pos)

    def draw_text_box(self, texto, x, y, is_task_text):
        """Desenhar uma caixa de texto com bordas estilizadas."""
        if is_task_text and not self.show_task_text:
            return
        
        quest_box = pygame.Rect(x, y, len(str(texto)) * (self.font_size - self.font_width) + self.font_width, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), quest_box)
        pygame.draw.rect(self.screen, self.font_color, quest_box, 6)
        pygame.draw.rect(self.screen, (200, 200, 0), quest_box, 3)
        texto_surface = self.font.render(texto, False, self.font_color)
        self.screen.blit(texto_surface, (quest_box.left + self.font_width, quest_box.centery - quest_box.height / 4))

    def draw_frame(self):
        background = pygame.image.load('assets/images/background_1.png').convert_alpha()
        background = pygame.transform.scale(background, (400, 400))

        # Desenhar o fundo em mosaico
        for x in range(0, self.width, background.get_width()):
            for y in range(0, self.height, background.get_height()):
                self.screen.blit(background, (x, y))

        # Desenhar os alvos
        for target in self.targets:
            self.screen.blit(target['image'], target['rect'])

        # Desenhar as pedras no chão
        for rock in self.rocks_on_ground:
            self.screen.blit(rock['image'], rock['rect'])

        # Desenhar o personagem
        self.screen.blit(self.character, self.char_rect)

        # Desenhar seta indicando direção do personagem
        self.draw_arrow()

        # Desenhar caixa de texto da tarefa
        self.draw_text_box(self.current_task["description"], self.task_text_box_rect.x, self.task_text_box_rect.y, True)

        # Desenhar caixa de texto da contagem de pedras
        rock_count_text = f"Rocks: {len(self.collected_rocks)}"
        self.draw_text_box(rock_count_text, 25, self.height - 60, False)  # Não piscar a caixa de texto da contagem de pedras

    def generate_new_task(self):
        """Gerar uma nova tarefa aleatória."""
        tasks = [
            {"description": "Hit the blue target!", "target_color": "blue"},
            {"description": "Hit the sky's color target!", "target_color": "blue"},
            {"description": "Hit the green target!", "target_color": "green"},
            {"description": "Don't hit the blue, red or yellow target!", "target_color": "green"},
            {"description": "Hit the red target!", "target_color": "red"},
            {"description": "Don't hit a yellow, blue or green target!", "target_color": "red"},
            {"description": "Hit the yellow target", "target_color": "yellow"},
            {"description": "Hit a round target!", "target_shape": "round"},
            {"description": "Hit a target that isn't square!", "target_shape": "round"},
            {"description": "Hit a square target!", "target_shape": "square"},
        ]
        return random.choice(tasks)

# Inicializar Pygame e criar uma tela
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Minigame de Alvos')
    game = TargetMinigame(screen)
    game.run()