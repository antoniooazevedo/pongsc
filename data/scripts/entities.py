import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.size = size
        self.type = e_type
        self.pos = list(pos)

        self.velocity = (0,0)
