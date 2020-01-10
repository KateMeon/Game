import pygame
from pygame import *
from random import choice, randrange

running = True
menu = True
game_over_scene = False

width = 500
height = 500
size = width, height
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('RUN')

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
        self.image = Surface((100, 100))
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
                self.image = image.load('gamer.png')
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
    global enemys

    def __init__(self):
        sprite.Sprite.__init__(self)
        self.enemys = [('man1.png'), ('man2.png'), ('man3.png')]
        self.enemys_r = [('man_r1.png'), ('man_r2.png'), ('man_r3.png')]
        self.image = pygame.Surface((100, 100))
        self.right_left = choice(['left', 'right'])
        if self.right_left == 'left':
            self.image = image.load(choice(self.enemys))
            self.rect = self.image.get_rect()
        else:
            self.image = image.load(choice(self.enemys_r))
            self.rect = self.image.get_rect()
        if len(enemys) > 1:
            self.coords_y = [e.rect.y for e in enemys]
            self.rect.y = randrange(10, 400)
            tf = False
            while not tf:
                tf = all([abs(self.rect.y - i) >= 100 for i in self.coords_y])
                if not tf:
                    self.rect.y = randrange(10, 400)
        else:
            self.rect.y = randrange(10, 400)
        if self.right_left == 'left':
            self.rect.x = randrange(540, 600)
        else:
            self.rect.x = randrange(-120, -70)
        self.speed_x = randrange(1, 5)

    def update(self):
        self.border = False
        if self.right_left == 'left':
            self.rect.x -= self.speed_x
            if self.rect.x < -70:
                self.border = True
                self.image = image.load(choice(self.enemys))
                self.rect.x = randrange(540, 600)
                self.speed_x = randrange(1, 5)
        else:
            self.rect.x += self.speed_x
            if self.rect.x > 600:
                self.border = True
                self.image = image.load(choice(self.enemys_r))
                self.rect.x = randrange(-120, -70)
                self.speed_x = randrange(1, 5)
        if self.border:
            self.coords_y = [e.rect.y for e in enemys]
            self.rect.y = randrange(10, 400)
            tf = False
            while not tf:
                tf = all([abs(self.rect.y - i) >= 100 for i in self.coords_y])
                if not tf:
                    self.rect.y = randrange(10, 400)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Camera:
    def __init__(self):
        self.dy = 1

    def apply(self, obj):
        obj.rect.y += self.dy


def menu_scene():
    global fon, fon_rect

    intro_text = ['RUN', 'if you can']

    fon = pygame.image.load('fon.jpg')
    fon_rect = fon.get_rect()
    screen.blit(fon, fon_rect)

    text_coord = 50
    font = pygame.font.Font(None, 30)

    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 50
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and \
                (menu or game_over_scene):
            menu = False
            if not game_over_scene:
                hero = Player()
                left = right = False
                all_sprites.add(hero)
                camera = Camera()

                UPDATECAMERA = USEREVENT + 0
                for i in range(randrange(2, 5)):
                    enemy = Enemy()
                    all_sprites.add(enemy)
                    enemys.add(enemy)

            game_over_scene = False
            game_scene()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and not menu and not\
                game_over_scene:
            left = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and not menu and not\
                game_over_scene:
            right = True

        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT and not menu and not\
                game_over_scene:
            left = False
            hero.image = image.load('gamer.png')
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT and not menu and not\
                game_over_scene:
            right = False
            hero.image = image.load('gamer.png')

        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and not menu and not\
                game_over_scene:
            hero.rect.y += hero.speed_y
            if hero.rect.y > 410:
                hero.rect.y = 410
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and not menu and not\
                game_over_scene:
            hero.rect.y -= hero.speed_y
            if hero.rect.y < -10:
                hero.rect.y = -10
        if menu:
            menu_scene()
    screen.blit(fon, (0, 0))
    if not menu and not game_over_scene:
        hero.update(left, right)
        hero.draw(screen)
        for e in enemys:
            e.update()
            e.draw(screen)
        hits = pygame.sprite.spritecollide(hero, enemys, False)
        if event.type == UPDATECAMERA:
            for sprite in all_sprites:
                camera.apply(sprite)
        if hits:
            game_over_scene = True
            game_over()
        pygame.time.set_timer(UPDATECAMERA, 35)
    pygame.display.update()
