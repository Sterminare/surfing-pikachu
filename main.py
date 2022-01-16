import pygame
import random
import math
from sys import exit

# INITIALIZE WINDOW AND LOAD SPRITES TO SURFACES
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1000, 900))
pygame.display.set_caption('Surfing Pikachu')
icon = pygame.image.load('graphics/icon.png')
pygame.display.set_icon(icon)

sky = pygame.image.load('graphics/environment/sky.png')
ocean = pygame.image.load('graphics/environment/ocean_scrollable.png')
small_wave = pygame.image.load('graphics/environment/small_wave.png')

tutorial = pygame.image.load('graphics/overlay/tutorial.png')
overlay = pygame.image.load('graphics/overlay/overlay.png')
ohno = pygame.image.load('graphics/overlay/ohno.png')
upkey = pygame.image.load('graphics/overlay/upkey.png')
score0 = pygame.image.load('graphics/overlay/0.png')
score1 = pygame.image.load('graphics/overlay/1.png')
score2 = pygame.image.load('graphics/overlay/2.png')
score3 = pygame.image.load('graphics/overlay/3.png')
score4 = pygame.image.load('graphics/overlay/4.png')
score5 = pygame.image.load('graphics/overlay/5.png')
score6 = pygame.image.load('graphics/overlay/6.png')
score7 = pygame.image.load('graphics/overlay/7.png')
score8 = pygame.image.load('graphics/overlay/8.png')
score9 = pygame.image.load('graphics/overlay/9.png')

player_stand = pygame.image.load('graphics/player/standing.png')
player_crouch = pygame.image.load('graphics/player/crouching.png')
player_splash = pygame.image.load('graphics/player/splash.png')
player_crash = pygame.image.load('graphics/player/crash.png')
player_slight_up = pygame.image.load('graphics/player/slight_up.png')
player_mid_up = pygame.image.load('graphics/player/mid_up.png')
player_very_up = pygame.image.load('graphics/player/very_up.png')
player_slight_down = pygame.image.load('graphics/player/slight_down.png')
player_mid_down = pygame.image.load('graphics/player/mid_down.png')
player_very_down = pygame.image.load('graphics/player/very_down.png')
player_straight = pygame.image.load('graphics/player/straight.png')

# OCEAN SCROLL VARS
ocean_pos = [-1000, 299]
ocean_speed = 4
ocean_start_pos = -1099

# WAVE GENERATION VARS
small_waves = []
wave_previous_ticks = 0
wave_base_delay = 1500
next_random_delay = 0

# PLAYER STATES, POSITION
player_isdown = False
player_isalive = True
player_isjumping = False
player_idle_previous_ticks = 0
player_animation_alternate = False
player_crash_ticks = 0

player_pos = [600, 500]
player_velocity = 0
crash_splash_modifier = 0

# SCOREKEEPING
score_previous_ticks = 0
player_score = 0
score_start_pos = [700, 850]
digit_distance = 40

while True:
    # MANAGE EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_isdown = True
            if event.key == pygame.K_UP:
                player_isjumping = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                if player_isdown:
                    player_isdown = False
            if event.key == pygame.K_UP:
                if player_isjumping:
                    player_isjumping = False

    # SCROLL BACKGROUND OCEAN
    screen.blit(ocean, (ocean_pos[0], ocean_pos[1]))
    screen.blit(sky, (0, 0))
    screen.blit(overlay, (0, 900 - 112))

    ocean_pos[0] += ocean_speed
    if ocean_pos[0] >= 0:
        ocean_pos[0] = ocean_start_pos

    ocean_pos[1] = math.sin(ocean_pos[0] / 50) * 5 + 280

    # GENERATE AND SCROLL WAVES
    wave_current_ticks = pygame.time.get_ticks()
    if wave_current_ticks - wave_previous_ticks > wave_base_delay + next_random_delay and player_isalive:
        next_random_delay = random.randint(0, 2000)
        small_waves.append(-400)
        wave_previous_ticks = wave_current_ticks
    for i, position in enumerate(small_waves):
        if position > 1100:
            small_waves.remove(position)
        screen.blit(small_wave, (position, ocean_pos[1] + 200))
        if len(small_waves) > 0:
            small_waves[i] += ocean_speed

    # MOVE/ANIMATE PLAYER
    # SPLASH BEHIND PLAYER
    if player_isalive and player_pos[1] > 490:
        screen.blit(player_splash, (player_pos[0] + 120, player_pos[1] + 60))

        # IDLE ANIMATION
    player_idle_current_ticks = pygame.time.get_ticks()
    if player_idle_current_ticks - player_idle_previous_ticks > 500:
        player_idle_previous_ticks = player_idle_current_ticks
        if player_animation_alternate:
            player_animation_alternate = False
        else:
            player_animation_alternate = True

    if player_animation_alternate and player_pos[1] > 499 and not player_isdown and player_isalive:
        screen.blit(player_straight, (player_pos[0], player_pos[1]))
    elif player_pos[1] > 499 and not player_isdown and player_isalive:
        screen.blit(player_stand, (player_pos[0], player_pos[1]))

    # SPLASH ANIMATION ON CRASH
    if not player_isalive:
        crash_splash_modifier += 2
        screen.blit(player_splash, (player_pos[0] + crash_splash_modifier, player_pos[1] + 120 - crash_splash_modifier / 10))
        screen.blit(player_splash, (player_pos[0] + 50 + crash_splash_modifier, player_pos[1] + 120 - crash_splash_modifier / 10))
        screen.blit(player_splash, (player_pos[0] + 100 + crash_splash_modifier, player_pos[1] + 120 - crash_splash_modifier / 10))

        # PLAYER CROUCH/STANDING/CRASHED
    if player_isdown and player_isalive and player_pos[1] > 499:
        screen.blit(player_crouch, (player_pos[0], player_pos[1]))
    elif not player_isalive:
        screen.blit(player_crash, (player_pos[0], player_pos[1] + 120))

        # PLAYER JUMPING
    if player_isjumping and player_pos[1] > 499 and player_isalive:
        player_velocity = -7
        player_score += 147
    if player_velocity < -2 and not player_isjumping:
        player_velocity *= 0.95
    player_pos[1] += player_velocity
    if player_velocity < 50:
        player_velocity += 0.1
    if player_pos[1] >= 500:
        player_pos[1] = 500
        player_velocity = 0
    if 1 > player_velocity >= -1 and player_pos[1] < 499:
        screen.blit(player_stand, (player_pos[0], player_pos[1]))
    elif 3.5 > player_velocity >= 1:
        screen.blit(player_slight_down, (player_pos[0], player_pos[1]))
    elif 5 > player_velocity >= 3.5:
        screen.blit(player_mid_down, (player_pos[0], player_pos[1]))
    elif 49 > player_velocity >= 5:
        screen.blit(player_very_down, (player_pos[0], player_pos[1]))
    elif -3.5 < player_velocity <= -1:
        screen.blit(player_slight_up, (player_pos[0], player_pos[1]))
    elif -5 < player_velocity <= -3.5:
        screen.blit(player_mid_up, (player_pos[0], player_pos[1]))
    elif -49 < player_velocity <= -5:
        screen.blit(player_very_up, (player_pos[0], player_pos[1]))

    # PLAYER-OBSTACLE COLLISION
        # COLLISION WITH SMALL WAVES:
    for position in small_waves:
        if position + 30 < player_pos[0] + 50 and position + 150 > player_pos[0] - 50 and player_isalive:
            if player_pos[1] > 400:
                player_score = 0
                player_isalive = False
                ocean_speed = 2
                player_crash_ticks = pygame.time.get_ticks()
                if player_velocity < 1:
                    player_velocity = 1
            else:
                player_score += 25


        # RESET AFTER CRASH
    player_crash_check_ticks = pygame.time.get_ticks()
    if player_crash_check_ticks - player_crash_ticks > 2000:
        player_isalive = True
        ocean_speed = 4
        crash_splash_modifier = 0
    # SCORE
        # SURVIVAL TIME SCORE
    score_current_ticks = pygame.time.get_ticks()
    if score_current_ticks - score_previous_ticks > 100:
        player_score += 110
        score_previous_ticks = score_current_ticks

        # DISPLAY SCORE
    for i, digit in enumerate(str(player_score)):
        if int(digit) == 0:
            screen.blit(score0, (score_start_pos[0] + (i * digit_distance), score_start_pos[1]))
        elif int(digit) == 1:
            screen.blit(score1, (score_start_pos[0] + (i * digit_distance), score_start_pos[1]))
        elif int(digit) == 2:
            screen.blit(score2, (score_start_pos[0] + (i * digit_distance), score_start_pos[1]))
        elif int(digit) == 3:
            screen.blit(score3, (score_start_pos[0] + (i * digit_distance), score_start_pos[1]))
        elif int(digit) == 4:
            screen.blit(score4, (score_start_pos[0] + (i * digit_distance), score_start_pos[1]))
        elif int(digit) == 5:
            screen.blit(score5, (score_start_pos[0] + (i * digit_distance), score_start_pos[1]))
        elif int(digit) == 6:
            screen.blit(score6, (score_start_pos[0] + (i * digit_distance), score_start_pos[1]))
        elif int(digit) == 7:
            screen.blit(score7, (score_start_pos[0] + (i * digit_distance), score_start_pos[1]))
        elif int(digit) == 8:
            screen.blit(score8, (score_start_pos[0] + (i * digit_distance), score_start_pos[1]))
        elif int(digit) == 9:
            screen.blit(score9, (score_start_pos[0] + (i * digit_distance), score_start_pos[1]))

    # DISPLAY CONTROLS/TITLE
    screen.blit(tutorial, (0, 0))

    # UPDATE WINDOW, MAINTAIN FRAMERATE
    pygame.display.update()
    clock.tick(90)
