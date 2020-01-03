import pygame
from pygame import *
from random import choice, randrange

running = True
menu = True

width = 500
height = 500
size = width, height
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('GREEN ROADs')

timer = pygame.time.Clock()
fps = 60

fon = pygame.image.load('fon.jpg')
fon_rect = fon.get_rect()
screen.blit(fon, fon_rect)
pygame.display.update()
all_sprites = pygame.sprite.Group()
enemys = pygame.sprite.Group()


class Player(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.step_right = [('right_1.png'), ('right_2.png'), ('right_3.png'), ('right_4.png')]
        self.step_left = [('left_1.png'), ('left_2.png'), ('left_3.png'), ('left_4.png')]
        self.move = 0
        self.speed = 5
        self.step_r = 0
        self.step_l = 0
        self.speed_y = 20
        self.startX = 120
        self.startY = 400
        self.image = Surface((30, 30))
        self.image = image.load('gamer.png')
        self.rect = Rect(self.startX, self.startY, 30, 30)

    def update(self, left_l, right_r):
        global right, left
        if left_l:
            self.step_l = (self.step_l + 1) % len(self.step_right)
            self.image = image.load(self.step_left[self.step_l])
            hero.rect.x -= hero.speed
            if hero.rect.x < -20:
                hero.rect.x = -20
                left = False
        if right_r:
            self.step_r = (self.step_r + 1) % len(self.step_right)
            self.image = image.load(self.step_right[self.step_r])
            hero.rect.x += hero.speed
            if hero.rect.x > 420:
                hero.rect.x = 420
                right = False
                self.image = image.load('gamer.png')

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Enemy(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.enemys = [('man1.png'), ('man2.png'), ('man3.png'), ('man4.png'), ('man5.png'),
                       ('man6.png')]
        self.image = pygame.Surface((10, 10))
        self.image = image.load(choice(self.enemys))
        self.rect = self.image.get_rect()
        if len(enemys) > 0:
            for e in enemys:
                self.rect.y = randrange(10, 400)

        else:
            self.rect.y = randrange(10, 400)
        self.rect.x = randrange(-50, -20)
        self.speed_x = randrange(5, 10)
    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.x < -30:
            self.rect.x = randrange(540, 600)
            self.rect.y = randrange(10, 400)
            self.speed_x = randrange(1, 5)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


def menu_scene():
    global fon, fon_rect
    fon = pygame.image.load('fon.jpg')
    fon_rect = fon.get_rect()
    screen.blit(fon, fon_rect)
    pygame.display.update()


def game_scene():
    global fon, fon_rect
    fon = pygame.image.load('fon_game.jpeg')
    fon_rect = fon.get_rect()
    screen.blit(fon, fon_rect)
    pygame.display.update()


def game_over():
    global fon, fon_rect
    fon = pygame.image.load('fon_game.jpeg')
    fon_rect = fon.get_rect()
    screen.blit(fon, fon_rect)
    pygame.display.update()


while running:
    timer.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and menu:
            menu = False
            hero = Player()
            left = right = False
            all_sprites.add(hero)
            for i in range(3):
                enemy = Enemy()
                all_sprites.add(enemy)
                enemys.add(enemy)
            game_scene()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and not menu:
            left = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and not menu:
            right = True

        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT and not menu:
            left = False
            hero.image = image.load('gamer.png')
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT and not menu:
            right = False
            hero.image = image.load('gamer.png')
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and not menu:
            hero.rect.y += hero.speed_y
            if hero.rect.y > 410:
                hero.rect.y = 410
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and not menu:
            hero.rect.y -= hero.speed_y
            if hero.rect.y < -10:
                hero.rect.y = -10
        if menu:
            menu_scene()
    screen.blit(fon, (0, 0))
    if not menu:
        hero.update(left, right)
        hero.draw(screen)
        for e in enemys:
            e.update()
            e.draw(screen)
        hits = pygame.sprite.spritecollide(hero, enemys, False)
        if hits:
            running = False
            game_over()
    pygame.display.update()
