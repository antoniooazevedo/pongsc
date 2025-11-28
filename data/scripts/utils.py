import pygame
import json
from .entities import TileEntity

ASSETS_PATH = "data/assets/"

def load_image(path):
    return pygame.image.load(ASSETS_PATH + path).convert_alpha()

def load_level(path):
    with open(ASSETS_PATH + path, 'r') as f:
        return json.load(f)

def get_tile_entities(tiles, game):
    tile_entities = []
    for tile in tiles:
        tile_entities.append(TileEntity(game, (tile.x, tile.y), tile.width, tile))

    return tile_entities
