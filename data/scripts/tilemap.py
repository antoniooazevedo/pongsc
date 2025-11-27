import pygame
from .utils import load_image, load_level


class Tilemap:
    """
    A class to manage and render tilemaps from a spritesheet.
    This class handles loading a spritesheet, dividing it into individual tiles,
    placing tiles according to level data, and rendering the tilemap to the display.
    Attributes:
        game: The game instance that contains the display and other game state.
        ss: The loaded spritesheet image containing all tile graphics.
        level: The level data loaded from JSON, defining tile placement.
        loaded_tiles (dict): Dictionary mapping tile coordinates to tile surfaces.
        tilesize (int): The size of each tile in pixels (default 16).
        tiles (dict): Dictionary mapping world coordinates to tile surfaces for rendering.
    """

    """
        Initialize the Tilemap with game reference and load necessary resources.
        Args:
            game: The game instance that provides access to display and other components.
    """
    def __init__(self, game):
        self.game = game
        self.ss = load_image("ss.png")
        self.level = load_level("level.json")
        self.loaded_tiles = dict() 
        self.collidable_tiles = dict()
        self.placed_collidable = []
        self.tilesize = 16
        self.tiles = dict() 

        self.first_render_pass = True

    """
       Divide the spritesheet into individual tile surfaces.
       Iterates through the spritesheet in tilesize chunks and stores non-transparent
       tiles in the loaded_tiles dictionary. Tiles that are completely transparent
       (alpha = 0 for all pixels) are skipped.
       The tiles are stored with keys in the format "row;col" based on their position
       in the spritesheet.
    """
    def divide_tiles(self):
        for col in range(int(self.ss.get_height() / self.tilesize)): 
            for row in range(int(self.ss.get_width() / self.tilesize)):
                tile = self.ss.subsurface((row * self.tilesize, col * self.tilesize, self.tilesize, self.tilesize))
                if tile.get_at((0, 0)).a == 0 and all(tile.get_at((x, y)).a == 0 for x in range(self.tilesize) for y in range(self.tilesize)):
                    continue
                self.loaded_tiles[f"{row};{col}"] = tile
        
        self.set_collidable_tiles()


    def set_collidable_tiles(self):
        for key in self.loaded_tiles.keys():
            x = int(key.split(";")[0])
            y = int(key.split(";")[1])

            if (y >= 2 and y <=4 and x >= 0 and x <= 2) and not (x == 1 and y == 3):
                self.collidable_tiles[key] = True
            else:
                self.collidable_tiles[key] = False 

        
    """
    Place tiles according to the loaded level data.
    Reads the level data and maps tile keys from the level definition to actual
    tile surfaces from loaded_tiles. The tiles are positioned with an offset of
    (3, 1) from their level data coordinates.
    The placed tiles are stored in the tiles dictionary with keys in the format
    "x;y" representing their world coordinates.
    """
    def place_level(self):
        for level_data in self.level.values():
            for y, row in enumerate(level_data):
                for x, tile_key in enumerate(row):
                    self.tiles[f"{x+3};{y+1}"] = tile_key

    
    """
    Render all placed tiles to the game display.
    Iterates through all tiles in the tiles dictionary and blits them to the
    game display at their corresponding world coordinates. Each tile's position
    is calculated by multiplying its grid coordinates by the tilesize.
    Prints debug information showing each tile and its screen coordinates.
    """
    def render(self):
        s_coords = lambda x,y: (x*self.tilesize, y*self.tilesize) 

        for key, tile_key in self.tiles.items():
            x = int(key.split(";")[0])
            y = int(key.split(";")[1])

            self.game.display.blit(self.loaded_tiles[tile_key], s_coords(x,y))

            if (self.first_render_pass and self.collidable_tiles[tile_key]):
                self.placed_collidable.append(pygame.Rect(*s_coords(x,y), self.tilesize, self.tilesize))

        self.first_render_pass = False