import pygame
import random
import math
from pygame import mixer
import time
import sys
import os

from config import *
from player import Player
from missile import Missile
from ufo import Purple1, Ufo1, Ufo2, Ufo3
from boss import Dragon,Dragon_attack
from mini_dragon import Mini_dragon
from ice_monster import Ice_monster1, Ice_monster2
from yeti import Yeti, Yeti_attack
from mini_yeti import Mini_yeti
from zombies import Zombie1, Zombie2
from mini_goblin import Mini_goblin1, Mini_goblin2
from goblin import Goblin, Spear_throw, Potion_throw


# Initialize the pygame
pygame.init()

# Create the entities
player = Player(screen, easy_damage, easy_speed, easy_lives)
missile = Missile(screen, player.x, player.y)
dragon = Dragon(screen, easy_dragon_health, easy_dragon_speed, easy_dragon_damage)

enemies = {
    "purple_lvl1": {
        "enemy_list": [],
        "enemies_remaining": purple_lvl1_remaining,
        "max_enemies": purple_lvl1_num,
        "is_active": False
    },

     "ufo1": {
        "enemy_list": [],
        "enemies_remaining": ufo1_remaining,
        "max_enemies": ufo1_max,
        "is_active": False
     },

    "ufo2": {
        "enemy_list": [],
        "enemies_remaining": ufo2_remaining,
        "max_enemies": ufo2_max,
        "is_active": False
    },

    "ufo3": {
        "enemy_list": [],
        "enemies_remaining": ufo3_remaining,
        "max_enemies": ufo3_max,
        "is_active": False
    },

    "ice_monster1": {
        "enemy_list": [],
        "enemies_remaining": ice_monsters1_remaining,
        "max_enemies": ice_monster1_max,
        "is_active": False
    },

    "ice_monster2": {
        "enemy_list": [],
        "enemies_remaining": ice_monsters2_remaining,
        "max_enemies": ice_monster2_max,
        "is_active": False
    },

    "zombie1": {
        "enemy_list": [],
        "enemies_remaining": zombies1_remaining,
        "max_enemies": zombies1_max,
        "is_active": False
    },

    "zombie2": {
        "enemy_list": [],
        "enemies_remaining": zombies2_remaining,
        "max_enemies": zombies2_max,
        "is_active": False
    },

}

minions = {
    "mini_yeti": {
        "enemy_list": [],
        "spawn_count" : None
    },

    "mini_goblin1": {
        "enemy_list": [],
        "spawn_count": 1,
        "is_active": False
    },

    "mini_goblin2": {
        "enemy_list": [],
        "spawn_count": 1,
        "is_active": False
    },
}

def start_scene():
    mixer.music.load("sounds/start_music.mp3")
    mixer.music.play(-1)

    global start, running
    while start:
        screen.blit(start_screen, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                mixer.music.load("sounds/music.mp3")
                mixer.music.play(-1)
                start = False
                global round1_begin
                round1_begin = True

        pygame.display.update()

def random_x(enemy_size):
    return random.randint(borderLeft + 1, borderRight - enemy_size - 1)

def create_enemy_list(enemy_class, max_enemies_num):
    enemy_list = []
    for _ in range(max_enemies_num):
        new_enemy = create_one_enemy(enemy_class)
        enemy_list.append(new_enemy)
    return enemy_list

def create_enemy(enemy_class, enemies_remaining, max_enemies_num):
    enemies[enemy_class]["enemy_list"] = create_enemy_list(enemy_class, max_enemies_num)
    enemies[enemy_class]["enemies_remaining"] = enemies_remaining
    enemies[enemy_class]["max_enemies"] = max_enemies_num
    enemies[enemy_class]["is_active"] = True

def create_one_enemy(enemy_class):
    if enemy_class == "purple_lvl1":
        new_enemy = Purple1(purple_lvl1_init_dict)
    elif enemy_class == "mini_yeti":
        new_enemy = Mini_yeti(mini_yeti_init_dict, random_x(enemy_size), height // 10, random.choice([-1, 1]))
    elif enemy_class == "ufo1":
        new_enemy = Ufo1(ufo_init_dict)
    elif enemy_class == "ufo2":
        new_enemy = Ufo2(ufo_init_dict)
    elif enemy_class == "ufo3":
        new_enemy = Ufo3(ufo_init_dict)
    elif enemy_class == "zombie1":
        new_enemy = Zombie1(zombie_init_dict)
    elif enemy_class == "zombie2":
        new_enemy = Zombie2(zombie_init_dict)
    elif enemy_class == "ice_monster1":
        new_enemy = Ice_monster1(ice_monster_init_dict)
    elif enemy_class == "ice_monster2":
        new_enemy = Ice_monster2(ice_monster_init_dict)
    return new_enemy

def create_minions(minion_class, spawn_count):
    minions[minion_class]["enemy_list"] = create_enemy_list(minion_class,spawn_count)

# Score
score_value = 0
font_32 = pygame.font.Font("freesansbold.ttf", 32)

def show_score():
    score = font_32.render(f"Score: {str(score_value)}", True, (255, 255, 255))
    screen.blit(score, (10, 10))

def stats_scene():
    stats = True
    font_stats = pygame.font.Font("freesansbold.ttf", 64)
    damage_display = font_stats.render(f"Damage: {str(player.damage)}", True, (255, 255, 255))
    speed_display = font_stats.render(f"Speed: {str(int(player.speed*30))}", True, (255, 255, 255))

    while stats:
        screen.blit(stats_image, (0, 0))
        screen.blit(damage_display, (300, 230))
        screen.blit(speed_display, (300, 400))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stats = False
                global running
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                stats = False

        pygame.display.update()

def move_display_enemies():
    for enemy_type in enemies:
        if not enemies[enemy_type]["is_active"]:
            continue  # if the enemy is not active, skip him
        current_enemy_count = min(enemies[enemy_type]["enemies_remaining"],enemies[enemy_type]["max_enemies"])
        for i in range(current_enemy_count-1, -1 ,-1):   #iterate backwards trough the remaining enemies so invalid indexes are not accessed
            enemies[enemy_type]["enemy_list"][i].move()
            enemies[enemy_type]["enemy_list"][i].display()
            if enemies[enemy_type]["enemy_list"][i].hit():
                player.lives = 0
                return
            if isCollision(enemies[enemy_type]["enemy_list"][i].x, enemies[enemy_type]["enemy_list"][i].y, missile.x, missile.y):
                treat_collision(enemy_type, i)

def missile_move_display():
    if missile.y <= borderUp:
        missile.y = player.y
        missile.is_fired = False
    if missile.is_fired:
        missile.display()
        missile.y -= missile.speed

def victory_scene():
    pygame.mixer.music.stop()
    start_time = time.time()

    victory_sound.play()
    victory_animation_play = True
    while victory_animation_play:
        screen.blit(victory_image, (0, 0))
        if time.time() - start_time > victory_sound.get_length():
            victory_animation_play = False

        pygame.display.update()

    mixer.music.load("sounds/victory_music.mp3")
    mixer.music.play(-1)

    global victory, running
    while victory:
        screen.fill((0, 0, 0))
        screen.blit(victory_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                victory = False

        pygame.display.update()

def game_over():
    pygame.mixer.music.stop()
    game_over_sound.play()
    time.sleep(game_over_sound.get_length())
    mixer.music.load("sounds/game_over_music.mp3")
    mixer.music.play(-1)

    game_over_check = True
    while game_over_check:
        screen.blit(game_over_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_check = False
                global running
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_over_check = False

        pygame.display.update()

def increase_enemies_health(value):
    for enemy_type in enemies:
        current_enemy_count = min(enemies[enemy_type]["enemies_remaining"],enemies[enemy_type]["max_enemies"])
        for i in range(current_enemy_count-1, -1 ,-1):
            enemies[enemy_type]["enemy_list"][i].health += value

    global purple_lvl1_init_dict
    purple_lvl1_init_dict["health"] += value

    global ufo_init_dict
    ufo_init_dict["health"] += value


def check_next_level(score):
    global upgrading
    if score == 15 or score == 45 or score == 80:
        upgrading = True
    elif score == 30:
        dragon_fight()
    elif score == 60:
        yeti_fight()
    elif score == 100:
        goblin_fight()
    else:
        upgrading = False

def slow_enemies():
    power_up_sound.play()
    for enemy_type in enemies:
        if not enemies[enemy_type]["is_active"]:
            continue
        current_enemy_count = min(enemies[enemy_type]["enemies_remaining"],enemies[enemy_type]["max_enemies"])
        for i in range(current_enemy_count-1, -1 ,-1):
            enemies[enemy_type]["enemy_list"][i].speed = enemies[enemy_type]["enemy_list"][i].speed * 0.75
            enemies[enemy_type]["enemy_list"][i].x_change = enemies[enemy_type]["enemy_list"][i].speed

    global purple_lvl1_init_dict
    purple_lvl1_init_dict["speed"] = purple_lvl1_init_dict["speed"] * 0.75

    global ufo_init_dict
    ufo_init_dict["speed"] = ufo_init_dict["speed"] * 0.75

    global zombie_init_dict
    zombie_init_dict["speed"] = zombie_init_dict["speed"] * 0.75

    global ice_monster_init_dict
    ice_monster_init_dict["speed"] = ice_monster_init_dict["speed"] * 0.75

def upgrade():
    global upgrading,running
    while upgrading:
        screen.fill((0, 0, 0))
        screen.blit(upgrades_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                upgrading = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    power_up_sound.play()
                    player.damage *= 2
                    upgrading = False
                elif event.key == pygame.K_s:
                    slow_enemies()
                    upgrading = False
                elif event.key == pygame.K_d:
                    power_up_sound.play()
                    player.speed += player.speed/5
                    missile.speed += missile_speed/5
                    upgrading = False

        pygame.display.update()

def treat_collision_mini_dragon(i, mini_dragons):
    explosion_sound = mixer.Sound("sounds/explosion.wav")
    explosion_sound.play()
    global score_value, mini_dragons_num, mini_dragons_alive
    missile.is_fired = False
    missile.y = player.y
    mini_dragons[i].health -= player.damage
    if mini_dragons[i].health <= 0:
        del mini_dragons[i]
        mini_dragons_alive -= 1


def treat_collision_mini_yeti(i):
    explosion_sound = mixer.Sound("sounds/explosion.wav")
    explosion_sound.play()
    global mini_yetis_alive
    missile.is_fired = False
    missile.y = player.y
    minions["mini_yeti"]["enemy_list"][i].health -= player.damage
    if minions["mini_yeti"]["enemy_list"][i].health <= 0:
        minions["mini_yeti"]["enemy_list"].pop(i)
        mini_yetis_alive -= 1

def treat_collision_mini_goblin1(i):
    mini_goblin_death_effect.play()
    global mini_goblins1_alive
    missile.is_fired = False
    missile.y = player.y
    minions["mini_goblin1"]["enemy_list"][i].health -= player.damage
    if minions["mini_goblin1"]["enemy_list"][i].health <= 0:
        minions["mini_goblin1"]["enemy_list"].pop(i)
        mini_goblin_death_effect.play()
        mini_goblins1_alive -= 1

def treat_collision_mini_goblin2(i):
    mini_goblin_death_effect.play()
    global mini_goblins2_alive
    missile.is_fired = False
    missile.y = player.y
    minions["mini_goblin2"]["enemy_list"][i].health -= player.damage
    if minions["mini_goblin2"]["enemy_list"][i].health <= 0:
        minions["mini_goblin2"]["enemy_list"].pop(i)
        mini_goblin_death_effect.play()
        mini_goblins2_alive -= 1


def show_dragon_health(health):
    health = font_32.render(f"Dragon Health: {str(health)}", True, (255, 0, 0))
    screen.blit(health, (10, 10))

def show_yeti_health(health):
    health = font_32.render(f"Yeti Health: {str(health)}", True, (100, 149, 237))
    screen.blit(health, (10, 10))

def show_goblin_health(health):
    health = font_32.render(f"Goblin Health: {str(health)}", True, (27, 67, 50))
    screen.blit(health, (10, 10))

def dragon_fight_introduction():
    start_time = time.time()
    boss_fight_introduction_sound.play()
    displaying_image = True

    while displaying_image:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((0, 0, 0))
        screen.blit(dragon_start_fight_image, (0, 0))
        # Update the display
        pygame.display.update()

        # Check if the duration has passed
        if time.time() - start_time > 9:
            displaying_image = False

def dragon_fight():

    player.img = pygame.image.load("images/dragon_spaceship.png")

    pygame.mixer.music.stop()
    dragon_fight_introduction()

    mixer.music.load("sounds/dragon_fight_music_test.mp3")
    mixer.music.play(-1)

    dragon_fight_sound_start.play()

    global mini_dragons_alive
    mini_dragons = [None, None]
    mini_dragons[0] = Mini_dragon(screen, easy_mini_dragon_health, easy_mini_dragon_distance, easy_mini_dragon_speed, random_x(enemy_size), dragon.y, -1)
    mini_dragons[1] = Mini_dragon(screen, easy_mini_dragon_health, easy_mini_dragon_distance, easy_mini_dragon_speed, random_x(enemy_size), dragon.y, 1)
    fireball_attack = Dragon_attack(screen, dragon)
    last_fireball_attack_time = pygame.time.get_ticks()
    last_minion_spawn_time = pygame.time.get_ticks() + 4000

    dragon_boss_fight = True
    while dragon_boss_fight:
        if dragon.health <= 0:
            dragon_boss_fight = False
            dragon_defeat_sound.play()
            dragon_defeat_animation()

        screen.fill((0, 0, 0))
        screen.blit(dragon_fight_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fireball_attack.active = False
                dragon_boss_fight = False
                global running
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.change_direction_left()
                if event.key == pygame.K_RIGHT:
                    player.change_direction_right()
                if event.key == pygame.K_SPACE and not missile.is_fired:
                    missile.fire(player.x, player.y)
                if event.key == pygame.K_p:
                    stats_scene()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.x_change == -1 * player.speed or event.key == pygame.K_RIGHT and player.x_change == player.speed:
                    player.x_change = 0

        player.move()
        dragon.move()

        for i in range(mini_dragons_alive):
            if mini_dragons[i].hit():
                player.lives = 0
                game_over()
                break

            mini_dragons[i].move()
            mini_dragons[i].display()

            if isCollision(mini_dragons[i].x, mini_dragons[i].y, missile.x, missile.y):
                treat_collision_mini_dragon(i, mini_dragons)

        current_time = pygame.time.get_ticks()
        if current_time - last_fireball_attack_time >= attack_interval:
            fireball_attack.activate(dragon)
            last_fireball_attack_time = current_time

        if current_time - last_minion_spawn_time >= minions_spawn_interval:
            mini_dragons_alive += mini_dragons_num
            for _ in range(mini_dragons_num):
                new_mini_dragon = Mini_dragon(screen, easy_mini_dragon_health, easy_mini_dragon_distance, easy_mini_dragon_speed, random_x(enemy_size), dragon.y, -1)
                mini_dragons.append(new_mini_dragon)
            last_minion_spawn_time = current_time

        if fireball_attack.active:
            fireball_attack.display()
            fireball_attack.move()
            fireball_attack.check_collision(player)
            if player.lives == 0:
                dragon_boss_fight = False
                game_over()


        if isCollision(dragon.x, dragon.y, missile.x, missile.y, isBoss = True):
            dragon.health -= player.damage
            explosion_sound = mixer.Sound("sounds/explosion.wav")
            explosion_sound.play()
            missile.is_fired = False
            missile.y = player.y

        dragon.display()
        player.display()

        # Missile Movement
        if missile.y <= borderUp:
            missile.y=player.y
            missile.is_fired = False

        if  missile.is_fired:
            missile.display()
            missile.y -= missile.speed

        show_dragon_health(dragon.health)
        pygame.display.update()

def dragon_defeat_animation():
    defeat_animation = True
    while defeat_animation:
        screen.fill((0, 0, 0))
        screen.blit(dragon_fight_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
                defeat_animation = False

        dragon.y += 0.1
        screen.blit(dragon.dragon_img, (dragon.x, dragon.y))

        if dragon.y > height + 150:
            defeat_animation = False
            global round2_begin
            round2_begin = True

        pygame.display.update()

def yeti_fight_introduction():
    start_time = time.time()
    boss_fight_introduction_sound.play()
    displaying_image = True

    while displaying_image:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.blit(yeti_introduction_image, (0, 0))
        pygame.display.update()

        # Check if the duration has passed
        if time.time() - start_time > 9:
            displaying_image = False

def yeti_fight():
    global running

    yeti = Yeti(yeti_init_dict)

    pygame.mixer.music.stop()
    yeti_fight_introduction()

    mixer.music.load("sounds/yeti_fight_music.mp3")
    mixer.music.play(-1)

    global mini_yetis_alive
    mini_yeti = create_minions("mini_yeti", mini_yetis_num)
    mini_yetis_alive += 2
    snowflake_attack = Yeti_attack(screen, yeti)
    last_snowflake_attack_time = pygame.time.get_ticks()
    last_minion_spawn_time = pygame.time.get_ticks() + 4000
    freeze_player = False
    freeze_time_start = pygame.time.get_ticks()

    yeti_boss_fight = True
    while yeti_boss_fight:
        if yeti.health <= 0:
            yeti_boss_fight = False
            yeti_defeat_sound.play()
            yeti_defeat_animation(yeti)

        screen.fill((0, 0, 0))
        screen.blit(yeti_fight_background, (0, 0))

        # Check if player is still frozen to prevent/allow player.move and fire_missile
        current_time = pygame.time.get_ticks()
        if current_time - freeze_time_start >= snowflake_freeze_time:
            freeze_player = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                snowflake_attack.active = False
                yeti_boss_fight = False
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.change_direction_left()
                if event.key == pygame.K_RIGHT:
                    player.change_direction_right()
                if event.key == pygame.K_SPACE and not missile.is_fired and not freeze_player:
                    missile.fire(player.x, player.y)
                if event.key == pygame.K_p:
                    stats_scene()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.x_change == -1 * player.speed or event.key == pygame.K_RIGHT and player.x_change == player.speed:
                    player.x_change = 0

        if not freeze_player:
            player.move()
            player.display()
        else:
            screen.blit(freeze_effect,(player.x,player.y))
        yeti.move()
        yeti.display()

        for i in range(mini_yetis_alive - 1, -1, -1):
            if minions["mini_yeti"]["enemy_list"][i].hit():
                player.lives = 0
                yeti_boss_fight = False
                game_over()
                break

            minions["mini_yeti"]["enemy_list"][i].move()
            minions["mini_yeti"]["enemy_list"][i].display()

            if isCollision(minions["mini_yeti"]["enemy_list"][i].x, minions["mini_yeti"]["enemy_list"][i].y, missile.x, missile.y):
                treat_collision_mini_yeti(i)

        if current_time - last_snowflake_attack_time >= snowflake_attack_interval:
            snowflake_attack_sound.play()
            snowflake_attack.activate(yeti)
            last_snowflake_attack_time = current_time

        if current_time - last_minion_spawn_time >= minions_spawn_interval:
            mini_yetis_alive += mini_yetis_num
            for _ in range(mini_yetis_num):
                new_mini_yeti = Mini_yeti(mini_yeti_init_dict, random_x(enemy_size), yeti.y, random.choice([-1, 1]))
                minions["mini_yeti"]["enemy_list"].append(new_mini_yeti)
            last_minion_spawn_time = current_time

        if snowflake_attack.active:
            snowflake_attack.display()
            snowflake_attack.move()
            if snowflake_attack.collision(player):
                freeze_player = True
                freeze_time_start = pygame.time.get_ticks()


        if isCollision(yeti.x, yeti.y, missile.x, missile.y, isBoss = True):
            yeti.health -= player.damage
            explosion_sound = mixer.Sound("sounds/explosion.wav")
            explosion_sound.play()
            missile.is_fired = False
            missile.y = player.y

        # Missile Movement
        if missile.y <= borderUp:
            missile.y = player.y
            missile.is_fired = False

        if  missile.is_fired:
            missile.display()
            missile.y -= missile.speed

        show_yeti_health(yeti.health)
        pygame.display.update()

def yeti_defeat_animation(yeti):
    defeat_animation = True
    while defeat_animation:
        screen.fill((0, 0, 0))
        screen.blit(yeti_fight_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
                defeat_animation = False

        yeti.y += 0.1
        screen.blit(yeti.img, (yeti.x, yeti.y))

        if yeti.y > height + 150:
            defeat_animation = False
            global round2_active
            round2_active = False
            global round3_begin
            round3_begin = True

        pygame.display.update()

def health_potion_display(goblin):
    screen.blit(health_potion, (goblin.x, goblin.y+boss_size/2))
    screen.blit(health_regen_icon, (10, 30))
    regenerating_message = font_32.render(f"Regenerating", True, (164,19,60))
    screen.blit(regenerating_message, (80, 50))

def mini_goblins_move_display():
    for i in range(mini_goblins1_alive - 1, -1, -1):
        if minions["mini_goblin1"]["enemy_list"][i].hit():
            player.lives = 0
            goblin_boss_fight = False
            game_over()
            break

        minions["mini_goblin1"]["enemy_list"][i].move()
        minions["mini_goblin1"]["enemy_list"][i].display()

        if isCollision(minions["mini_goblin1"]["enemy_list"][i].x, minions["mini_goblin1"]["enemy_list"][i].y,
                       missile.x, missile.y):
            treat_collision_mini_goblin1(i)

    for i in range(mini_goblins2_alive - 1, -1, -1):
        if minions["mini_goblin2"]["enemy_list"][i].hit():
            player.lives = 0
            goblin_boss_fight = False
            game_over()
            break

        minions["mini_goblin2"]["enemy_list"][i].move()
        minions["mini_goblin2"]["enemy_list"][i].display()

        if isCollision(minions["mini_goblin2"]["enemy_list"][i].x, minions["mini_goblin2"]["enemy_list"][i].y,
                       missile.x, missile.y):
            treat_collision_mini_goblin2(i)


def goblin_fight_introduction():
    start_time = time.time()
    boss_fight_introduction_sound.play()
    displaying_image = True

    while displaying_image:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.blit(goblin_introduction_image, (0, 0))
        pygame.display.update()

        if time.time() - start_time > 9:
            displaying_image = False

def goblin_fight():
    global running

    goblin = Goblin(goblin_init_dict)

    pygame.mixer.music.stop()
    goblin_fight_introduction()
    goblin_introduction_sound.play()
    mixer.music.load("sounds/goblin_fight_music.mp3")
    mixer.music.play(-1)

    global mini_goblins1_alive,mini_goblins2_alive
    new_mini_goblin1 = Mini_goblin1(mini_goblin_init_dict,random_x(enemy_size), height // 10, 1)
    new_mini_goblin2 = Mini_goblin2(mini_goblin_init_dict,random_x(enemy_size), height // 10, -1)
    minions["mini_goblin1"]["enemy_list"].append(new_mini_goblin1)
    minions["mini_goblin2"]["enemy_list"].append(new_mini_goblin2)
    mini_goblins1_alive += mini_goblins1_num
    mini_goblins2_alive += mini_goblins2_num
    spear_throw = Spear_throw(screen, goblin)
    potion_throw = Potion_throw(screen, goblin)
    last_spear_throw_time = pygame.time.get_ticks() - 20000
    last_potion_throw_time = pygame.time.get_ticks() - 15000
    last_minion_spawn_time = pygame.time.get_ticks() - 10000
    last_health_potion_time = pygame.time.get_ticks() - 5000
    thorn_time_start = pygame.time.get_ticks()
    health_potion_start_time = pygame.time.get_ticks()
    thorn_catch_player = False
    drinking_potion = False

    goblin_boss_fight = True
    while goblin_boss_fight:
        if goblin.health <= 0:
            goblin_boss_fight = False
            goblin_defeat_sound.play()
            goblin_defeat_animation(goblin)

        screen.fill((0, 0, 0))
        screen.blit(goblin_fight_background, (0, 0))

        # Check if player is still caught in thorns to prevent/allow player.move and fire_missile
        current_time = pygame.time.get_ticks()
        if current_time - thorn_time_start >= thorn_catch_time:
            thorn_catch_player = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                goblin_boss_fight = False
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.change_direction_left()
                if event.key == pygame.K_RIGHT:
                    player.change_direction_right()
                if event.key == pygame.K_SPACE and not missile.is_fired and not thorn_catch_player:
                    missile.fire(player.x, player.y)
                if event.key == pygame.K_p:
                    stats_scene()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.x_change == -1 * player.speed or event.key == pygame.K_RIGHT and player.x_change == player.speed:
                    player.x_change = 0

        mini_goblins_move_display()

        player.display()
        goblin.display()
        if not thorn_catch_player:
            player.move()
        else:
            screen.blit(thorn_effect_image, (player.x, player.y))
        if not drinking_potion:
            goblin.move()
        else:
            health_potion_display(goblin)

        # Throw spear
        if current_time - last_spear_throw_time >= goblin_attack_interval:
            throw_sound.play()
            spear_throw.activate(goblin)
            last_spear_throw_time = current_time
        # Throw potion if time
        elif current_time - last_potion_throw_time >= goblin_attack_interval:
            throw_sound.play()
            potion_throw.activate(goblin)
            last_potion_throw_time = current_time
        # Spawn minions
        elif current_time - last_minion_spawn_time >= goblin_attack_interval:
            mini_goblins_spawn_sound.play()
            mini_goblins1_alive += mini_goblins1_num
            mini_goblins2_alive += mini_goblins2_num
            for _ in range(mini_goblins1_num):
                new_mini_goblin1 = Mini_goblin1(mini_goblin_init_dict, random_x(enemy_size), goblin.y, 1)
                minions["mini_goblin1"]["enemy_list"].append(new_mini_goblin1)
            for _ in range(mini_goblins2_num):
                new_mini_goblin2 = Mini_goblin2(mini_goblin_init_dict, random_x(enemy_size), goblin.y, -1)
                minions["mini_goblin2"]["enemy_list"].append(new_mini_goblin2)
            last_minion_spawn_time = current_time
        # Drink Health Potion
        elif current_time - last_health_potion_time >= goblin_attack_interval:
            drinking_health_potion_sound.play()
            health_potion_display(goblin)
            last_health_potion_time = current_time
            health_potion_start_time = current_time
            drinking_potion = True


        if drinking_potion and current_time - health_potion_start_time >= 4000:
            goblin.health += 25
            health_regenerated_sound.play()
            drinking_potion = False

        if spear_throw.active:
            spear_throw.move()
            spear_throw.display()
            if spear_throw.collision(player):
                player.lives = 0

        if potion_throw.active:
            potion_throw.move()
            potion_throw.display()
            if potion_throw.collision(player):
                thorn_catch_player = True
                thorn_time_start = pygame.time.get_ticks()

            if player.lives == 0:
                goblin_boss_fight = False
                game_over()

        if player.lives == 0:
            goblin_boss_fight = False
            game_over()


        if isCollision(goblin.x, goblin.y, missile.x, missile.y, isBoss=True):
            goblin.health -= player.damage
            explosion_sound = mixer.Sound("sounds/explosion.wav")
            explosion_sound.play()
            missile.is_fired = False
            missile.y = player.y
            if drinking_potion:
                drinking_potion = False # If the player hits the goblin while drinking the health potion,it stops him
                drinking_health_potion_sound.stop()
                potion_break_sound.play()

        # Missile Movement
        if missile.y <= borderUp:
            missile.y = player.y
            missile.is_fired = False

        if  missile.is_fired:
            missile.display()
            missile.y -= missile.speed

        show_goblin_health(goblin.health)
        pygame.display.update()

def goblin_defeat_animation(goblin):
    defeat_animation = True
    while defeat_animation:
        screen.fill((0, 0, 0))
        screen.blit(goblin_fight_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
                defeat_animation = False

        goblin.y += 0.1
        screen.blit(goblin.img, (goblin.x, goblin.y))

        if goblin.y > height + 150:
            defeat_animation = False
            global victory
            victory = True

        pygame.display.update()

def isCollision(enemy_x, enemy_y, missile_x, missile_y, isBoss=False):
    distance = math.sqrt(math.pow(enemy_x - missile_x, 2) + math.pow(enemy_y - missile_y, 2))
    if not isBoss:
        return distance < (height + width) // 45
    else:
        return distance < (height + width) // 21

def treat_collision(enemy_type, index):
    explosion_sound = mixer.Sound("sounds/explosion.wav")
    explosion_sound.play()
    global score_value
    missile.is_fired = False
    missile.y = player.y
    enemies[enemy_type]["enemy_list"][index].health -= player.damage
    if enemies[enemy_type]["enemy_list"][index].health <= 0:
        score_value += 1
        check_next_level(score_value)
        enemies[enemy_type]["enemies_remaining"] -= 1
        if enemies[enemy_type]["enemies_remaining"] >= enemies[enemy_type]["max_enemies"]:
            new_enemy = create_one_enemy(enemy_type)
            enemies[enemy_type]["enemy_list"][index] = new_enemy
        else:
            enemies[enemy_type]["enemy_list"].pop(index)

def deactivate_enemies(*args):
    for enemy_name in args:
        enemies[enemy_name]["is_active"] = False

def create_enemies_round1():
    create_enemy("ufo1", ufo1_remaining, ufo1_max)
    create_enemy("ufo2", ufo2_remaining, ufo2_max)
    create_enemy("ufo3", ufo3_remaining, ufo3_max)
    global round1_begin
    round1_begin = False

def create_enemies_round2():
    deactivate_enemies("ufo1", "ufo2", "ufo3")
    create_enemy("ice_monster1", ice_monsters1_remaining, ice_monster1_max)
    create_enemy("ice_monster2", ice_monsters2_remaining, ice_monster2_max)
    global round2_begin
    round2_begin = False

def create_enemies_round3():
    deactivate_enemies("ice_monster1", "ice_monster2")
    create_enemy("zombie1", zombies1_remaining, zombies1_max)
    create_enemy("zombie2", zombies2_remaining, zombies2_max)
    global round3_begin
    round3_begin = False

# Game loop
running = True
while running:
    screen.blit(background, (0, 0))

    if start:
        start_scene()

    if round1_begin:
        create_enemies_round1()
        background = round1_background
        round1_active = True
    elif round2_begin:
        create_enemies_round2()
        player.img = pygame.image.load("images/yeti_spaceship.png")
        round2_active = True
        background = round2_background
    elif round3_begin:
        create_enemies_round3()
        player.img = pygame.image.load("images/goblin_spaceship.png")
        round3_active = True
        background = round3_background

    if is_game_over:
        game_over()

    if upgrading:
        upgrade()

    if dragon_boss_fight:
        dragon_fight()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.change_direction_left()
            if event.key == pygame.K_RIGHT:
                player.change_direction_right()
            if event.key == pygame.K_SPACE and not missile.is_fired:
                missile_sound.play()
                missile.x = player.x
                missile.fire(player.x, player.y)
            if event.key == pygame.K_p:
                stats_scene()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.x_change == -1*player.speed or event.key == pygame.K_RIGHT and player.x_change == player.speed:
                player.x_change = 0


    # Missile Movement
    if missile.y <= borderUp:
        missile.y = player.y
        missile.is_fired = False
    if missile.is_fired:
        missile.display()
        missile.y -= missile.speed

    player.move()
    player.display()
    move_display_enemies()
    if player.lives == 0:
        game_over()

    show_score()

    if victory:
        victory_scene()

    pygame.display.update()