import pygame
import os
import sys

FPS = 60
clock = pygame.time.Clock()

size = WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode(size)
fon_surf = pygame.image.load('data/fonner.png')
fon_rect = fon_surf.get_rect()
screen.blit(fon_surf, fon_rect)

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
prep_group = pygame.sprite.Group()
normal_group = pygame.sprite.Group()


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


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.isJump = False
        self.jumpCount = 5
        super().__init__(player_group, all_sprites)
        self.image = load_image('player.png')
        self.rect = self.image.get_rect()

    def update(self):
        if self.jumpCount >= -7:
            if self.jumpCount < 0:
                self.rect.y += (self.jumpCount ** 2) / 2
            else:
                self.rect.y -= (self.jumpCount ** 2) / 2
            self.jumpCount -= 1
        else:
            self.isJump = False
            self.jumpCount = 7
            self.rect.x = player.pos_x
            self.rect.y = player.pos_y

    def check(self):
        pass


player = Player(70, 605)
player.rect.x = player.pos_x
player.rect.y = player.pos_y

if __name__ == '__main__':
    while True:
        screen.blit(fon_surf, fon_rect)
        player_group.draw(screen)
        for event in pygame.event.get():
            if event.type != pygame.QUIT:
                pass
                if not player.isJump:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        player.isJump = True
                else:
                    player.update()
            else:
                pygame.quit()
        clock.tick(FPS)
        pygame.display.flip()
