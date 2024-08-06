import pygame
import sys

class StarMinigame():
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Pressione ESC para sair do mini game
                        self.running = False

            self.screen.fill((0, 0, 0))  # Preenche a tela com preto
            pygame.draw.circle(self.screen, (255, 255, 255), (400, 300), 50)  # Desenha um círculo branco no centro

            pygame.display.flip()
            self.clock.tick(60)

# Teste do mini game
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    StarMinigame(screen).run()
    pygame.quit()