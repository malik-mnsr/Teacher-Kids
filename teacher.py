# teacher.py
import pygame
from random import choice
from agent import Agent

class Teacher(Agent):
    def __init__(self, x, y):
        super().__init__(x, y, pygame.Color('blue'))

    def move(self, cols, rows):

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        direction = choice(directions)
        super().move(*direction, cols, rows)
