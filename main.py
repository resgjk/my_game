import pygame
import os
import sys
import time

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget

FPS = 60
clock = pygame.time.Clock()

size = WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode(size)
dvig = True


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


player_image = load_image('player1.png')


class Wid_ch(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/ch_pers_UI.ui', self)
        self.bg.buttonClicked.connect(self.ch_fnc)

    def ch_fnc(self, btn):
        global player_image
        global player
        global player_group
        if btn == self.p1:
            player_image = load_image('player1.png')
        elif btn == self.p2:
            player_image = load_image('player2.png')
        elif btn == self.p3:
            player_image = load_image('player3.png')
        elif btn == self.p4:
            player_image = load_image('player4.png')
        elif btn == self.p5:
            player_image = load_image('player5.png')
        elif btn == self.p6:
            player_image = load_image('player6.png')
        elif btn == self.p7:
            player_image = load_image('player7.png')
        elif btn == self.p8:
            player_image = load_image('player8.png')
        elif btn == self.p9:
            player_image = load_image('player9.png')
        player_group = pygame.sprite.Group()
        player = Player(70, 605)
        player.rect.x = player.pos_x
        player.rect.y = player.pos_y
        ex.pw.close()
        ex.show()


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/start_UI.ui', self)
        self.play_btn.clicked.connect(self.start_fnc)
        self.pers_btn.clicked.connect(self.pers_fnc)

    def pers_fnc(self):
        ex.close()
        self.pw = Wid_ch()
        self.pw.show()

    def start_fnc(self):
        ex.close()
        self.ch_lvl = Ch_lvl()
        self.ch_lvl.show()


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '!':
                Tile('prep', x, y)
            elif level[y][x] == '@':
                Tile('normal', x, y)
            elif level[y][x] == '?':
                Tile('vixod', x, y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.tile_type = tile_type
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        if tile_type == 'vixod':
            self.rect = self.image.get_rect().move(
                55 * pos_x + 550, 605 - 60)
        else:
            self.rect = self.image.get_rect().move(
                55 * pos_x + 550, 605 - (55 * pos_y))
        self.start_pos_x = 55 * pos_x + 550
        if tile_type == 'normal':
            self.floor = pos_y + 1


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.isJump = False
        self.jumpCount = 32
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def update(self):
        global dvig
        global ex
        if not pygame.sprite.groupcollide(player_group, exit_group, False, False,
                                          pygame.sprite.collide_mask):
            if not pygame.sprite.groupcollide(player_group, prep_group, False, False,
                                              pygame.sprite.collide_mask) and not pygame.sprite.groupcollide(
                player_group,
                normal_group,
                False, False,
                pygame.sprite.collide_mask) and not self.isJump:
                self.rect.x = 70
                self.rect.y = 605
            if not pygame.sprite.groupcollide(player_group, prep_group, False, False, pygame.sprite.collide_mask):
                if self.isJump:
                    if self.jumpCount >= -32:
                        if self.jumpCount < 0:
                            self.rect.y += self.jumpCount ** 2 * 0.01
                        else:
                            self.rect.y -= self.jumpCount ** 2 * 0.01
                        self.jumpCount -= 1
                        if pygame.sprite.groupcollide(player_group, normal_group, False, False,
                                                      pygame.sprite.collide_mask):
                            ex = pygame.sprite.groupcollide(player_group, normal_group, False, False,
                                                            pygame.sprite.collide_mask)
                            self.rect.y = 605 - (55 * ex[list(ex)[0]][0].floor) + 3
                            self.isJump = False
                            self.jumpCount = 32
                    else:
                        self.isJump = False
                        self.jumpCount = 32
                        self.rect.y = player.pos_y
            else:
                time.sleep(0.3)
                self.rect.x = 70
                self.rect.y = 605
                self.isJump = False
                self.jumpCount = 32
                for i in normal_group.sprites():
                    i.rect.x = i.start_pos_x
                for i in prep_group.sprites():
                    i.rect.x = i.start_pos_x
                for i in exit_group.sprites():
                    i.rect.x = i.start_pos_x
        else:
            if dvig == True:
                dvig = False
                self.msg = Win_Msg()
                self.msg.show()
                exit_group.sprites()[0].kill()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))[::-1]


class Ch_lvl(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/go_UI.ui', self)
        self.next.clicked.connect(self.next_fnc)
        self.back.clicked.connect(self.back_fnc)
        self.go.clicked.connect(self.go_fnc)

    def go_fnc(self):
        ex.ch_lvl.close()
        pygame.display.set_caption('CubeJumper')
        if self.sw.currentIndex() == 0:
            generate_level(load_level('map.txt'))
        elif self.sw.currentIndex() == 1:
            generate_level(load_level('map2.txt'))
        normal_group.add([i for i in tiles_group.sprites() if i.tile_type == 'normal'])
        prep_group.add([i for i in tiles_group.sprites() if i.tile_type == 'prep'])
        exit_group.add([i for i in tiles_group.sprites() if i.tile_type == 'vixod'])
        while True:
            screen.blit(fon_surf, fon_rect)
            if dvig:
                for i in prep_group.sprites():
                    i.rect.x -= 6
                for i in normal_group.sprites():
                    i.rect.x -= 6
                for i in exit_group.sprites():
                    i.rect.x -= 6
            player_group.draw(screen)
            prep_group.draw(screen)
            normal_group.draw(screen)
            exit_group.draw(screen)
            player.update()
            for event in pygame.event.get():
                if event.type != pygame.QUIT:
                    if not player.isJump:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            player.isJump = True
                else:
                    pygame.quit()
            player.update()
            clock.tick(60)
            pygame.display.flip()

    def next_fnc(self):
        try:
            self.sw.setCurrentIndex(self.sw.currentIndex() + 1)
        except Exception:
            pass

    def back_fnc(self):
        try:
            self.sw.setCurrentIndex(self.sw.currentIndex() - 1)
        except Exception:
            pass


class Win_Msg(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/msg_UI.ui', self)
        self.back.clicked.connect(self.back_fnc)

    def back_fnc(self):
        global dvig
        global ex
        dvig = True
        ex = MyWidget()
        ex.show()
        self.close()


fon_surf = pygame.image.load('data/fonner.png')
fon_rect = fon_surf.get_rect()
screen.blit(fon_surf, fon_rect)

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
prep_group = pygame.sprite.Group()
normal_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

player = Player(70, 605)
player.rect.x = player.pos_x
player.rect.y = player.pos_y

tile_images = {
    'prep': load_image('triangle.png'),
    'normal': load_image('box.png'),
    'vixod': load_image('exit.png')
}


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
