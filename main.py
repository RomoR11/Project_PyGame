import pygame
import sys
import os
import csv


pygame.init()


width, height = 640, 480
screen = pygame.display.set_mode((width, height))
FPS = 60
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
border_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
unused_bullet_group = pygame.sprite.Group()
STOP, LEFT, RIGHT, JUMP = 0, 1, 2, 3
player_motion = STOP
bullet_flip = False
level_number = 1
levels_dict = dict()
for i in open('data/levels.txt', mode='r').read().split('\n'):
    levels_dict[i.split(':')[0]] = i.split(':')[1]


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    main_menu_screen = pygame.transform.scale(load_image('main_menu_screen.png'), (width, height))
    screen.blit(main_menu_screen, (0, 0))
    start_game_button = pygame.draw.rect(screen, 'white', pygame.Rect(210, 200, 200, 80), 3, 10)
    pygame.draw.rect(screen, 'DarkMagenta', pygame.Rect(213, 203, 194, 74), 0, 10)
    exit_button = pygame.draw.rect(screen, 'white', pygame.Rect(210, 310, 200, 80), 3, 10)
    pygame.draw.rect(screen, 'DarkMagenta', pygame.Rect(213, 313, 194, 74), 0, 10)
    font_start_game = pygame.font.Font(None, 35)
    string_rendered = font_start_game.render('Играть', 1, 'black')
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 230
    intro_rect.x = 268
    screen.blit(string_rendered, intro_rect)
    string_rendered = font_start_game.render('Выйти из игры', 1, 'black')
    intro_rect.top = 340
    intro_rect.x = 220
    screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_game_button.x <= event.pos[0] <= start_game_button.x + start_game_button.width and\
                        start_game_button.y <= event.pos[1] <= start_game_button.y + start_game_button.height:
                    change_level_screen()
                    return
                elif exit_button.x <= event.pos[0] <= exit_button.x + exit_button.width and\
                        exit_button.y <= event.pos[1] <= exit_button.y + exit_button.height:
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


def get_button_color(level):
    if levels_dict[level] == 'True':
        return 'DarkMagenta'
    else:
        return 'Black'


def change_level_screen():
    global level_number, player_motion, player, flag, level_x, level_y
    title_text = 'Уровни'
    screen.fill('DarkSeaGreen')
    font_title = pygame.font.Font('data/SAIBA-45.otf', 35)
    string_rendered = font_title.render(title_text, 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 30
    intro_rect.x = 250
    screen.blit(string_rendered, intro_rect)
    first_level_button = pygame.draw.rect(screen, 'white', pygame.Rect(40, 150, 180, 80), 3, 10)
    pygame.draw.rect(screen, get_button_color('level_1'), pygame.Rect(43, 153, 174, 74), 0, 10)
    second_level_button = pygame.draw.rect(screen, 'white', pygame.Rect(240, 150, 180, 80), 3, 10)
    pygame.draw.rect(screen, get_button_color('level_2'), pygame.Rect(243, 153, 174, 74), 0, 10)
    third_level_button = pygame.draw.rect(screen, 'white', pygame.Rect(440, 150, 180, 80), 3, 10)
    pygame.draw.rect(screen, get_button_color('level_3'), pygame.Rect(443, 153, 174, 74), 0, 10)
    fourth_level_button = pygame.draw.rect(screen, 'white', pygame.Rect(40, 300, 180, 80), 3, 10)
    pygame.draw.rect(screen, get_button_color('level_4'), pygame.Rect(43, 303, 174, 74), 0, 10)
    fifth_level_button = pygame.draw.rect(screen, 'white', pygame.Rect(240, 300, 180, 80), 3, 10)
    pygame.draw.rect(screen, get_button_color('level_5'), pygame.Rect(243, 303, 174, 74), 0, 10)
    sixth_level_button = pygame.draw.rect(screen, 'white', pygame.Rect(440, 300, 180, 80), 3, 10)
    pygame.draw.rect(screen, get_button_color('level_6'), pygame.Rect(443, 303, 174, 74), 0, 10)
    font_level = pygame.font.Font(None, 30)
    string_rendered = font_level.render('Первый', 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 180
    intro_rect.x = 90
    screen.blit(string_rendered, intro_rect)
    string_rendered = font_level.render('Второй', 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 180
    intro_rect.x = 295
    screen.blit(string_rendered, intro_rect)
    string_rendered = font_level.render('Третий', 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 180
    intro_rect.x = 495
    screen.blit(string_rendered, intro_rect)
    string_rendered = font_level.render('Четвёртый', 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 330
    intro_rect.x = 75
    screen.blit(string_rendered, intro_rect)
    string_rendered = font_level.render('Пятый', 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 330
    intro_rect.x = 299
    screen.blit(string_rendered, intro_rect)
    string_rendered = font_level.render('Шестой', 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 330
    intro_rect.x = 490
    screen.blit(string_rendered, intro_rect)
    if levels_dict['level_2'] == 'False':
        screen.blit(padlock_image, (310, 162))
    if levels_dict['level_3'] == 'False':
        screen.blit(padlock_image, (510, 162))
    if levels_dict['level_4'] == 'False':
        screen.blit(padlock_image, (110, 312))
    if levels_dict['level_5'] == 'False':
        screen.blit(padlock_image, (310, 312))
    if levels_dict['level_6'] == 'False':
        screen.blit(padlock_image, (510, 312))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if first_level_button.x <= event.pos[0] <= first_level_button.x + first_level_button.width and\
                        first_level_button.y <= event.pos[1] <= first_level_button.y + first_level_button.height:
                    level_number = 1
                    player, flag, level_x, level_y = generate_level(levels[level_number])
                    return
                elif second_level_button.x <= event.pos[0] <= second_level_button.x + second_level_button.width and\
                        second_level_button.y <= event.pos[1] <= second_level_button.y + second_level_button.height and\
                        levels_dict['level_2'] == 'True':
                    level_number = 2
                    player, flag, level_x, level_y = generate_level(levels[level_number])
                    return
                elif third_level_button.x <= event.pos[0] <= third_level_button.x + third_level_button.width and\
                        third_level_button.y <= event.pos[1] <= third_level_button.y + third_level_button.height and\
                        levels_dict['level_3'] == 'True':
                    level_number = 3
                    player, flag, level_x, level_y = generate_level(levels[level_number])
                    return
                elif fourth_level_button.x <= event.pos[0] <= fourth_level_button.x + fourth_level_button.width and\
                        fourth_level_button.y <= event.pos[1] <= fourth_level_button.y + fourth_level_button.height and\
                        levels_dict['level_4'] == 'True':
                    level_number = 4
                    player, flag, level_x, level_y = generate_level(levels[level_number])
                    return
                elif fifth_level_button.x <= event.pos[0] <= fifth_level_button.x + fifth_level_button.width and\
                        fifth_level_button.y <= event.pos[1] <= fifth_level_button.y + fifth_level_button.height and\
                        levels_dict['level_5'] == 'True':
                    level_number = 5
                    player, flag, level_x, level_y = generate_level(levels[level_number])
                    return
                elif sixth_level_button.x <= event.pos[0] <= sixth_level_button.x + sixth_level_button.width and\
                        sixth_level_button.y <= event.pos[1] <= sixth_level_button.y + sixth_level_button.height and\
                        levels_dict['level_6'] == 'True':
                    level_number = 6
                    player, flag, level_x, level_y = generate_level(levels[level_number])
                    return
        pygame.display.flip()
        clock.tick(FPS)


def pause_screen():
    global level_number, player_motion, player, flag, level_x, level_y
    title_text = 'Пауза'
    screen.fill('DarkSeaGreen')
    font_title = pygame.font.Font('data/SAIBA-45.otf', 35)
    string_rendered = font_title.render(title_text, 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 30
    intro_rect.x = 250
    screen.blit(string_rendered, intro_rect)
    return_game_button = pygame.draw.rect(screen, 'white', pygame.Rect(210, 170, 200, 80), 3, 10)
    pygame.draw.rect(screen, 'DarkMagenta', pygame.Rect(213, 173, 194, 74), 0, 10)
    return_button = pygame.draw.rect(screen, 'white', pygame.Rect(210, 280, 200, 80), 3, 10)
    pygame.draw.rect(screen, 'DarkMagenta', pygame.Rect(213, 283, 194, 74), 0, 10)
    exit_button = pygame.draw.rect(screen, 'white', pygame.Rect(210, 390, 200, 80), 3, 10)
    pygame.draw.rect(screen, 'DarkMagenta', pygame.Rect(213, 393, 194, 74), 0, 10)
    font_start_game = pygame.font.Font(None, 35)
    string_rendered = font_start_game.render('Продолжить', 1, 'black')
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 200
    intro_rect.x = 225
    screen.blit(string_rendered, intro_rect)
    string_rendered = font_start_game.render('Выйти в меню', 1, 'black')
    intro_rect.top = 310
    intro_rect.x = 225
    screen.blit(string_rendered, intro_rect)
    string_rendered = font_start_game.render('Выйти из игры', 1, 'black')
    intro_rect.top = 420
    intro_rect.x = 220
    screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_game_button.x <= event.pos[0] <= return_game_button.x + return_game_button.width and \
                        return_game_button.y <= event.pos[1] <= return_game_button.y + return_game_button.height:
                    return
                elif exit_button.x <= event.pos[0] <= exit_button.x + exit_button.width and \
                        exit_button.y <= event.pos[1] <= exit_button.y + exit_button.height:
                    terminate()
                elif return_button.x <= event.pos[0] <= return_button.x + return_button.width and \
                        return_button.y <= event.pos[1] <= return_button.y + return_button.height:
                    level_number = 1
                    player_motion = STOP
                    camera.dx = 0
                    all_sprites.empty()
                    border_group.empty()
                    flag_group.empty()
                    player_group.empty()
                    enemy_group.empty()
                    platform_group.empty()
                    start_screen()
                    return
        pygame.display.flip()
        clock.tick(FPS)


def finish_screen(win=False):
    global level_number, player_motion, player, flag, level_x, level_y
    title_text = 'Поражение' if not win else 'Победа'
    button_text = 'Играть заново' if not win or level_number == 6 else 'След уровень'
    screen.fill('DarkSeaGreen')
    font_title = pygame.font.Font('data/SAIBA-45.otf', 35)
    string_rendered = font_title.render(title_text, 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 30
    intro_rect.x = 190 if title_text == 'Поражение' else 225
    screen.blit(string_rendered, intro_rect)
    return_game_button = pygame.draw.rect(screen, 'white', pygame.Rect(210, 170, 200, 80), 3, 10)
    pygame.draw.rect(screen, 'DarkMagenta', pygame.Rect(213, 173, 194, 74), 0, 10)
    return_button = pygame.draw.rect(screen, 'white', pygame.Rect(210, 280, 200, 80), 3, 10)
    pygame.draw.rect(screen, 'DarkMagenta', pygame.Rect(213, 283, 194, 74), 0, 10)
    exit_button = pygame.draw.rect(screen, 'white', pygame.Rect(210, 390, 200, 80), 3, 10)
    pygame.draw.rect(screen, 'DarkMagenta', pygame.Rect(213, 393, 194, 74), 0, 10)
    font_start_game = pygame.font.Font(None, 35)
    string_rendered = font_start_game.render(button_text, 1, 'black')
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 200
    intro_rect.x = 225
    screen.blit(string_rendered, intro_rect)
    string_rendered = font_start_game.render('Выйти в меню', 1, 'black')
    intro_rect.top = 310
    intro_rect.x = 225
    screen.blit(string_rendered, intro_rect)
    string_rendered = font_start_game.render('Выйти из игры', 1, 'black')
    intro_rect.top = 420
    intro_rect.x = 220
    screen.blit(string_rendered, intro_rect)
    all_sprites.empty()
    border_group.empty()
    flag_group.empty()
    player_group.empty()
    enemy_group.empty()
    platform_group.empty()
    if win and level_number < 6:
        levels_dict[f'level_{level_number + 1}'] = 'True'
        update_levels(levels_dict)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_game_button.x <= event.pos[0] <= return_game_button.x + return_game_button.width and \
                        return_game_button.y <= event.pos[1] <= return_game_button.y + return_game_button.height and \
                        win and level_number < 6:
                    level_number += 1
                    player, flag, level_x, level_y = generate_level(levels[level_number])
                    return
                elif return_game_button.x <= event.pos[0] <= return_game_button.x + return_game_button.width and \
                        return_game_button.y <= event.pos[1] <= return_game_button.y + return_game_button.height and \
                        (not win or level_number == 6):
                    player, flag, level_x, level_y = generate_level(levels[level_number])
                    return
                elif exit_button.x <= event.pos[0] <= exit_button.x + exit_button.width and \
                        exit_button.y <= event.pos[1] <= exit_button.y + exit_button.height:
                    terminate()
                elif return_button.x <= event.pos[0] <= return_button.x + return_button.width and \
                        return_button.y <= event.pos[1] <= return_button.y + return_button.height:
                    level_number = 1
                    player_motion = STOP
                    camera.dx = 0
                    start_screen()
                    return
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def generate_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as csvfile:
        r = csv.reader(csvfile, delimiter=';', quotechar='"')
        data = [[row[0], row[1], row[2], row[3], row[4]] for row in r]
    new_player, new_flag, max_width, max_height = None, None, 0, 0
    for i in data:
        if i[0] == 'player':
            new_player = Player(int(i[1]), int(i[2]))
        elif i[0] == 'platform':
            if i[3] == 'border':
                Platform('border', int(i[1]), int(i[2]), i[3])
            elif level_number in (1, 2, 6):
                Platform('platform_1_2_6', int(i[1]), int(i[2]), i[3])
            else:
                Platform(f'platform_{level_number}', int(i[1]), int(i[2]), i[3])
        elif i[0] == 'level':
            max_width, max_height = int(i[1]), int(i[2])
        elif i[0] == 'bullet':
            UnusedBullet(int(i[1]), int(i[2]))
        elif i[0] == 'flag':
            new_flag = Flag(int(i[1]), int(i[2]))
        elif i[0] == 'enemy':
            xL, xR = i[1].split(':')
            Enemy(xL, xR, int(i[2]), int(i[4]))
    return new_player, new_flag, max_width, max_height


def update_levels(dict_levels):
    file = open('data/levels.txt', mode='w')
    column = 0
    file.seek(column)
    file.close()
    file_new = open('data/levels.txt', mode='w')
    for key, value in dict_levels.items():
        file_new.write(f'{key}:{value}' + '\n')
    file_new.close()


platform_image = {'platform_1_2_6': load_image('platform_level_1_2_6.png'),
                  'platform_3': load_image('platform_level_3.png'), 'platform_4': load_image('platform_level_4.png'),
                  'platform_5': load_image('platform_level_5.png'), 'border': load_image('border.png')}
levels = {1: 'level.csv', 2: 'level_2.csv', 3: 'level_3.csv',
          4: 'level_4.csv', 5: 'level_5.csv', 6: 'level_6.csv'}
level_fon = {1: load_image('fon_level_1_6.png'), 2: load_image('fon_level_2.png'), 3: load_image('fon_level_3_5.png'),
             4: load_image('fon_level_4.png'), 5: load_image('fon_level_3_5.png'), 6: load_image('fon_level_1_6.png')}
player_image = load_image('hero.png')
sneech_image = pygame.transform.scale(load_image('Sneech.png'), (86.4, 45.6))
flag_image = load_image('finish_flag.png')
bullet_image = load_image('bullet.png')
unused_bullet_image = load_image('bullet.png', (80, 80))
jumped_player_image = load_image('dencor-jump.png')
padlock_image = load_image('padlock.png')


class Platform(pygame.sprite.Sprite):
    def __init__(self, platform_type, pos_x, pos_y, group):
        super().__init__(platform_group if group == 'platform' else border_group, all_sprites)
        self.image = platform_image[platform_type]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Flag(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(flag_group, all_sprites)
        self.image = flag_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.x = pos_x
        self.x0 = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.mask = pygame.mask.from_surface(self.image)
        self.flip = False
        self.die = False
        self.bullets = 3

    def jump(self):
        self.image = jumped_player_image
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

    def twist(self, *args):
        if args:
            event = args[0]
            if event.key == pygame.K_LEFT:
                self.x0 -= 1
                if not self.flip:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.flip = True
            elif event.key == pygame.K_RIGHT:
                self.x0 += 1
                if self.flip:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.flip = False

    def update(self, *args, **kwargs):
        borders_collided = pygame.sprite.spritecollide(self, border_group, False)
        platforms_collided = pygame.sprite.spritecollide(self, platform_group, False)
        enemies_collided = pygame.sprite.spritecollide(self, enemy_group, False)
        if enemies_collided:
            self.die = True
        if not platforms_collided and not borders_collided and not jump or\
                any(map(lambda x: x.rect.y + 3 < self.y + self.rect.height, platforms_collided)) and not jump and\
                platforms_collided or any(map(lambda x: x.rect.y + 3 < self.y + self.rect.height, borders_collided))\
                and borders_collided and not platforms_collided and not jump:
            self.y += 3
            if self.y >= screen.get_rect().height:
                self.die = True
        self.rect = self.image.get_rect().move(self.x, self.y)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, flip):
        super().__init__(bullet_group, all_sprites)
        self.image = bullet_image
        self.x = pos_x
        self.x_max = 539
        self.x_min = -105
        self.y = pos_y
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.mask = pygame.mask.from_surface(self.image)
        self.flip = flip
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, *args, **kwargs):
        x = args[0] if args else 0
        enemies_collided = pygame.sprite.spritecollide(self, enemy_group, False)
        borders_collided = pygame.sprite.spritecollide(self, border_group, False)
        if borders_collided:
            self.kill()
        if not self.flip:
            self.x += 5 - x
            self.x_max -= x
        elif self.flip:
            self.image = pygame.transform.flip(self.image, True, False)
            self.x -= 5 + x
            self.x_min += x
        if self.x >= self.x_max or self.x <= self.x_min:
            self.kill()
        self.rect = self.image.get_rect().move(self.x, self.y)


class UnusedBullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(unused_bullet_group, all_sprites)
        self.image = unused_bullet_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.use = False

    def update(self, *args, **kwargs):
        player_collided = pygame.sprite.spritecollide(self, player_group, False)
        if player_collided and not self.use:
            player.bullets += 1
            self.kill()
            self.use = True


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_xL, pos_xR, pos_y, speed):
        super().__init__(enemy_group, all_sprites)
        self.borders = [int(pos_xL), int(pos_xR)]
        self.image = sneech_image
        self.x = int(pos_xR)
        self.y = int(pos_y)
        self.speed = int(speed)
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.mask = pygame.mask.from_surface(self.image)
        self.move_left = True

    def update(self, *args, **kwargs):
        bullets_collided = pygame.sprite.spritecollide(self, bullet_group, False)
        if bullets_collided:
            self.kill()
        x = args[0] if args else 0
        if self.x - self.speed > self.borders[0] and self.move_left:
            self.x -= self.speed + x
        elif self.x - self.speed <= self.borders[0] and self.move_left:
            self.image = pygame.transform.flip(self.image, True, False)
            self.move_left = False
        elif self.x + self.speed < self.borders[1] and not self.move_left:
            self.x += self.speed - x
        elif self.x + self.speed >= self.borders[1] and not self.move_left:
            self.image = pygame.transform.flip(self.image, True, False)
            self.move_left = True
        self.rect = self.image.get_rect().move(self.x, self.y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.event = None

    def check_collide(self):
        return lambda x: x.rect.x <= player.x + player.rect.width + self.dx and \
                         player.x + self.dx <= x.rect.x + x.rect.width and \
                         player.y <= x.rect.y + 3 < player.y + player.rect.height

    def apply(self, obj):
        if any(map(self.check_collide(), border_group)):
            return
        elif obj.__class__.__name__ == 'Bullet':
            obj.update(self.dx)
        elif obj.__class__.__name__ == 'Enemy':
            obj.update(self.dx)
            if player_motion != STOP:
                obj.borders[0] -= self.dx
                obj.borders[1] -= self.dx
            if obj.rect.x - obj.speed <= obj.borders[0] and obj.move_left and player_motion != STOP:
                obj.image = pygame.transform.flip(obj.image, True, False)
                obj.move_left = False
                obj.rect.x += obj.speed
            elif obj.rect.x - (obj.speed * 2) <= obj.borders[0] and obj.move_left and player_motion != STOP:
                obj.image = pygame.transform.flip(obj.image, True, False)
                obj.move_left = False
                obj.rect.x += obj.speed
            elif obj.rect.x + obj.speed >= obj.borders[1] and not obj.move_left and player_motion != STOP:
                obj.image = pygame.transform.flip(obj.image, True, False)
                obj.move_left = True
                obj.rect.x -= obj.speed
            elif obj.rect.x + (obj.speed * 2) >= obj.borders[1] and not obj.move_left and player_motion != STOP:
                obj.image = pygame.transform.flip(obj.image, True, False)
                obj.move_left = True
                obj.rect.x -= obj.speed
        else:
            obj.rect.x -= self.dx

    def update(self, *args):
        if args:
            self.event = args[0]
            if player_motion == RIGHT:
                self.dx = 2
            elif player_motion == LEFT:
                self.dx = -2
            elif player_motion == STOP:
                self.dx = 0
            player.twist(self.event)


font = pygame.font.Font(None, 36)


def draw_bullets_count(screen, text, x, y):
    text_surface = font.render(text, True, (143, 188, 143))
    screen.blit(text_surface, (x, y))


if __name__ == '__main__':
    running = True
    player, flag, level_x, level_y = generate_level(levels[level_number])
    all_sprites.empty()
    border_group.empty()
    flag_group.empty()
    player_group.empty()
    enemy_group.empty()
    platform_group.empty()
    start_screen()
    camera = Camera()
    camera.update()
    jump = False
    jump_count = 0
    jump_max = 18
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and player.bullets > 0:
                    Bullet(239 if not bullet_flip else 195, player.y + 21, bullet_flip)
                    player.bullets -= 1
                elif event.key == pygame.K_LEFT:
                    bullet_flip = True
                    player_motion = LEFT
                    camera.update(event)
                elif event.key == pygame.K_RIGHT:
                    bullet_flip = False
                    player_motion = RIGHT
                    camera.update(event)
                elif not jump and event.key == pygame.K_UP:
                    if pygame.sprite.spritecollideany(player, border_group) or\
                            pygame.sprite.spritecollideany(player, platform_group):
                        jump = True
                        player.jump()
                        jump_count = jump_max
                elif event.key == pygame.K_ESCAPE:
                    pause_screen()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_motion = STOP
                    camera.update(event)
        if jump:
            player.y -= jump_count
            if jump_count > 0:
                jump_count -= 1
            elif jump_count == 0:
                jump = False
                if not player.flip:
                    player.image = player_image
                elif player.flip:
                    player.image = pygame.transform.flip(player_image, True, False)
            elif pygame.sprite.spritecollide(player, border_group, False)[0].rect.y > player.y + player.rect.height + 3:
                jump = False
                if not player.flip:
                    player.image = player_image
                elif player.flip:
                    player.image = pygame.transform.flip(player_image, True, False)
                player.y = pygame.sprite.spritecollide(player, border_group, False)[0].rect.y - player.rect.width
            elif pygame.sprite.spritecollideany(player, platform_group):
                jump = False
                if not player.flip:
                    player.image = player_image
                elif player.flip:
                    player.image = pygame.transform.flip(player_image, True, False)
                player.y = pygame.sprite.spritecollide(player, platform_group, False)[0].rect.y - player.rect.width
        if player:
            if player.die:
                finish_screen()
                player_motion = STOP
                camera.dx = 0
            if pygame.sprite.spritecollide(player, flag_group, False) and not enemy_group:
                finish_screen(win=True)
                player_motion = STOP
                camera.dx = 0
        fon = pygame.transform.scale(level_fon[level_number], (width, height))
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)
        player_group.draw(screen)
        enemy_group.draw(screen)
        bullet_group.draw(screen)
        if player:
            for sprite in platform_group:
                camera.apply(sprite)
            for sprite in border_group:
                camera.apply(sprite)
            for sprite in enemy_group:
                camera.apply(sprite)
            for sprite in bullet_group:
                camera.apply(sprite)
            for sprite in unused_bullet_group:
                camera.apply(sprite)
            camera.apply(flag)
        draw_bullets_count(screen, f"Количество пуль: {player.bullets}", 10, 10)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
