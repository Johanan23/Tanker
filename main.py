import pygame
from pygame import mixer
import math
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load("background.jpg")
# background sound
mixer.music.load("background.mp3")
mixer.music.play(-1)
# game over text
game_over = pygame.font.Font("freesansbold.ttf", 80)


def show_gameover():
    over_text = game_over.render("GAME OVER", True, (225, 255, 255))

    screen.blit(over_text, (100, 200))


title = pygame.display.set_caption("SteveSRoaR Game")
path = pygame.image.load("joystick.png")
icon = pygame.display.set_icon(path)

# PLAYER SPITE
skin = pygame.image.load("joystick.png")
playerX = 370
playerY = 510
speed = 0
# ENEMY SPITE
enemy_skin = []
enemyX = []
enemyY = []
enemyspeedx = []
enemyspeedy = []
number_of_enemy = 30
for i in range(number_of_enemy):


    enemy_skin.append(pygame.image.load("Spaceship1.png"))
    enemyX.append(random.randint(0, 765))
    enemyY.append(random.randint(30, 350))
    enemyspeedx.append(1)
    enemyspeedy.append(40)
# BULLET
bullet_skin = pygame.image.load("bullet-arrow-up-icon.png")
bulletX = 0
bullety = 510
bulletspeedY = 0.8
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textx = 10
texty = 10


def display_score(x, y):
    score = font.render("score :" + str(score_value), True, (225, 225, 225))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(skin, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_skin[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_skin, (x + 8, y + 6))


def collusion(ex, ey, bx, by):
    distance = math.sqrt((math.pow(ex - bx, 2)) + (math.pow(ey - by, 2)))
    if distance < 26:
        return True
    else:
        return False


running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        # game machincs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed = -0.8
            if event.key == pygame.K_RIGHT:
                speed = 0.8
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    bullet(bulletX, bullety)
                    bullety += bulletspeedY

        if event.type == pygame.KEYUP:
            speed = 0

    # parallex background
    colour = screen.fill((0, 255, 250))
    screen.blit(background, ((0, 0)))
    # boundry for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 768:
        playerX = 768

    for i in range(number_of_enemy):
        if enemyY[i] > 450:
            for j in range(number_of_enemy):
                enemyY[j] = 2000
            show_gameover()
            break

        if enemyX[i] <= 0:
            enemyspeedx[i] = 0.3
            enemyY[i] += enemyspeedy[i]


        elif enemyX[i] >= 768:
            enemyspeedx[i] = -0.3
            enemyY[i] += enemyspeedy[i]

        co = collusion(enemyX[i], enemyY[i], bulletX, bullety)
        if co:
            bullety = 510
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 765)
            enemyY[i] = random.randint(30, 120)
        enemy(enemyX[i], enemyY[i], i)
        enemyX[i] += enemyspeedx[i]

    if bullety <= 0:
        bullety = 510
        bullet_state = "ready"

    # player function call
    playerX += speed

    player(playerX, playerY)
    display_score(textx, texty)
    playerX += speed
    if bullet_state == "fire":
        bullet(bulletX, bullety)
        bullety -= bulletspeedY

    pygame.display.update()
