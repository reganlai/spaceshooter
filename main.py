import pygame


def spawn_wave_one():
    
    enemy_list = [
        {"rect": pygame.Rect(150, 80, 70, 70), "health": 3},
        {"rect": pygame.Rect(380, 80, 70, 70), "health": 3},
        {"rect": pygame.Rect(270, 20, 70, 70), "health": 3}
    ]
    return enemy_list

def spawn_wave_two():

    enemy_list = [
        {"rect": pygame.Rect(0, 80, 70, 70), "health": 5},
        {"rect": pygame.Rect(530, 80, 70, 70), "health": 5},
        {"rect": pygame.Rect(70, 20, 70, 70), "health": 5},
        {"rect": pygame.Rect(460, 20, 70, 70), "health": 5}
    ]
    return enemy_list

def check_collision(bullet, enemy):
    return bullet.colliderect(enemy["rect"])    

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
player_health = 3
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

background = pygame.image.load("graphics/space.svg").convert()
starship = pygame.image.load("graphics2/player.png").convert_alpha()
resized_image = pygame.transform.scale(starship, (70, 70))

enemy = pygame.image.load("graphics2/enemyShip.png").convert_alpha()
resized_enemy = pygame.transform.scale(enemy, (70, 70))

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
life_list = display_life()

ENEMY_FIRE_DELAY = 1000
last_enemy_shot_time = pygame.time.get_ticks()

running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shooting_sound.play()
                bullet_x = starship_x + 30
                bullet_y = starship_y - 15 
                bullets.append(pygame.Rect(bullet_x, bullet_y, 10, 20))  

    keys = pygame.key.get_pressed()

    screen.blit(background, (0,0))
    screen.blit(resized_image, (starship_x, starship_y))

    for life_image in life_list:
        screen.blit(life, life_image["rect"].topleft)
    
    for enemy_data in enemy_list:
        screen.blit(resized_enemy, enemy_data["rect"].topleft)

        if current_time - last_enemy_shot_time > ENEMY_FIRE_DELAY:
            for enemy_data in enemy_list:
                enemy_x, enemy_y = enemy_data["rect"].midbottom
                enemy_bullets.append(pygame.Rect(enemy_x, enemy_y, 10, 20))
            last_enemy_shot_time = current_time

    if len(enemy_list) == 0:
        current_time = pygame.time.get_ticks()  
        if current_time - start_time >= 3000:
    
    for enemy_bullet in enemy_bullets[:]:
        enemy_bullet.y += BULLET_SPEED  
        if enemy_bullet.y > HEIGHT: 
            enemy_bullets.remove(enemy_bullet)


    for enemy_bullet in enemy_bullets:
        screen.blit(enemy_bullet_img, enemy_bullet.topleft)

    for enemy_bullet in enemy_bullets[:]:
        if enemy_bullet.colliderect(pygame.Rect(starship_x, starship_y, 70, 70)):
            enemy_bullets.remove(enemy_bullet)  
            if player_health > 0:
                player_health -= 1  
                life_list.pop()
                if player_health == 0:
                    destroyed_sound.play()

    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and starship_x - 2 > 0:
        starship_x -= 5
    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and starship_x - 2 < 500:
        starship_x += 5
    if (keys[pygame.K_w] or keys[pygame.K_UP]) and starship_y - 2 > 0: 
        starship_y -= 5   
    if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and starship_y - 2 < 500: 
        starship_y += 5    


    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED  
        if bullet.y < -30: 
            bullets.remove(bullet)

    for bullet in bullets[:]:
        for enemy_data in enemy_list[:]:
            if check_collision(bullet, enemy_data):  
                enemy_data["health"] -= 1  
                bullets.remove(bullet)  
                if enemy_data["health"] <= 0:  
                    enemy_list.remove(enemy_data)
                    destroyed_sound.play()


    for bullet in bullets:
        screen.blit(bullet_img, bullet.topleft)

    pygame.display.update()  
    clock.tick(60)

pygame.quit()

