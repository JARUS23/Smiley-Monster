import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Title and Icon
pygame.display.set_caption("Smiley Monster")
icon = pygame.image.load('res/logo.png')
pygame.display.set_icon(icon)

# BackGround
background = pygame.image.load('res/background.png')

# Player
playerImg = pygame.image.load('res/player.png')
playerX = 320
playerY = 480
playerX_change = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('res/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2.5)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('res/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 20)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# FPS
clock = pygame.time.Clock()


def show_score(x, y):
    score = font.render("Score - " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# create the screen
screen = pygame.display.set_mode((800, 600))

# Game Loop
running = True
while running:
    dt = clock.tick(60)

    # Reset the screen
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # All Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Left and Right Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('res/laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Movement & Boundaries of Player
    playerX = playerX + playerX_change * (dt / 10)
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Movement & Boundaries of Enemy
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 430:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] = enemyX[i] + enemyX_change[i] * (dt / 10)
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.5
            enemyY[i] = enemyY[i] + enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1.5
            enemyY[i] = enemyY[i] + enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('res/explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value = score_value + 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY = bulletY - bulletY_change * (dt / 10)

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
