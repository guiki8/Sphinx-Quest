import pygame
import sys
import random
import os
from pygame import mixer

class FruitMinigame():
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.width, self.height = screen.get_size()

        # Load character image
        self.character = pygame.transform.scale(pygame.image.load('assets/images/character.png').convert_alpha(), (64, 64))
        self.char_rect = self.character.get_rect(center=(self.width // 2, self.height // 2))

        # Load fruits images
        self.fruit_images = {
            'grape': pygame.transform.scale(pygame.image.load('assets/images/fruits/grape.png').convert_alpha(), (64, 64)),
            'cherry': pygame.transform.scale(pygame.image.load('assets/images/fruits/cherry.png').convert_alpha(), (64, 64)),
            'frutas': []
        }
        fruit_files = os.listdir('assets/images/fruits/')
        for fruit_file in fruit_files:
            if fruit_file not in ['grape.png', 'cherry.png']:
                fruit_image = pygame.transform.scale(pygame.image.load(f'assets/images/fruits/{fruit_file}').convert_alpha(), (64, 64))
                self.fruit_images['frutas'].append(fruit_image)

        self.fruits = self.randomize_fruits()

        # Load sounds
        self.sound_correct = pygame.mixer.Sound('assets/sounds/click_right.mp3')
        self.sound_wrong = pygame.mixer.Sound('assets/sounds/click_wrong.mp3')

        # Play background music in loop
        pygame.mixer.music.load('assets/sounds/minigame_track.mp3')
        pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely

        self.font_color = (0, 150, 200)
        self.font_size = 25
        self.fonte = pygame.font.Font('assets/fonts/Pixel.ttf', self.font_size)
        self.fonte_bold = pygame.font.Font('assets/fonts/PixelBold.ttf', self.font_size)
        self.font_width = self.font_size * 0.3

        # Timer for blinking text box
        self.blink_timer = 0
        self.show_text_box = True

    def randomize_fruits(self):
        fruits = []
        num_uvas = random.randint(1, 3)  # Number of grapes
        num_fruits = 10  # Total number of fruits

        # Ensure we don't place more fruits than possible
        while num_fruits > 0:
            fruit_type = 'grape' if num_uvas > 0 else random.choice(['cherry', 'frutas'])
            if fruit_type == 'frutas':
                fruit_image = random.choice(self.fruit_images['frutas'])
            else:
                fruit_image = self.fruit_images[fruit_type]
            
            # Generate fruit position and check for overlap with other fruits
            placed = False
            while not placed:
                fruit_rect = fruit_image.get_rect(center=(random.randint(50, self.width - 50), random.randint(50, self.height - 50)))
                overlap = False
                for _, rect, _ in fruits:
                    if fruit_rect.colliderect(rect):
                        overlap = True
                        break
                if not overlap and not fruit_rect.colliderect(self.char_rect):
                    fruits.append((fruit_image, fruit_rect, fruit_type))
                    num_fruits -= 1
                    if fruit_type == 'grape':
                        num_uvas -= 1
                    placed = True
        
        return fruits

    def draw_text_box(self):
        quest_box = pygame.Rect(300, 20, len('Get the Grape!!') * (self.font_size - self.font_width) + self.font_width, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), quest_box)
        pygame.draw.rect(self.screen, self.font_color, quest_box, 6)
        pygame.draw.rect(self.screen, (200, 200, 0), quest_box, 3)
        texto = self.fonte.render('Get the Grape!!', False, self.font_color)
        self.screen.blit(texto, (quest_box.left + self.font_width, quest_box.centery - quest_box.height / 4))

    def pixel_collision(self, rect1, image1, rect2, image2):
        # Create masks from the surfaces
        mask1 = pygame.mask.from_surface(image1)
        mask2 = pygame.mask.from_surface(image2)
        
        # Calculate the overlap rectangle
        overlap_rect = rect1.clip(rect2)
        if overlap_rect.width == 0 or overlap_rect.height == 0:
            return False
        
        # Calculate offset for mask overlap
        offset = (overlap_rect.left - rect2.left, overlap_rect.top - rect2.top)
        
        # Check if masks overlap
        if mask1.overlap(mask2, offset):
            return True
        return False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.char_rect.x -= 5
            if keys[pygame.K_RIGHT]:
                self.char_rect.x += 5
            if keys[pygame.K_UP]:
                self.char_rect.y -= 5
            if keys[pygame.K_DOWN]:
                self.char_rect.y += 5

            # Restrict movement to screen bounds
            self.char_rect.clamp_ip(self.screen.get_rect())

            background = pygame.image.load('assets/images/background_1.png').convert_alpha()
            background = pygame.transform.scale(background, (400, 400))

            # Draw the tiled background
            for x in range(0, self.width, 400):
                for y in range(0, self.height, 400):
                    self.screen.blit(background, (x, y))

            # Draw fruits and check for collision
            for fruit_image, fruit_rect, fruit_type in self.fruits:
                self.screen.blit(fruit_image, fruit_rect)
                if self.pixel_collision(self.char_rect, self.character, fruit_rect, fruit_image):
                    if fruit_type == 'grape':
                        self.sound_correct.play()
                        print("You got a grape!")
                        return True
                    else:
                        self.sound_wrong.play()
                        print(f"You touched a {fruit_type}!")
                        pygame.time.delay(1000)  # Adiciona um atraso de 1000ms para garantir que o som toque completamente
                        return False

            # Draw the character
            self.screen.blit(self.character, self.char_rect)

            # Blinking text box
            self.blink_timer += self.clock.get_time()
            if self.blink_timer >= 300:  # 0.3 seconds
                self.show_text_box = not self.show_text_box
                self.blink_timer = 0

            if self.show_text_box:
                self.draw_text_box()

            pygame.display.flip()
            self.clock.tick(60)

# Teste do mini game
if __name__ == "__main__":
    pygame.init()
    mixer.init()
    screen = pygame.display.set_mode((800, 600))
    FruitMinigame(screen).run()
    pygame.quit()
