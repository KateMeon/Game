import sys
import pygame
from pygame import *
from random import choice, randrange

running = True
start = True
game_over_scene = False
game = False

width = 500
height = 500
size = width, height
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('RUN')

clock = pygame.time.Clock()
fps = 60

fon = pygame.image.load('fon.jpg')
fon_rect = fon.get_rect()
screen.blit(fon, fon_rect)
pygame.display.update()

all_sprites = pygame.sprite.Group()
enemys = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


class Player(sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.step_right = [('right_1.png'), ('right_2.png'), ('right_3.png'), ('right_4.png')]
        self.step_left = [('left_1.png'), ('left_2.png'), ('left_3.png'), ('left_4.png')]
        self.move = 0
        self.speed = 5
        self.step_r = 0
        self.step_l = 0
        self.speed_y = 20  # скорость игрока при движении вверх
        self.startX = 120  # начальное положение игрока по оси х
        self.startY = 380  # начальное положение игрока по оси у
        self.image = Surface((100, 100))
        self.image = image.load('player.png')
        self.rect = Rect(self.startX, self.startY, 30, 30)

    def update(self, left_l, right_r):
        global right, left, game

        if left_l:
            self.step_l = (self.step_l + 1) % len(self.step_right)
            self.image = image.load(self.step_left[self.step_l])  # анимация движения влево
            hero.rect.x -= hero.speed
            if hero.rect.x < -20:
                hero.rect.x = -20
                left = False
                self.image = image.load('player.png')  # остановка игрока при касании границы
        if right_r:
            self.step_r = (self.step_r + 1) % len(self.step_right)
            self.image = image.load(self.step_right[self.step_r])  # анимация движения вправо
            hero.rect.x += hero.speed
            if hero.rect.x > 420:
                hero.rect.x = 420
                right = False
                self.image = image.load(
                    'player.png')  # остановка анимации игрока при касании границы
        self.rect.y += 1  # "движение камеры"

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Enemy(sprite.Sprite):
    def __init__(self):
        super().__init__(enemys)
        self.enemys = [('man1.png'), ('man2.png'), ('man3.png')]
        self.enemys_r = [('man_r1.png'), ('man_r2.png'), ('man_r3.png')]
        self.image = pygame.Surface((100, 100))
        self.right_left = choice(['left', 'right'])  # рандомный выбор направления движения игрока
        if self.right_left == 'left':
            self.image = image.load(choice(self.enemys))
            self.rect = self.image.get_rect()
            self.rect.x = randrange(540, 600)
        else:
            self.image = image.load(choice(self.enemys_r))
            self.rect = self.image.get_rect()
            self.rect.x = randrange(-120, -70)
        self.rect.y = randrange(-10, 400)
        if len(enemys) > 1:  # проверка координат по оси у
            self.coords_y = [e.rect.y for e in enemys]
            tf = False
            while not tf:
                tf = all([abs(self.rect.y - i) >= 100 for i in self.coords_y if i != self.rect.y])
                if not tf:
                    self.rect.y = randrange(-10, 400)
        self.speed_x = randrange(2, 6)

    def update(self):
        self.border = False
        if self.right_left == 'left':
            self.rect.x -= self.speed_x
            if self.rect.x < -70:  # проверка касания границы
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
            self.rect.y = randrange(10, 400)
            self.coords_y = [e.rect.y for e in enemys]
            tf = False
            while not tf:
                tf = all([abs(self.rect.y - i) >= 100 for i in self.coords_y if i != self.rect.y])
                if not tf:
                    self.rect.y = randrange(-10, 400)
        self.rect.y += 1


def start_scene():
    global fon, fon_rect, start, game

    intro_text = ['RUN', 'if you can', 'Press \'space\' to start the game']

    fon = pygame.image.load('fon.jpg')
    fon_rect = fon.get_rect()
    screen.blit(fon, fon_rect)

    text_coord = 100

    for line in intro_text:
        if line == 'RUN':
            font = pygame.font.Font(None, 200)
            color = '#00733C'
            coord_x = 100
        else:
            font = pygame.font.Font(None, 40)
            if line == 'if you can':
                coord_x = 180
                color = 'black'
            else:
                text_coord += 30
                color = '#1C1C1C'
                coord_x = 50
        string_rendered = font.render(line, 1, pygame.Color(color))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = coord_x
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                start = False
                game = True
        pygame.display.flip()
        clock.tick(fps)


def check_rotation(keys):  # проверка нажатия клавиш
    left = right = False
    if keys[pygame.K_LEFT]:
        left = True
    if keys[pygame.K_RIGHT]:
        right = True
    return left, right


def draw_text(surf, score):  # отрисовка счета игры
    font = pygame.font.Font(None, 30)
    text_surface = font.render(score, 1, pygame.Color('black'))
    text_rect = text_surface.get_rect()
    text_rect.y = 450
    text_rect.x = 420
    surf.blit(text_surface, text_rect)


def game_scene():
    global fon, fon_rect, game, hero, game_over_scene
    # загрузка звукового сопровождения игры
    pygame.mixer.init()
    pygame.mixer.music.load('gazonokosilka.mp3')
    pygame.mixer.music.play(-1, 0.0)

    fon = pygame.image.load('fon_game.jpeg')
    fon_rect = fon.get_rect()
    screen.blit(fon, fon_rect)
    pygame.display.update()
    hero = Player()
    left = right = False
    score = 0

    [Enemy() for i in range(randrange(3, 6))]  # создание рандомного количества врагов

    while game:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            left, right = check_rotation(pygame.key.get_pressed())  # проверка нажатых клавиш
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                hero.rect.y -= hero.speed_y
                if hero.rect.y < -10:
                    hero.rect.y = -10
                score += 1
            # проверка отпуска клавиш
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                left = False
                hero.image = image.load('player.png')  # остановка анимации игрока
            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                right = False
                hero.image = image.load('player.png')  # остановка анимации игрока
        # обновление всех персонажей
        screen.blit(fon, (0, 0))
        hero.update(left, right)
        hero.draw(screen)
        enemys.update()
        enemys.draw(screen)
        draw_text(screen, str(score))  # отрисовка счета
        # проверка на пересечение игрока с врагами и касания нижней границы
        if pygame.sprite.spritecollide(hero, enemys, False) or hero.rect.bottom > 480:
            game = False  # конец игры
            game_over_scene = True
            # прекращение музыкального сопровождения игры и загрузка последнего звука проигрыша
            pygame.mixer.music.pause()
            pygame.mixer.music.load('oh.mp3')
            pygame.mixer.music.play(1, 0.0)
        pygame.display.update()


def game_over():
    global fon, fon_rect, game_over_scene, game, start, all_sprites, enemys

    intro_text = ['GAME', 'OVER', 'Press \'space\' to start over']
    # загрузка фона
    fon = pygame.image.load('fon.jpg')
    fon_rect = fon.get_rect()
    screen.blit(fon, fon_rect)
    # координаты текста
    text_coord = 50
    # загрузка текста о проигрыше
    for line in intro_text:
        coord_x = 50
        if line == 'GAME' or line == 'OVER':
            font = pygame.font.Font(None, 200)
            color = '#00733C'
            text_coord += 10
            if line == 'OVER':
                coord_x = 70
        else:
            font = pygame.font.Font(None, 40)
            text_coord += 30
            color = '#1C1C1C'
            coord_x = 80
        string_rendered = font.render(line, 1, pygame.Color(color))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = coord_x
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while game_over_scene:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # возвращение к стартовому экрану
                start = True
                game_over_scene = False
                # обновление групп
                all_sprites = pygame.sprite.Group()
                enemys = pygame.sprite.Group()

        pygame.display.flip()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    if start:
        start_scene()
    elif game:
        game_scene()
    elif game_over_scene:
        game_over()
