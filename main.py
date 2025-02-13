import pygame
import random

# the location of the first wave of the enemy ships 
def spawn_wave_one(): 
    enemy_list = [
        {"rect": pygame.Rect(150, 80, 70, 70), "health": 3},
        {"rect": pygame.Rect(380, 80, 70, 70), "health": 3},
        {"rect": pygame.Rect(270, 20, 70, 70), "health": 3}
    ]
    return enemy_list

# the location of the second wave of the enemy ships 
def spawn_wave_two():
    enemy_list = [
        {"rect": pygame.Rect(40, 80, 70, 70), "health": 5},
        {"rect": pygame.Rect(110, 20, 70, 70), "health": 5},
        {"rect": pygame.Rect(420, 20, 70, 70), "health": 5},
        {"rect": pygame.Rect(490, 80, 70, 70), "health": 5}
    ]
    return enemy_list

def spawn_wave_three():
    enemy_list = [
        {"asteroid": pygame.Rect(30, 150, 90, 90), "health": 5},
        {"asteroid": pygame.Rect(180, 150, 90, 90), "health": 5},
        {"asteroid": pygame.Rect(330, 150, 90, 90), "health": 5},
        {"asteroid": pygame.Rect(480, 150, 90, 90), "health": 5},
        {"rect": pygame.Rect(40, 30, 70, 70), "health": 5},
        {"rect": pygame.Rect(190, 30, 70, 70), "health": 5},
        {"rect": pygame.Rect(340, 30, 70, 70), "health": 5},
        {"rect": pygame.Rect(490, 30, 70, 70), "health": 5}
    ]
    return enemy_list

def check_collision(bullet, enemy):
    return bullet.colliderect(enemy["rect"])    

ENEMY_MOVE_DOWN_LIMIT = 200
def move_enemies():
    random_x = random.randint(-2, 2)
    increment = 2
    for enemy_data in enemy_list:
        if enemy_data["rect"].x + random_x > 0 and enemy_data["rect"].x + random_x < 600:
            enemy_data["rect"].x += random_x


ENEMY_MOVE_SPEED = 2
ENEMY_MOVE_DOWN_LIMIT = 300
def move_enemies_ver2():
    for enemy_data in enemy_list:
        # Randomly move left (-1), right (+1), or stay in place (0)
        move_x = random.choice([-1, 0, 1]) * ENEMY_MOVE_SPEED
        
        # Move down slightly, but only if it's above the limit
        if enemy_data["rect"].y < ENEMY_MOVE_DOWN_LIMIT:
            move_y = random.choice([0, 1]) * ENEMY_MOVE_SPEED
        else:
            move_y = 0  # Stop moving down if limit is reached

        # Update enemy position
        enemy_data["rect"].x += move_x
        enemy_data["rect"].y += move_y

        # Ensure enemies stay within screen width
        if enemy_data["rect"].x < 0:
            enemy_data["rect"].x = 0
        elif enemy_data["rect"].x > WIDTH - 70:
            enemy_data["rect"].x = WIDTH - 70

def display_life():
    life = [
        {"rect": pygame.Rect(0, 570, 30, 30)},
        {"rect": pygame.Rect(30, 570, 30, 30)},
        {"rect": pygame.Rect(60, 570, 30, 30)}
    ]
    return life


pygame.init()

WIDTH, HEIGHT = 600, 600
BULLET_SPEED = 6
ENEMY_BULLET_SPEED = 3
player_health = 3
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

background = pygame.image.load("graphics/space.svg").convert()
starship = pygame.image.load("graphics2/player.png").convert_alpha()
resized_image = pygame.transform.scale(starship, (70, 70))

enemy = pygame.image.load("graphics2/enemyShip.png").convert_alpha()
resized_enemy = pygame.transform.scale(enemy, (70, 70))

asteroid = pygame.image.load("graphics2/meteorBig.png").convert_alpha()
asteroid = pygame.transform.scale(asteroid, (90, 90))

bullet_img = pygame.image.load("graphics2/laserRed.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

enemy_bullet_img = pygame.image.load("graphics2/laserGreen.png").convert_alpha()
enemy_bullet_img = pygame.transform.scale(enemy_bullet_img, (10, 20))

life = pygame.image.load("graphics2/life.png").convert_alpha()

shooting_sound = pygame.mixer.Sound("graphics/pew.mp3")
destroyed_sound = pygame.mixer.Sound("graphics/destroyed.mp3")

starship_x = 270
starship_y = 500

bullets = []
enemy_bullets = []
enemy_list = spawn_wave_one()
enemy_list_two = spawn_wave_two()
enemy_list_three = spawn_wave_three()
second_wave_spawned = False
third_wave_spawned = False
second_wave_done = False
wave_spawn_time = None
third_spawn_time = None
life_list = display_life()

ENEMY_FIRE_DELAY = 1700
last_enemy_shot_time = pygame.time.get_ticks()

running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_health > 0:
                shooting_sound.play()
                bullet_x = starship_x + 30
                bullet_y = starship_y - 15 
                bullets.append(pygame.Rect(bullet_x, bullet_y, 10, 20))  

    

    screen.blit(background, (0,0)) # draw star background
            
    # draw player lives
    for life_image in life_list:
        screen.blit(life, life_image["rect"].topleft) 
    
    # draw first wave of enemy ships
    for enemy_data in enemy_list:
        screen.blit(resized_enemy, enemy_data["rect"].topleft) 

        # enemy ships firing bullets
        if current_time - last_enemy_shot_time > ENEMY_FIRE_DELAY:   
            for enemy_data in enemy_list:
                enemy_x, enemy_y = enemy_data["rect"].midbottom
                enemy_bullets.append(pygame.Rect(enemy_x, enemy_y, 10, 20)) 
            last_enemy_shot_time = current_time

    # check if wave one is cleared 
    if len(enemy_list) == 0 and not second_wave_spawned:
        if wave_spawn_time is None:
            wave_spawn_time = current_time
        
        #spawn second wave after 5 second delay of clearing first wave 
        if current_time - wave_spawn_time >= 5000:
            enemy_list = enemy_list_two  # spawn second wave
            second_wave_spawned = True  # prevent further respawns
            last_enemy_shot_time = current_time



    # draw second wave of ships 
    if second_wave_spawned:
        if len(enemy_list) > 0:
            for enemy_data in enemy_list:
                screen.blit(resized_enemy, enemy_data["rect"].topleft) 
        else:
            second_wave_done = True

    # draw third wave of ships 
    if second_wave_done:
        for enemy_data in enemy_list_three:
            if "asteroid" in enemy_data:
                screen.blit(asteroid, enemy_data["asteroid"].topleft) 
            else: 
                screen.blit(resized_enemy, enemy_data["rect"].topleft) 

    # enemy bullets travelling 
    for enemy_bullet in enemy_bullets[:]:
        enemy_bullet.y += ENEMY_BULLET_SPEED  
        if enemy_bullet.y > HEIGHT: 
            enemy_bullets.remove(enemy_bullet)

    # drawing enemy bullets
    for enemy_bullet in enemy_bullets:
        screen.blit(enemy_bullet_img, enemy_bullet.topleft)

    # check if enemy bullets collide with player's starship
    for enemy_bullet in enemy_bullets[:]:
        if player_health > 0 and enemy_bullet.colliderect(pygame.Rect(starship_x, starship_y, 70, 70)):
            enemy_bullets.remove(enemy_bullet)  
            player_health -= 1 
            if player_health >= 0:
                life_list.pop()
            else: 
                destroyed_sound.play()

    # draw starship location if alive 
    if player_health > 0:
        screen.blit(resized_image, (starship_x, starship_y)) 

    # keys to move our starship if alive 
    if player_health >  0:
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and starship_x - 2 > 0:
            starship_x -= 5
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and starship_x - 2 < 500:
            starship_x += 5
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and starship_y - 2 > 0: 
            starship_y -= 5   
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and starship_y - 2 < 500: 
            starship_y += 5    

    # make (our) bullets travel
    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED  
        if bullet.y < -30: 
            bullets.remove(bullet)

    # check if (our) bullet hit enemy 
    for bullet in bullets[:]:
        for enemy_data in enemy_list[:]:
            if check_collision(bullet, enemy_data):  
                enemy_data["health"] -= 1  
                bullets.remove(bullet)  
                if enemy_data["health"] <= 0:  
                    enemy_list.remove(enemy_data)
                    destroyed_sound.play()

    # draw our bullets
    for bullet in bullets:
        screen.blit(bullet_img, bullet.topleft)

    pygame.display.update()  
    clock.tick(60)

pygame.quit()

