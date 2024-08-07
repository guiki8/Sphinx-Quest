import pygame
import sys
import random
import os

class FruitMinigame():
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.width, self.height = screen.get_size()

        # Load character image
        self.character = pygame.transform.scale(pygame.image.load('assets/images/character.png').convert_alpha(), (64, 64))
        self.char_rect = self.character.get_rect(center=(self.width//2, self.height//2))
        self.char_mask = pygame.mask.from_surface(self.character)

        # Load background image
        self.background = pygame.image.load('assets/images/background_1.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (400, 400))

        # Load fruits images and resize to 64x64
        self.fruit_images = {
            'uva': pygame.transform.scale(pygame.image.load('assets/images/fruits/uva.png').convert_alpha(), (64, 64)),
            'cherrie': pygame.transform.scale(pygame.image.load('assets/images/fruits/cherrie.png').convert_alpha(), (64, 64)),
            'other': []
        }
        fruit_files = os.listdir('assets/images/fruits/')
        for fruit_file in fruit_files:
            if fruit_file not in ['uva.png', 'cherrie.png']:
                fruit_image = pygame.transform.scale(pygame.image.load(f'assets/images/fruits/' + fruit_file).convert_alpha(), (64, 64))
                self.fruit_images['other'].append(fruit_image)

        self.fruits = self.randomize_fruits()

    def randomize_fruits(self):
        fruits = []
        num_uvas = random.randint(1, 3)
        for _ in range(num_uvas):  # Add 1-3 uvas
            fruit_image = self.fruit_images['uva']
            fruit_rect = self.get_non_colliding_rect(fruit_image)
            fruit_mask = pygame.mask.from_surface(fruit_image)
            fruits.append((fruit_image, fruit_rect, 'uva', fruit_mask))

        while len(fruits) < 10:  # Add random fruits until there are 10
            fruit_type = random.choice(['cherrie', 'other'])
            if fruit_type == 'other':
                fruit_image = random.choice(self.fruit_images['other'])
            else:
                fruit_image = self.fruit_images[fruit_type]
            fruit_rect = self.get_non_colliding_rect(fruit_image)
            fruit_mask = pygame.mask.from_surface(fruit_image)
            fruits.append((fruit_image, fruit_rect, fruit_type, fruit_mask))
        return fruits

    def get_non_colliding_rect(self, fruit_image):
        while True:
            fruit_rect = fruit_image.get_rect(
                center=(random.randint(50, self.width-50), random.randint(50, self.height-50)))
            if not fruit_rect.colliderect(self.char_rect.inflate(128, 128)):
                return fruit_rect

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
            if keys[pygame.K_a]:
                self.char_rect.x -= 5
            if keys[pygame.K_d]:
                self.char_rect.x += 5
            if keys[pygame.K_w]:
                self.char_rect.y -= 5
            if keys[pygame.K_s]:
                self.char_rect.y += 5

            # Fill the screen with the repeated background
            for x in range(0, self.width, 400):
                for y in range(0, self.height, 400):
                    self.screen.blit(self.background, (x, y))

            # Draw fruits
            for fruit_image, fruit_rect, fruit_type, fruit_mask in self.fruits:
                self.screen.blit(fruit_image, fruit_rect)
                offset = (fruit_rect.x - self.char_rect.x, fruit_rect.y - self.char_rect.y)
                if self.char_mask.overlap(fruit_mask, offset):
                    if fruit_type == 'cherrie':
                        print("You died!")
                        self.running = False
                    elif fruit_type == 'uva':
                        print("You won!")
                        self.running = False
                    else:  # Other fruits
                        print("You died!")
                        self.running = False

            # Draw character
            self.screen.blit(self.character, self.char_rect)

            pygame.display.flip()
            self.clock.tick(60)

# Teste do mini game
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    FruitMinigame(screen).run()
    pygame.quit()
