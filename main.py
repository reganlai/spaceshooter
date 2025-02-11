import pygame

def spawn_wave_one():
    screen.blit(resized_enemy, (150, 80))
    screen.blit(resized_enemy, (380, 80))
    screen.blit(resized_enemy, (270, 20))

pygame.init()

WIDTH, HEIGHT = 600, 600
BULLET_SPEED = 6
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

shooting_sound = pygame.mixer.Sound("graphics/pew.mp3")

starship_x = 270
starship_y = 500

bullets = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shooting_sound.play()
                bullet_x = starship_x + 30
                bullet_y = starship_y - 15 
                bullets.append([bullet_x, bullet_y])  # Store bullet position

    keys = pygame.key.get_pressed()

    screen.blit(background, (0,0))
    screen.blit(resized_image, (starship_x, starship_y))
    spawn_wave_one()

    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and starship_x - 2 > 0:
        starship_x -= 2
    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and starship_x - 2 < 500:
        starship_x += 2
    if (keys[pygame.K_w] or keys[pygame.K_UP]) and starship_y - 2 > 0: 
        starship_y -= 2   
    if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and starship_y - 2 < 500: 
        starship_y += 2    


    for bullet in bullets[:]:
        bullet[1] -= BULLET_SPEED  
        if bullet[1] < -30: 
            bullets.remove(bullet)


    for bullet in bullets:
        screen.blit(bullet_img, (bullet[0], bullet[1]))

    pygame.display.update()  
    clock.tick(60)

pygame.quit()

