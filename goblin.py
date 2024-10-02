import pygame
import random
from config import *

class Goblin:
    def __init__(self, init_dict):
        self._img = pygame.image.load("images/goblin.png")
        self._screen = init_dict["screen"]
        self._x = (width - rocket_size)//2
        self._y = height//10
        self._speed = init_dict["speed"]
        self._x_change = init_dict["speed"] * random.choice([-1, 1])
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
    def damage(self):
        return self._damage

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

        if self.x <= borderLeft or self.x >= borderRightBoss:
            self.x_change *= -1

    def spear_throw(self, spear_throw):
        spear_throw.active = True

    def potion_throw(self, potion_throw):
        potion_throw.active = True

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

    @damage.setter
    def damage(self, value):
        self._damage = value

    @speed.setter
    def speed(self, value):
        self._speed = value

    @health.setter
    def health(self, value):
        self._health = value


class Spear_throw:
    def __init__(self, screen, goblin):
        self._screen = screen
        self._image = pygame.image.load("images/spear.png")
        self._x = goblin.x
        self._y = goblin.y
        self._speed = spear_throw_speed
        self._active = False
        self._goblin = goblin

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
    def active(self):
        return self._active

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    @speed.setter
    def speed(self, value):
        self._speed = value

    @active.setter
    def active(self, value):
        self._active = value

    def activate(self, goblin):
        throw_sound.play()
        self.active = True
        self.x = goblin.x
        self.y = goblin.y + goblin_size // 2

    def move(self):
        if self.active:
            self.y += self.speed
        if self.y > height + spear_throw_size:
            self.active = False
            self.y = self._goblin.y

    def display(self):
        if self.active:
            self._screen.blit(self._image, (self.x, self.y))

    def collision(self, player):
        if self.active:

            player_rect = pygame.Rect(player.x, player.y, player.img.get_width(), player.img.get_height())
            spear_width = 50
            spear_height = self._image.get_height()
            spear_x = self.x + (self._image.get_width() - spear_width) // 2
            attack_rect = pygame.Rect(spear_x, self.y, spear_width, spear_height)

            if player_rect.colliderect(attack_rect):
                self.active = False
                return True
            else:
                return False
        else:
            return False

class Potion_throw:
    def __init__(self, screen, goblin):
        self._screen = screen
        self._image = pygame.image.load("images/potion_throw.png")
        self._x = goblin.x
        self._y = goblin.y
        self._speed = potion_throw_speed
        self._active = False
        self._goblin = goblin

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
    def active(self):
        return self._active

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    @speed.setter
    def speed(self, value):
        self._speed = value

    @active.setter
    def active(self, value):
        self._active = value

    def activate(self, goblin):
        throw_sound.play()
        self.active = True
        self.x = goblin.x
        self.y = goblin.y + goblin_size // 2

    def move(self):
        if self.active:
            self.y += self.speed
        if self.y > height + potion_throw_size:
            self.active = False
            self.y = self._goblin.y

    def display(self):
        if self.active:
            self._screen.blit(self._image, (self.x, self.y))

    def collision(self, player):
        if self.active:
            player_rect = pygame.Rect(player.x, player.y, player.img.get_width(), player.img.get_height())
            attack_rect = pygame.Rect(self.x, self.y, self._image.get_width(), self._image.get_height())
            if player_rect.colliderect(attack_rect):
                self.active = False
                potion_break_sound.play()
                thorn_growing_sound.play()
                return True
            else:
                return False
        else:
            return False