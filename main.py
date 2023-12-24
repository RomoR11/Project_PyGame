import pygame
import sys
import os


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


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


platform_image = {'platform': pygame.transform.scale(load_image('platform_py.png'), (80, 80)),
                  'empty': pygame.transform.scale(load_image('empty.png'), (80, 80))}
player_image = pygame.transform.scale(load_image('hero.png'), (80, 80))
pl_height = pl_width = 80


class Platform(pygame.sprite.Sprite):
    def __init__(self, platform_type, pos_x, pos_y):
        super().__init__(platform_group, all_sprites)
        self.image = platform_image[platform_type]
        self.rect = self.image.get_rect().move(
            pl_width * pos_x, pl_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            pl_width * pos_x + 15, pl_height * pos_y + 5)
        self.x = pos_x
        self.y = pos_y
        self.flip = False

    def update(self, *args, **kwargs):
        if args:
            event, level = args[0], args[1]
            if event.key == pygame.K_LEFT and self.x - 1 >= 0:
                self.x -= 1
                if not self.flip:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.flip = True
            elif event.key == pygame.K_RIGHT and len(level[self.y]) > self.x + 1:
                self.x += 1
                if self.flip:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.flip = False
            self.rect = self.image.get_rect().move(pl_width * self.x + 15, pl_height * self.y + 5)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Platform('empty', x, y)
            elif level[y][x] == '#':
                Platform('platform', x, y)
            elif level[y][x] == '$':
                Platform('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y, level


player, level_x, level_y, level = generate_level(load_level('level.txt'))

if __name__ == '__main__':
    running = True
    start_screen()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    all_sprites.update(event, level)
        screen.fill('black')
        all_sprites.draw(screen)
        player_group.draw(screen)
        all_sprites.update()
        pygame.display.flip()
    pygame.quit()
