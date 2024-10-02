import random
from config import *

def random_speed(speed):
    return random.uniform(0, 0.05) + speed

class Ice_monster1:
    def __init__(self, init_dict):
        __new_random_speed = random_speed(init_dict["speed"])
        self._img = pygame.image.load("images/ice_monster1.png")
        self._screen = init_dict["screen"]
        self._x = random.randint(borderLeft + 1, borderRight - enemy_size - 1)
        self._y = random.randint(height//20, height//4)
        self._x_change = __new_random_speed * random.choice([-1, 1])
        self._health = init_dict["health"]
        self._speed = __new_random_speed
        self._move_distance = init_dict["move_distance"]



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
        return self.y > height / 1.4

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

class Ice_monster2:
    def __init__(self, init_dict):
        __new_random_speed = random_speed(init_dict["speed"])
        self._img = pygame.image.load("images/ice_monster2.png")
        self._screen = init_dict["screen"]
        self._x = random.randint(borderLeft + 1, borderRight - enemy_size - 1)
        self._y = random.randint(height//20, height//4)
        self._x_change = __new_random_speed * random.choice([-1, 1])
        self._health = init_dict["health"]
        self._speed = __new_random_speed
        self._move_distance = init_dict["move_distance"]



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
        return self.y > height / 1.4

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