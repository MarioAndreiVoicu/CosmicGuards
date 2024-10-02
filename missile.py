import pygame
from config import *

class Missile():
    def __init__(self, screen, player_x, player_y):
        self._screen = screen
        self._missile_img = pygame.image.load("images/missile.png")
        self._x = player_x
        self._y = player_y
        self._is_fired = False
        self._speed = missile_speed


    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def speed(self):
        return self._speed

    @property
    def is_fired(self):
        return self._is_fired

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    @is_fired.setter
    def is_fired(self, value):
        self._is_fired = value

    @speed.setter
    def speed(self, value):
        self._speed = value

    def fire(self, player_x, player_y):
        missile_sound.play()
        self.is_fired = True
        self.x = player_x
        self.y = player_y

    def display(self):
        self._screen.blit(missileImg, (self.x + rocket_size // 4, self.y + rocket_size // 15))