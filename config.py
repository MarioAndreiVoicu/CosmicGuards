import pygame
from pygame import mixer
import random

# Title and Icon
pygame.display.set_caption("Cosmic Guards")
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)

# General
rocket_size = 64
enemy_size = 64
boss_size = 128
missile_size = 32
mega_attack_size = 256
yeti_size = 128
snowflake_attack_size = 128
snowflake_attack_interval = 5000
fireball_attack_damage = 10
width = 800
height = 600
borderUp = 0
borderLeft = 0
borderRight = width - enemy_size
borderRightBoss = width - boss_size
enemy_advance_distance = height//15
boss_enemy_speed = 0.1
attack_interval = 8000
minions_spawn_interval = 10000
current_enemies1_num = 5

# Create the screen
screen = pygame.display.set_mode((width, height))

# Screen States
running = True
start = True
upgrading = False
is_game_over = False
dragon_boss_fight = False
victory = False
round1_begin = False
round1_active = False
round2_begin = False
round2_active = False
round3_begin = False
round3_active = False



# Images and Icons
background = pygame.image.load("images/round1_background.jpg")
start_screen = pygame.image.load("images/start_screen.jpg")
missileImg = pygame.image.load("images/missile.png")
snowflake = pygame.image.load("images/snowflake.png")
fireball = pygame.image.load("images/fireball.png")
round1_background = pygame.image.load("images/round1_background.jpg")
round2_background = pygame.image.load("images/round2_background.jpg")
round3_background = pygame.image.load("images/round3_background.jpg")
dragon_fight_background = pygame.image.load("images/dragon_fight_background.jpg")
dragon_start_fight_image = pygame.image.load("images/dragon_start_fight_image.jpg")
victory_image = pygame.image.load("images/victory_image.jpg")
game_over_image = pygame.image.load("images/game_over_final.jpeg")
upgrades_image = pygame.image.load("images/upgrades_image.jpg")
defeated_dragon_icon = pygame.image.load("images/dragon.png")
stats_image = pygame.image.load("images/stats_image.png")
yeti_fight_background = pygame.image.load("images/yeti_fight_background.jpg")
spaceship_img = pygame.image.load("images/spaceship.png")
freeze_effect = pygame.image.load("images/freeze_effect.png")
yeti_introduction_image = pygame.image.load("images/yeti_introduction_image.jpg")

# Sounds
pygame.mixer.init()
missile_sound = mixer.Sound('sounds/shoot_sound.wav')
boss_fight_introduction_sound = mixer.Sound('sounds/boss_fight_introduction_sound.mp3')
fireball_attack_sound = mixer.Sound("sounds/fireball_attack_sound.wav")
dragon_fight_sound_start = mixer.Sound("sounds/dragon_fight_sound_start.wav")
dragon_defeat_sound = mixer.Sound("sounds/dragon_defeat_sound.wav")
game_over_sound = mixer.Sound("sounds/game_over_sound.mp3")
victory_sound = mixer.Sound("sounds/victory_sound.mp3")
power_up_sound = mixer.Sound("sounds/power_up_sound.wav")
snowflake_attack_sound = mixer.Sound("sounds/snowflake_attack_sound.wav")
snowflake_hit_sound = mixer.Sound("sounds/snowflake_hit_sound.wav")
unfreeze_sound = mixer.Sound("sounds/unfreeze_sound.wav")
yeti_growl = mixer.Sound("sounds/yeti_growl.wav")
yeti_defeat_sound = mixer.Sound("sounds/yeti_defeat_sound.mp3")

# Game difficulty
game_difficulty = "Easy"

# Player - EasyMode
easy_damage = 1
easy_speed = 0.3
easy_lives = 1
missile_speed = 0.75

# Enemy - EasyMode
purple_lvl1_health = 1
purple_lvl1_speed = 0.25
purple_lvl1_move_distance = height//12
purple_lvl1_remaining = 0
purple_lvl1_num = 0
purple_lvl1_init_dict = {"screen":screen, "health":purple_lvl1_health,"speed": purple_lvl1_speed,"move_distance": purple_lvl1_move_distance}


# UFO
ufo_health = 1
ufo_speed = 0.2
ufo_move_distance = height//12
ufo1_remaining = ufo2_remaining = ufo3_remaining = 10
ufo1_max = ufo2_max = ufo3_max = 2
ufo_init_dict = {"screen": screen, "health": ufo_health, "speed": ufo_speed, "move_distance": ufo_move_distance}

# Mini Dragons
easy_mini_dragon_speed = 0.3
easy_mini_dragon_health = 4
easy_mini_dragon_damage = 3
easy_mini_dragon_distance = height//15
mini_dragons_num = 2
mini_dragons_alive = 0

# Dragon
easy_dragon_health = 100
easy_dragon_damage = 2
easy_dragon_speed = 0.1
fireball_attack_speed = 0.15

# Ice Monster
ice_monster_health = 4
ice_monster_speed = 0.20
ice_monster_move_distance = height//10
ice_monsters1_remaining = ice_monsters2_remaining = 15
ice_monster1_max = ice_monster2_max = 2
ice_monster_init_dict = {"screen": screen, "health": ice_monster_health, "speed": ice_monster_speed, "move_distance": ice_monster_move_distance}


# Yeti
yeti_health = 200
yeti_speed = 0.1
yeti_init_dict = {"screen":screen, "health":yeti_health, "speed": yeti_speed}
snowflake_attack_speed = 0.35
snowflake_freeze_time = 2000

# Mini Yetis
mini_yetis_num = 2
mini_yetis_alive = 0
mini_yeti_speed = 0.2
mini_yeti_health = 5
mini_yeti_distance = height//10
mini_yeti_init_dict = {"screen":screen, "health":mini_yeti_health,"speed": mini_yeti_speed,"move_distance": mini_yeti_distance}

# Zombies
zombie_health = 1
zombie_speed = 0.32
zombie_move_distance = height//15
zombies1_remaining = zombies2_remaining = 20
zombies1_max = zombies2_max = 2
zombie_init_dict = {"screen": screen, "health": zombie_health, "speed": zombie_speed, "move_distance": zombie_move_distance}

# Mini Goblin
mini_goblins1_num = mini_goblins2_num = 1
mini_goblins1_alive = mini_goblins2_alive = 0
mini_goblin_speed = 0.25
mini_goblin_health = 1
mini_goblin_distance = height//10
mini_goblin_init_dict = {"screen":screen, "health":mini_goblin_health,"speed": mini_goblin_speed,"move_distance": mini_goblin_distance}
mini_goblin_death_effect = mixer.Sound("sounds/mini_goblin_death_effect.mp3")

# Goblin
goblin_introduction_image = pygame.image.load("images/goblin_introduction_image.png")
goblin_fight_background = pygame.image.load("images/goblin_fight_background.jpg")
goblin_defeat_sound = mixer.Sound("sounds/goblin_defeat_sound.wav")
health_potion = pygame.image.load("images/health_potion.png")
thorn_effect_image = pygame.image.load("images/thorns_image.png")
health_regen_icon = pygame.image.load("images/health_regen.png")
goblin_introduction_sound = mixer.Sound("sounds/goblin_introduction_sound.flac")
throw_sound = mixer.Sound("sounds/throw_sound.mp3")
potion_hit_sound = mixer.Sound("sounds/thorn_hit_sound.wav")
potion_break_sound = mixer.Sound("sounds/potion_break_sound.wav")
thorn_growing_sound = mixer.Sound("sounds/thorn_growing_sound.wav")
drinking_health_potion_sound = mixer.Sound("sounds/drinking_health_potion_sound.wav")
health_regenerated_sound = mixer.Sound("sounds/health_regenerated_loud_sound.wav")
mini_goblins_spawn_sound = mixer.Sound("sounds/goblin_minions_spawn_laugh.flac")

goblin_size = 128
potion_throw_size = 128
potion_throw_speed = 0.3
goblin_health = 300
goblin_speed = 0.2
goblin_init_dict = {"screen":screen, "health":goblin_health, "speed": goblin_speed}
spear_throw_size = 128
spear_throw_speed = 0.15
goblin_attack_interval = 25000
thorn_catch_time = 2500