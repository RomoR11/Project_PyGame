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
STOP, LEFT, RIGHT, JUMP = 0, 1, 2, 3
player_motion = STOP


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    title_text = 'Просто платформер'
    screen.fill('DarkSeaGreen')
    font_title = pygame.font.Font('data/SAIBA-45.otf', 35)
    string_rendered = font_title.render(title_text, 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 30
    intro_rect.x = 110
    screen.blit(string_rendered, intro_rect)
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
                    return
                elif exit_button.x <= event.pos[0] <= exit_button.x + exit_button.width and\
                        exit_button.y <= event.pos[1] <= exit_button.y + exit_button.height:
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


def finish_screen():
    title_text = 'Поражение'
    screen.fill('DarkSeaGreen')
    font_title = pygame.font.Font('data/SAIBA-45.otf', 35)
    string_rendered = font_title.render(title_text, 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 30
    intro_rect.x = 190
    screen.blit(string_rendered, intro_rect)
    return_game_button = pygame.draw.rect(screen, 'white', pygame.Rect(210, 170, 200, 80), 3, 10)
    pygame.draw.rect(screen, 'DarkMagenta', pygame.Rect(213, 173, 194, 74), 0, 10)
    return_button = pygame.draw.rect(screen, 'white', pygame.Rect(210, 280, 200, 80), 3, 10)
    pygame.draw.rect(screen, 'DarkMagenta', pygame.Rect(213, 283, 194, 74), 0, 10)
    exit_button = pygame.draw.rect(screen, 'white', pygame.Rect(210, 390, 200, 80), 3, 10)
    pygame.draw.rect(screen, 'DarkMagenta', pygame.Rect(213, 393, 194, 74), 0, 10)
    font_start_game = pygame.font.Font(None, 35)
    string_rendered = font_start_game.render('Играть заново', 1, 'black')
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
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_game_button.x <= event.pos[0] <= return_game_button.x + return_game_button.width and \
                        return_game_button.y <= event.pos[1] <= return_game_button.y + return_game_button.height:
                    return
                elif exit_button.x <= event.pos[0] <= exit_button.x + exit_button.width and \
                        exit_button.y <= event.pos[1] <= exit_button.y + exit_button.height:
                    terminate()
                elif return_button.x <= event.pos[0] <= return_button.x + return_button.width and \
                        return_button.y <= event.pos[1] <= return_button.y + return_button.height:
                    start_screen()
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
            Platform('platform', int(i[1]), int(i[2]), i[3])
        elif i[0] == 'level':
            max_width, max_height = int(i[1]), int(i[2])
        elif i[0] == 'flag':
            new_flag = Flag(int(i[1]), int(i[2]))
        elif i[0] == 'enemy':
            xL, xR = i[1].split(':')
            Enemy(xL, xR, int(i[2]), int(i[4]))
    return new_player, new_flag, max_width, max_height


platform_image = {'platform': load_image('platform_py.png')}
player_image = pygame.transform.scale(load_image('hero.png'), (80, 80))
flag_image = load_image('finish_flag.png')


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
        platforms_collided = pygame.sprite.spritecollide(self, platform_group, False)
        borders_collided = pygame.sprite.spritecollide(self, border_group, False)
        if not platforms_collided and not borders_collided and not jump or\
                any(map(lambda x: x.rect.y + 2 < self.y + self.rect.height, platforms_collided)) and not jump and\
                platforms_collided or any(map(lambda x: x.rect.y + 2 < self.y + self.rect.height, borders_collided))\
                and borders_collided and not platforms_collided and not jump:
            self.y += 2
            if self.y >= screen.get_rect().height:
                self.die = True
        self.rect = self.image.get_rect().move(self.x, self.y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_xL, pos_xR, pos_y, speed):
        super().__init__(enemy_group, all_sprites)
        self.image = pygame.transform.flip(player_image, True, False)
        self.borders = [int(pos_xL), int(pos_xR)]
        self.x = int(pos_xR)
        self.y = int(pos_y)
        self.speed = int(speed)
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.mask = pygame.mask.from_surface(self.image)
        self.move_left = True

    def update(self, *args, **kwargs):
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
                         player.x + self.dx <= x.rect.x + x.rect.width

    def apply(self, obj):
        if any(map(self.check_collide(), border_group)) and \
                any(map(lambda x: player.y <= x.rect.y + 2 < player.y + player.rect.height, border_group)):
            return
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


player, flag, level_x, level_y = generate_level('level.csv')

if __name__ == '__main__':
    running = True
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
                if event.key == pygame.K_LEFT:
                    player_motion = LEFT
                    camera.update(event)
                elif event.key == pygame.K_RIGHT:
                    player_motion = RIGHT
                    camera.update(event)
                elif not jump and event.key == pygame.K_UP:
                    if pygame.sprite.spritecollideany(player, border_group) or\
                            pygame.sprite.spritecollideany(player, platform_group):
                        jump = True
                        jump_count = jump_max
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_motion = STOP
                    camera.update(event)
        if jump:
            player.y -= jump_count
            if jump_count > -jump_max:
                jump_count -= 1
            elif pygame.sprite.spritecollideany(player, border_group):
                jump = False
                player.y = pygame.sprite.spritecollide(player, border_group, False)[0].rect.y - player.rect.width
            elif pygame.sprite.spritecollideany(player, platform_group):
                jump = False
                player.y = pygame.sprite.spritecollide(player, platform_group, False)[0].rect.y - player.rect.width
        if player.die:
            finish_screen()
            player_motion = STOP
            player, flag, level_x, level_y = generate_level('level.csv')
        screen.fill('black')
        all_sprites.draw(screen)
        player_group.draw(screen)
        enemy_group.draw(screen)
        for sprite in platform_group:
            camera.apply(sprite)
        for sprite in border_group:
            camera.apply(sprite)
        for sprite in enemy_group:
            camera.apply(sprite)
        camera.apply(flag)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
