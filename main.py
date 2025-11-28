import pygame 
import sys
from data.scripts.tilemap import Tilemap
from data.scripts.entities import BallEntity, PaddleEntity
from data.scripts.utils import load_image, get_tile_entities

pygame.init()
pygame.display.set_caption("Pong: Super-Charged")

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((576, 720), pygame.SCALED|pygame.FULLSCREEN)
        self.display = pygame.Surface((288, 360))
        self.clock = pygame.time.Clock()

        self.ball = BallEntity(self,
                               pygame.math.Vector2(100, 100),
                               16,
                               load_image("ball/ball.png"))

        self.paddle1 = PaddleEntity(self, pygame.math.Vector2(120, 300), 1, load_image("paddle/paddle.png"), 1)

        self.movement = [False, False]
        self.tile_entities = []

    def load_tiles(self):
        self.tilemap = Tilemap(self) 
        self.tilemap.divide_tiles()
        self.tilemap.place_level()

    def run(self):
        self.load_tiles()
        press_once_keys = {"f": True}

        while True:
            self.display.fill((255, 215,0, 255))
            self.tilemap.render()

            if (len(self.tile_entities) == 0):
                self.entities = get_tile_entities(self.tilemap.placed_collidable, self)
                self.entities.append(self.paddle1)


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
                    if event.key == pygame.K_f and press_once_keys["f"]:
                        self.ball.force(pygame.math.Vector2(10,0), 45, False)
                        press_once_keys["f"] = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False 
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False 
                    if event.key == pygame.K_f:
                        press_once_keys["f"] = True 

            self.paddle1.move(self.movement)
                    
            self.paddle1.update_and_render()
            self.ball.update_and_render(self.entities)
            pygame.transform.scale(self.display, (576, 720), self.screen)

            pygame.display.update()
            self.clock.tick(60)

game = Game()
game.run()