import pygame
import json

ASSETS_PATH = "data/assets/"

def load_image(path):
    return pygame.image.load(ASSETS_PATH + path).convert_alpha()

def load_level(path):
    with open(ASSETS_PATH + path, 'r') as f:
        return json.load(f)
