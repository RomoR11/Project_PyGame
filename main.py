import pygame
import sys
import os
import csv


pygame.init()


width, height = 640, 480
screen = pygame.display.set_mode((width, height))
FPS = 50
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ['Чтобы начать игру нажмите любую кнопку']

    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
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
        data = [[row[0], row[1], row[2]] for row in r]
    new_player, max_width, max_height = None, 0, 0
    for i in data:
        if i[0] == 'player':
            new_player = Player(int(i[1]), int(i[2]))
        elif i[0] == 'platform':
            Platform('platform', int(i[1]), int(i[2]))
        elif i[0] == 'level':
            max_width, max_height = int(i[1]), int(i[2])
    return new_player, max_width, max_height


platform_image = {'platform': load_image('platform_py.png')}
player_image = pygame.transform.scale(load_image('hero.png'), (80, 80))


class Platform(pygame.sprite.Sprite):
    def __init__(self, platform_type, pos_x, pos_y):
        super().__init__(platform_group, all_sprites)
        self.image = platform_image[platform_type]
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
        if args:
            event, w, h = args[0], args[1], args[2]
            if event.key == pygame.K_LEFT and self.x - 1 >= 0:
                self.x -= 1
                self.x0 -= 1
                self.twist(event)
            elif event.key == pygame.K_RIGHT and self.x + 1 <= level_x:
                self.x += 1
                self.x0 += 1
                self.twist(event)
            self.rect = self.image.get_rect().move(self.x, self.y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.event = None

    def apply(self, obj):
        if player.x0 <= 100 and self.event:
            player.update(self.event, level_x, level_y)
        else:
            obj.rect.x -= self.dx

    def update(self, *args):
        if args:
            self.event = args[0]
            self.dx = -1 if self.event.key == pygame.K_LEFT else 1
            player.twist(event)


player, level_x, level_y = generate_level('level.csv')

if __name__ == '__main__':
    running = True
    start_screen()
    camera = Camera()
    camera.update()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    camera.update(event)
                    for sprite in platform_group:
                        camera.apply(sprite)
        screen.fill('black')
        all_sprites.draw(screen)
        player_group.draw(screen)
        all_sprites.update()
        pygame.display.flip()
    pygame.quit()
