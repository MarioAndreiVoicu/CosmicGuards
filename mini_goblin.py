import pygame
from config import *

class Mini_goblin1:
    def __init__(self, init_dict, x, y, direction):
        self._img = pygame.image.load("images/mini_goblin1.png")
        self._screen = init_dict["screen"]
        self._x = x
        self._y = y
        self._x_change = init_dict["speed"] * direction
        self._move_distance = init_dict["move_distance"]
        self._speed = init_dict["speed"]
        self._health = init_dict["health"]

    @property
    def img(self):
        return self._img

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def x_change(self):
        return self._x_change

    @property
    def move_distance(self):
        return self._move_distance

    @property
    def speed(self):
        return self._speed

    @property
    def health(self):
        return self._health

    def change_direction_left(self):
        self.x_change = -1 * self._speed

    def change_direction_right(self):
        self.x_change = self.speed

    def move(self):
        self.x += self.x_change

        if self.x <= borderLeft or self.x >= borderRight:
            self.x_change *= -1
            self.y += self.move_distance

    def hit(self):
        return self.y > height // 1.4

    def display(self):
        self._screen.blit(self._img, (self.x, self.y))

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    @x_change.setter
    def x_change(self, value):
        self._x_change = value

    @move_distance.setter
    def move_distance(self, value):
        self._move_distance = value

    @speed.setter
    def speed(self, value):
        self._speed = value

    @health.setter
    def health(self, value):
        self._health = value

class Mini_goblin2:
    def __init__(self, init_dict, x, y, direction):
        self._img = pygame.image.load("images/mini_golbin2.png")
        self._screen = init_dict["screen"]
        self._x = x
        self._y = y
        self._x_change = init_dict["speed"] * direction
        self._move_distance = init_dict["move_distance"]
        self._speed = init_dict["speed"]
        self._health = init_dict["health"]

    @property
    def img(self):
        return self._img

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def x_change(self):
        return self._x_change

    @property
    def move_distance(self):
        return self._move_distance

    @property
    def speed(self):
        return self._speed

    @property
    def health(self):
        return self._health

    def change_direction_left(self):
        self.x_change = -1 * self._speed

    def change_direction_right(self):
        self.x_change = self.speed

    def move(self):
        self.x += self.x_change

        if self.x <= borderLeft or self.x >= borderRight:
            self.x_change *= -1
            self.y += self.move_distance

    def hit(self):
        return self.y > height // 1.4

    def display(self):
        self._screen.blit(self._img, (self.x, self.y))

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    @x_change.setter
    def x_change(self, value):
        self._x_change = value

    @move_distance.setter
    def move_distance(self, value):
        self._move_distance = value

    @speed.setter
    def speed(self, value):
        self._speed = value

    @health.setter
    def health(self, value):
        self._health = value