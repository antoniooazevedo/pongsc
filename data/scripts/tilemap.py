import pygame
from .utils import load_image, load_level


class Tilemap:
    def __init__(self, game):
        self.game = game
        self.ss = load_image("ss.png")
        self.level = load_level("level.json")
        self.loaded_tiles = dict() 
        self.tilesize = 16
        self.tiles = dict() 

    def divide_tiles(self):
        for col in range(int(self.ss.get_height() / self.tilesize)): 
            for row in range(int(self.ss.get_width() / self.tilesize)):
                tile = self.ss.subsurface((row * self.tilesize, col * self.tilesize, self.tilesize, self.tilesize))
                if tile.get_at((0, 0)).a == 0 and all(tile.get_at((x, y)).a == 0 for x in range(self.tilesize) for y in range(self.tilesize)):
                    continue
                self.loaded_tiles[f"{row};{col}"] = tile

        print(self.loaded_tiles.keys())
        
    def place_level(self):
        for level_data in self.level.values():
            for y, row in enumerate(level_data):
                for x, tile_key in enumerate(row):
                    self.tiles[f"{x+3};{y+1}"] = self.loaded_tiles[tile_key] 

    
    def render(self):
        s_coords = lambda x,y: (x*self.tilesize, y*self.tilesize) 

        for key,tile in self.tiles.items():
            x = int(key.split(";")[0])
            y = int(key.split(";")[1])

            print(f"{tile} --> {s_coords(x,y)}")
            self.game.display.blit(tile, s_coords(x,y))