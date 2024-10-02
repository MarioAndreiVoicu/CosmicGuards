import pygame
import random
from config import *

random_direction = random.choice([-1, 1])

class Dragon:
    def __init__(self, screen, health, speed, damage):
        self._dragon_img = pygame.image.load("images/dragon.png")
        self._screen = screen
        self._x = (width - rocket_size)//2
        self._y = height//5
        self._x_change = speed * random_direction
        self._damage = damage
        self._speed = speed
        self._health = health



    @property
    def dragon_img(self):
        return self._dragon_img

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

    def fire_attack(self, fireball_attack):
        fireball_attack.active = True

    def display(self):
        self._screen.blit(self.dragon_img, (self.x, self.y))

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


class Dragon_attack:
    def __init__(self, screen, dragon):
        self._screen = screen
        self._image = pygame.image.load("images/fireball.png")
        self._x = dragon.x
        self._y = dragon.y
        self._speed = fireball_attack_speed
        self._active = False
        self._dragon = dragon

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

    def activate(self, dragon):
        fireball_attack_sound.play()
        self.active = True
        self.x = dragon.x
        self.y = dragon.y

    def move(self):
        if self.active:
            self.y += self.speed
        if self.y > height + mega_attack_size:
            self.active = False
            self.y = self._dragon.y

    def display(self):
        if self.active:
            self._screen.blit(self._image, (self.x, self.y))

    def check_collision(self, player):
        if self.active:
            player_rect = pygame.Rect(player.x, player.y, player.img.get_width(), player.img.get_height())
            attack_rect = pygame.Rect(self.x, self.y, self._image.get_width(), self._image.get_height())
            if player_rect.colliderect(attack_rect):
                self.active = False
                player.lives = 0


