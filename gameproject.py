import pygame
import os
import random


#Vx = float(input("Input Vx : "))
#Vy = float(input("Input Vy : "))
Vx = 20
Vy = 20

#GEOMETRY
screen_width = 1000
screen_height = 600
FPS = 30

#COLOR
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (204, 153, 255)
RED = (255, 0, 0)
WHITE = (155, 25, 0)
colorList = [BLUE, BLACK, GREEN, RED, WHITE]

#Initialize pygame
pygame.init()
path = os.path.dirname(__file__)
img_path = os.path.join(path, 'Gallery')
background = pygame.image.load('Gallery/parallax.png')
background = pygame.transform.scale(background, [screen_width, screen_height])
win = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Stateczek shoot Projectile")
clock = pygame.time.Clock()

pixelRatio = 10
accel = -9.81
timeStep = 1 / FPS
font = pygame.font.SysFont('comic', 50, False, False)

#####CREATE SPRITE#####
class player(pygame.sprite.Sprite):
    image = pygame.image.load(os.path.join(path, 'Gallery', 'life.png'))  # เรียกรูปตัวละครมาเก็บในตัวแปร
    def __init__(self, x, y):  # ฟังก์ชั่นนี้เอาไว้กำหนดตัวแปร
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.move = 10

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

#####CREATE PROJECTILE SHOOT#####
class projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, ux, uy):
        pygame.sprite.Sprite.__init__(self)
        self.x = x + 30
        self.y = y
        self.startX = self.x
        self.startY = self.y
        self.horVel = ux
        self.verVel = uy
        self.color = random.choice(colorList)
        self.bulletTime = 0.0
        self.status = 1

    def update(self):
        global maxHeight
        global maxHeightPos
        global landingPos
        global ranges
        global trace
        if self.y <= screen_height:
            self.bulletTime += timeStep
            self.x = (self.horVel * self.bulletTime) * pixelRatio + self.startX
            self.y = -(self.verVel * self.bulletTime + 0.5 * accel * (
                        self.bulletTime ** 2)) * pixelRatio + self.startY

            trace.append([self.x, self.y])
            if self.x >= screen_width:
                self.status = 0
            if self.y < 0:
                self.status = 0
        else:  # กระสุนลงพื้น
            self.status = 0

            pygame.display.update()

    def draw(self, win):
        pygame.draw.circle(win, self.color, (round(self.x), round(self.y)), 6)
        for t in traceShow:
            pygame.draw.circle(win, self.color, (round(t[0]), round(t[1])), 1)


#####CREATE ENEMYS#####
class enemy(pygame.sprite.Sprite):
    im = pygame.image.load(os.path.join(path, 'Gallery', 'stateczek.png'))
    im2 = pygame.image.load(os.path.join(path, 'Gallery', 'stateczek.png'))
    im3 = pygame.image.load(os.path.join(path, 'Gallery', 'stateczek.png'))
    imageList = [im, im2, im3]

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.hitbox = (self.x, self.y, 60, 60)
        self.vel = 6
        self.imageRandom = random.choice(self.imageList)

    def draw(self, win):
        self.move_enemy()
        win.blit(self.imageRandom, (self.x, self.y))

    def move_enemy(self):
        if self.vel > 0:
            if self.y + self.vel < 560:
                self.y += self.vel
                self.hitbox = (self.x, self.y, 60, 60)
            else:
                self.vel = self.vel * -1
        else:
            if self.y - self.vel > 10:
                self.y += self.vel
                self.hitbox = (self.x, self.y, 60, 60)
            else:
                self.vel = self.vel * -1


#####FUNCTION SHOW DISPLAY####
def display(s):
    win.blit(background, (0, 0))
    player1.draw(win)
    Monster1.draw(win)
    Monster2.draw(win)
    Monster3.draw(win)
    score = font.render('Score : ' + str(s), 1, (0, 0, 0))
    win.blit(score, (430, 30))
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


# mainloop
Y = 300
X = 30
X1 = random.randint(500, 590)
X2 = random.randint(660, 760)
X3 = random.randint(830, 900)
Y1 = random.randint(60, 720)
Y2 = random.randint(40, 720)
Y3 = random.randint(60, 720)

player1 = player(X, Y)
Monster1 = enemy(X1, Y1)
Monster2 = enemy(X2, Y2)
Monster3 = enemy(X3, Y3)

bullets = []
trace = []
traceShow = []
color = []
resetTrace = False
shootStage = 0
showText = 0
maxHeight = 0
ranges = 0
r = 1
s = 0

### START ###
runing = True
while runing:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if player1.y > 0:
            player1.y -= player1.move
        else:
            player1.y = 0

    if keys[pygame.K_DOWN]:
        if player1.y < screen_height-30:
            player1.y += player1.move
            print(player1.y)
        else:
            player1.y = screen_height-30
            print(player1.y)
    if keys[pygame.K_RIGHT]:
        if player1.x < screen_width-540:
            player1.x += player1.move
            print(player1.x)
        else:
            player1.x = screen_width-540
            print(player1.x)
    if keys[pygame.K_LEFT]:
        if player1.x > 0:
            player1.x -= player1.move
        else:
            player1.x = 0

    if keys[pygame.K_SPACE]:
        if shootStage == 0:
            bullets.append(projectile(player1.x, player1.y, Vx, Vy))
            shootStage = 1
            trace.clear()

    for bullet in bullets:
        bullet.update()
        traceShow = trace
        if bullet.y - 5 < Monster1.hitbox[1] + Monster1.hitbox[3] and bullet.y + 5 > Monster1.hitbox[1]:
            if bullet.x + 5 > Monster1.hitbox[0] and bullet.x - 5 < Monster1.hitbox[0] + Monster1.hitbox[2]:
                bullet.status = 0
                X1 = random.randint(500, 590)
                Y1 = random.randint(60, 720)

                Monster1 = enemy(X1, Y1)
                s += 1
        if bullet.y - 5 < Monster2.hitbox[1] + Monster2.hitbox[3] and bullet.y + 5 > Monster2.hitbox[1]:
            if bullet.x + 5 > Monster2.hitbox[0] and bullet.x - 5 < Monster2.hitbox[0] + Monster2.hitbox[2]:
                bullet.status = 0
                X2 = random.randint(660, 760)
                Y2 = random.randint(60, 720)
                Monster2 = enemy(X2, Y2)
                s += 1
        if bullet.y - 5 < Monster3.hitbox[1] + Monster3.hitbox[3] and bullet.y + 5 > Monster3.hitbox[
            1]:
            if bullet.x + 5 > Monster3.hitbox[0] and bullet.x - 5 < Monster3.hitbox[0] + Monster3.hitbox[
                2]:
                bullet.status = 0
                X3 = random.randint(830, 900)
                Y3 = random.randint(60, 720)
                Monster3 = enemy(X3, Y3)
                s += 1
        if bullet.status == 0:
            shootStage = 0
            bullets.pop(bullets.index(bullet))

    display(s)
    pygame.display.update()

pygame.quit()

