import pygame
import os
import sys

FPS = 60
clock = pygame.time.Clock()

size = WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = f'data/{name}'
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


player_image = load_image('player.png')


def generate_level(level):
    print(level[0])
    for x in range(len(level[0])):
        if level[0][x] == '!':
            Tile('prep', x, 605)
        elif level[0][x] == '@':
            Tile('normal', x, 605)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, prep_group, normal_group)
        self.tile_type = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            55 * pos_x + 70, pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.isJump = False
        self.jumpCount = 9
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect()

    def update(self):
        if self.isJump:
            if self.jumpCount >= -9:
                if self.jumpCount < 0:
                    self.rect.y += (self.jumpCount ** 2) / 2
                else:
                    self.rect.y -= (self.jumpCount ** 2) / 2
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 9
                self.rect.x = player.pos_x
                self.rect.y = player.pos_y

    def check(self):
        pass


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


fon_surf = pygame.image.load('data/fonner.png')
fon_rect = fon_surf.get_rect()
screen.blit(fon_surf, fon_rect)

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
prep_group = pygame.sprite.Group()
normal_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()

player = Player(70, 605)
player.rect.x = player.pos_x
player.rect.y = player.pos_y

tile_images = {
    'prep': load_image('triangle.png'),
    'normal': load_image('box.png')
}
if __name__ == '__main__':
    generate_level(load_level('map.txt'))
    while True:
        screen.blit(fon_surf, fon_rect)
        player_group.draw(screen)
        prep_group.draw(screen)
        normal_group.draw(screen)
        tiles_group.draw(screen)
        player.update()
        for event in pygame.event.get():
            if event.type != pygame.QUIT:
                if player.isJump == False:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            player.isJump = True
            else:
                pygame.quit()
        player.update()
        clock.tick(60)
        pygame.display.flip()
