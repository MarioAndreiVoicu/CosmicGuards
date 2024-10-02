import pygame
from config import *

class Player:
    def __init__(self, screen, damage, speed, lives):
        self._img = pygame.image.load("images/spaceship.png")
        self._screen = screen
        self._x = (width - rocket_size) // 2
        self._y = height // 1.25
        self._x_change = 0
        self._damage = damage
        self._speed = speed
        self._lives = lives

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
    def damage(self):
        return self._damage

    @property
    def speed(self):
        return self._speed

    @property
    def lives(self):
        return self._lives

    def change_direction_left(self):
        self.x_change = -1 * self._speed

    def change_direction_right(self):
        self.x_change = self.speed

    def move(self):
        self.x += self.x_change

        if self.x < borderLeft:
            self.x = borderLeft
        elif self.x > borderRight:
            self.x = borderRight

    def stop(self):
        self.x_change = 0

    def display(self):
        self._screen.blit(self._img, (self.x, self.y))

    @x_change.setter
    def x_change(self, value):
        self._x_change = value

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    @damage.setter
    def damage(self, value):
        self._damage = value

    @speed.setter
    def speed(self, value):
        self._speed = value

    @lives.setter
    def lives(self, value):
        self._lives = value

    @img.setter
    def img(self, value):
        self._img = value