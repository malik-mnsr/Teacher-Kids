import pygame
from random import choice

class Agent:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen, tile_size):

        pygame.draw.circle(screen, self.color, (self.x * tile_size + tile_size // 2, self.y * tile_size + tile_size // 2), tile_size // 4)

    def move(self, dx, dy, cols, rows):

        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < cols and 0 <= new_y < rows:
            self.x, self.y = new_x, new_y
