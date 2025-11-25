import pygame 
import sys
from data.scripts.tilemap import Tilemap

pygame.init()
pygame.display.set_caption("Pong: Super-Charged")

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((576, 720), pygame.SCALED|pygame.FULLSCREEN)
        self.display = pygame.Surface((288, 360))
        self.clock = pygame.time.Clock()

        self.movement = [False, False]
        self.img = pygame.image.load("data/assets/ball/ball.png").convert_alpha()
        self.img_pos = [100, 100]

    def load_tiles(self):
        self.tilemap = Tilemap(self) 
        self.tilemap.divide_tiles()
        self.tilemap.place_level()

    def run(self):
        self.load_tiles()

        while True:
            self.display.fill((255, 215,0, 255))
            self.tilemap.render()

            self.img_pos[0] += (self.movement[1] - self.movement[0])
            self.display.blit(self.img, (self.img_pos[0], self.img_pos[1]))

            pygame.transform.scale(self.display, (576, 720), self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False 
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False 

            pygame.display.update()
            self.clock.tick(60)

game = Game()
game.run()