import pygame
from sys import exit
from random import randint

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surf = test_font.render(f'Score: {int(current_time / 1000)}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time
    print(current_time)

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
            else: screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Pixel Runner')
clock = pygame.time.Clock()
# font_type_var_name = pygame.font.Font(font type from folder program is in, font_size)
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

# image_surface = pygame.image.load('folder/file_name.file_format')
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()
# text_surface = test_font.render(text, anti_aliasing, color)
# score_surf = test_font.render('My game', False, (64,64,64))
# score_rect = score_surf.get_rect(center = (400,50))

# Obstacles
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fly_surf = pygame.image.load('graphics/fly/fly1.png').convert_alpha()

obstacle_rect_list = []

player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
# rect_var_name = surface_var.get_rect(position = (x,y))
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0

# Intro/Outro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale(player_stand,(140,175))
player_stand_rect = player_stand.get_rect(center = (400,200))

title_text_surf = test_font.render("Pixel Runner", False, (111,196,169))
title_text_rect = title_text_surf.get_rect(center = (400,50))

instructions_surf = test_font.render("Press space to play", False, (111,196,169))
instructions_rect = instructions_surf.get_rect(center = (400, 350))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    # draw all our elements
    # update everything
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(snail_surf.get_rect(midbottom=(randint(900,1100), 300)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(midbottom=(randint(900, 1100), 210)))
    if game_active:
        # display_surface_var_name.blit(regular_surface,(x_y_coordinates))
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        score = display_score()
        # pygame.draw.shape(surface to draw on, color, shape we want to draw, optional argument: width of shape, optional argument: boarder radius)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # screen.blit(score_surf,score_rect)

        #snail_rect.x -= 5
        #if snail_rect.right <= 0:
        #    snail_rect.left = 800
        # screen.blit(snail_surf, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # if player_rect.colliderect(snail_rect):
        # print('collision!')

        # collisions
        game_active = collisions(player_rect,obstacle_rect_list)
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0


        score_text_surf = test_font.render(f"Score: {int(score / 1000)}", False, (111, 196, 169))
        score_text_rect = score_text_surf.get_rect(center=(400, 350))
        screen.blit(title_text_surf,title_text_rect)

        if score == 0: screen.blit(instructions_surf, instructions_rect)
        else: screen.blit(score_text_surf, score_text_rect)

    pygame.display.update()
    clock.tick(60)
