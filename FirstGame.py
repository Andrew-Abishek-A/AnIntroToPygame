import os

import pygame
import time as tim
pygame.init()

ScreenTuple = (852, 480)

win = pygame.display.set_mode(ScreenTuple)

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load(os.path.join('Graphics', 'R1.png')),
             pygame.image.load(os.path.join('Graphics', 'R2.png')),
             pygame.image.load(os.path.join('Graphics', 'R3.png')),
             pygame.image.load(os.path.join('Graphics', 'R4.png')),
             pygame.image.load(os.path.join('Graphics', 'R5.png')),
             pygame.image.load(os.path.join('Graphics', 'R6.png')),
             pygame.image.load(os.path.join('Graphics', 'R7.png')),
             pygame.image.load(os.path.join('Graphics', 'R8.png')),
             pygame.image.load(os.path.join('Graphics', 'R9.png'))]
walkLeft = [pygame.image.load(os.path.join('Graphics', 'L1.png')),
            pygame.image.load(os.path.join('Graphics', 'L2.png')),
            pygame.image.load(os.path.join('Graphics', 'L3.png')),
            pygame.image.load(os.path.join('Graphics', 'L4.png')),
            pygame.image.load(os.path.join('Graphics', 'L5.png')),
            pygame.image.load(os.path.join('Graphics', 'L6.png')),
            pygame.image.load(os.path.join('Graphics', 'L7.png')),
            pygame.image.load(os.path.join('Graphics', 'L8.png')),
            pygame.image.load(os.path.join('Graphics', 'L9.png'))]
bullets_dir = [pygame.image.load(os.path.join('Graphics', 'bullets_1.png')),
               pygame.image.load(os.path.join('Graphics', 'bullets_3.png'))]
bg = pygame.image.load(os.path.join('Graphics', 'bg.jpg'))
char = pygame.image.load(os.path.join('Graphics', 'standing.png'))

clock = pygame.time.Clock()

music = pygame.mixer.music.load(os.path.join('Sounds', 'music.mp3'))
pygame.mixer.music.play(-1)

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.run = True
        self.right = False
        self.left = False
        self.walkCount = 0
        self.standing = True
        self.hitBox = (self.x + 17, self.y + 11, 29, 52)
        self.healthBar = [self.x + 17, self.y, 40, 10]
        self.health = 40
        self.score = 0
        self.shootLoop = 0
        self.visible = True
        self.bullets = 0

    def draw(self, win):
        if self.visible:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
            if not self.standing:
                if self.left:
                    win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
                elif self.right:
                    win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
            else:
                if self.right:
                    win.blit(walkRight[0], (self.x, self.y))
                else:
                    win.blit(walkLeft[0], (self.x, self.y))
            self.hitBox = (self.x + 17, self.y + 11, 29, 52)
            self.healthBar = [self.x + 17, self.y, self.health, 10]
            pygame.draw.rect(win, (255, 0, 0), (self.healthBar[0], self.healthBar[1], 40, self.healthBar[3]))
            pygame.draw.rect(win, (0, 128, 0), self.healthBar)
        # pygame.draw.rect(win, (255, 255, 255), self.hitBox, 2) was to show the hitbox

    def hit(self):
        if self.health > 0:
            self.health -= 5
        else:
            self.visible = False
        print('Man: HIT')


class Projectile(object):
    def __init__(self, x, y, radius, colour, facing, person):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.facing = facing
        self.vel = 8 * facing
        self.person = person

    def draw(self, win):
        if self.facing == 1:
            win.blit(bullets_dir[0], (self.x, self.y))
        else:
            win.blit(bullets_dir[1], (self.x, self.y))


class Enemy(object):
    walkRight = [pygame.image.load(os.path.join('Graphics', 'R1E.png')),
                 pygame.image.load(os.path.join('Graphics', 'R2E.png')),
                 pygame.image.load(os.path.join('Graphics', 'R3E.png')),
                 pygame.image.load(os.path.join('Graphics', 'R4E.png')),
                 pygame.image.load(os.path.join('Graphics', 'R5E.png')),
                 pygame.image.load(os.path.join('Graphics', 'R6E.png')),
                 pygame.image.load(os.path.join('Graphics', 'R7E.png')),
                 pygame.image.load(os.path.join('Graphics', 'R8E.png')),
                 pygame.image.load(os.path.join('Graphics', 'R9E.png')),
                 pygame.image.load(os.path.join('Graphics', 'R10E.png')),
                 pygame.image.load(os.path.join('Graphics', 'R11E.png'))
                 ]
    walkLeft = [pygame.image.load(os.path.join('Graphics', 'L1E.png')),
                pygame.image.load(os.path.join('Graphics', 'L2E.png')),
                pygame.image.load(os.path.join('Graphics', 'L3E.png')),
                pygame.image.load(os.path.join('Graphics', 'L4E.png')),
                pygame.image.load(os.path.join('Graphics', 'L5E.png')),
                pygame.image.load(os.path.join('Graphics', 'L6E.png')),
                pygame.image.load(os.path.join('Graphics', 'L7E.png')),
                pygame.image.load(os.path.join('Graphics', 'L8E.png')),
                pygame.image.load(os.path.join('Graphics', 'L9E.png')),
                pygame.image.load(os.path.join('Graphics', 'L10E.png')),
                pygame.image.load(os.path.join('Graphics', 'L11E.png'))
                ]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = (self.x, self.end)
        self.walkCount = 0
        self.vel = 5
        self.hitBox = (self.x + 10, self.y + 1, 31, 57)
        self.healthBar = [self.x + 10, self.y + 1, 40, 10]
        self.health = 40
        self.visible = True
        self.isJump = False
        self.jumpCount = 10
        self.standing = True
        self.right = False
        self.left = False
        self.shootLoop = 0
        self.score = 0
        self.bullets = 0

    def draw(self, win):
        # self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            if not self.standing:
                if self.left:
                    win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
                    self.hitBox = (self.x + 25, self.y + 1, 31, 57)
                elif self.right:
                    win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
                    self.hitBox = (self.x + 10, self.y + 1, 31, 57)
            else:
                if self.right:
                    win.blit(self.walkRight[0], (self.x, self.y))
                    self.hitBox = (self.x + 10, self.y + 1, 31, 57)
                else:
                    win.blit(self.walkLeft[0], (self.x, self.y))
                    self.hitBox = (self.x + 25, self.y + 1, 31, 57)
            self.healthBar = [self.x + 13, self.y - 5, self.health, 10]
            pygame.draw.rect(win, (255, 0, 0), (self.healthBar[0], self.healthBar[1], 40, self.healthBar[3]))
            pygame.draw.rect(win, (0, 128, 0), self.healthBar)
            # pygame.draw.rect(win, (255, 255, 255), self.hitBox, 2)

    # def move(self):
    #     if self.vel > 0:
    #         if self.x + self.vel < self.path[1]:
    #             self.x += self.vel
    #         else:
    #             self.vel *= -1
    #             self.walkCount = 0
    #     else:
    #         if self.x - self.vel > self.path[0]:
    #             self.x += self.vel
    #         else:
    #             self.vel *= -1
    #             self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 5
        else:
            self.visible = False
        print('Goblin: HIT')


def redraw_game_window():
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(man.score), 1, (0, 0, 0))
    win.blit(text, (700, 10))
    text = font.render('Score: ' + str(goblin.score), 1, (0, 0, 0))
    win.blit(text, (0, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    if not man.visible:
        text = font1.render('Goblin Wins', 1, (0, 0, 0))
        win.blit(text, (ScreenTuple[0] // 2 - 100, ScreenTuple[1] // 2))
    elif not goblin.visible:
        text = font1.render('Man Wins', 1, (0, 0, 0))
        win.blit(text, (ScreenTuple[0] // 2 - 125, ScreenTuple[1] // 2))
    pygame.display.update()
    if not man.visible or not goblin.visible:
        tim.sleep(5)
        man.run = False


# Mainloop
font = pygame.font.SysFont('comicsans', 30, True)
font1 = pygame.font.SysFont('comicsans', 60, True)
man = Player(50, 410, 64, 64)
goblin = Enemy(ScreenTuple[0] - 50, 420, 64, 64, 450)
bullets = []

while man.run:
    clock.tick(27)

    if man.shootLoop > 0:
        man.shootLoop += 1
    if man.shootLoop > 3:
        man.shootLoop = 0

    if goblin.shootLoop > 0:
        goblin.shootLoop += 1
    if goblin.shootLoop > 3:
        goblin.shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            man.run = False

    for bullet in bullets:
        if bullet.person == 1:
            if bullet.y - bullet.radius < goblin.hitBox[1] + goblin.hitBox[3] and bullet.y + bullet.radius > \
                    goblin.hitBox[1]:
                if bullet.x + bullet.radius > goblin.hitBox[0] and bullet.x - bullet.radius < goblin.hitBox[0] + \
                        goblin.hitBox[2]:
                    goblin.hit()
                    man.score += 1
                    man.bullets -= 1
                    bullets.pop(bullets.index(bullet))
        elif bullet.person == -1:
            if bullet.y - bullet.radius < man.hitBox[1] + man.hitBox[3] and bullet.y + bullet.radius > man.hitBox[1]:
                if bullet.x + bullet.radius > man.hitBox[0] and bullet.x - bullet.radius < man.hitBox[0] + man.hitBox[2]:
                    man.hit()
                    goblin.score += 1
                    goblin.bullets -= 1
                    bullets.pop(bullets.index(bullet))
        if 852 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            if bullet.facing == 1:
                man.bullets -= 1
                bullets.pop(bullets.index(bullet))
            else:
                goblin.bullets -= 1
                bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SLASH] and man.shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1
        if man.bullets < 5:
            bullets.append(Projectile(man.x + man.width // 2, man.y + man.height // 2, 6, (0, 0, 0), facing, 1))
            man.bullets += 1
        man.shootLoop = 1
    if keys[pygame.K_e] and goblin.shootLoop == 0:
        if goblin.left:
            facing = -1
        else:
            facing = 1
        if goblin.bullets < 5:
            bullets.append(
                Projectile(goblin.x + goblin.width // 2, goblin.y + goblin.height // 2, 6, (0, 0, 0), facing, -1))
            goblin.bullets += 1
        goblin.shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < ScreenTuple[0] - man.vel - man.width:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * neg / 2
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    if keys[pygame.K_a] and goblin.x > goblin.vel:
        goblin.x -= goblin.vel
        goblin.left = True
        goblin.right = False
        goblin.standing = False
    elif keys[pygame.K_d] and goblin.x < ScreenTuple[0] - goblin.vel - goblin.width:
        goblin.x += goblin.vel
        goblin.right = True
        goblin.left = False
        goblin.standing = False
    else:
        goblin.standing = True
        goblin.walkCount = 0
    if not goblin.isJump:
        if keys[pygame.K_w]:
            goblin.isJump = True
            goblin.left = False
            goblin.right = False
            goblin.walkCount = 0
    else:
        if goblin.jumpCount >= -10:
            neg = 1
            if goblin.jumpCount < 0:
                neg = -1
            goblin.y -= (goblin.jumpCount ** 2) * neg / 2
            goblin.jumpCount -= 1
        else:
            goblin.isJump = False
            goblin.jumpCount = 10
    redraw_game_window()

pygame.quit()
