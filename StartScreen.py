import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtWidgets import QInputDialog
from PyQt5 import QtCore

from TheGame import TheGame

import GlobalVariables


class StartScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.startGame = QPushButton(self)
        self.usernameLabel = QLabel(self)
        self.recordLabel = QLabel(self)
        self.gameRulesLabel = QLabel(self)

        self.lastName = GlobalVariables.lastName
        self.lastNumberOfVictoriesInARow = GlobalVariables.lastNumberOfVictoriesInARow

        self.initUI()

    def initUI(self):
        self.setGeometry(425, 125, 300, 500)
        self.setWindowTitle('Начало игры')

        with open('TheGameRules.txt', mode='r', encoding='utf8') as f:
            gameRules = f.read()

        self.startGame.move(90, 345)
        self.startGame.setText("Начать игру")
        self.startGame.clicked.connect(self.writeUsernameFunction)
        self.startGame.resize(300, 100)

        self.usernameLabel.move(5, -210)
        self.usernameLabel.resize(450, 450)
        self.usernameLabel.setText('')

        self.gameRulesLabel.move(2, 5)
        self.gameRulesLabel.resize(300, 300)
        self.gameRulesLabel.setText(gameRules)
        self.gameRulesLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.recordLabel.move(2, 274)
        self.recordLabel.resize(300, 50)
        self.recordLabel.setText(f'  Также мы предлагаем вам побить\n рекорд прошлых игроков: \n'
                    f'{self.lastName},   {self.lastNumberOfVictoriesInARow}')
        self.recordLabel.setAlignment(QtCore.Qt.AlignCenter)

    def writeUsernameFunction(self):
        try:
            self.usernameLabel.setText('Имя персонажа')
            username, ok_pressed = QInputDialog.getText(self, "Введите имя",
                                                        "Введите своё имя")
            if ok_pressed:
                self.startGame.hide()

                if len(username) > 11:
                    raise ValueError
                elif username != username.capitalize() or not username.isalpha():
                    raise TypeError
                else:
                    self.hide()
                    self.game = TheGame(username)
                    self.game.show()

        except ValueError:
            self.usernameLabel.setText('Имя слишком длинное!')
            self.startGame.show()
        except TypeError:
            self.usernameLabel.setText('Введите корректное имя!')
            self.startGame.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = StartScreen()
    widget.show()
    sys.exit(app.exec_())













































import pygame
import os
import sys
import random


class Border(pygame.sprite.Sprite):
    def __init__(self, location):

        if location == 1:
            super().__init__(upper_sprite)
        elif location == 2:
            super().__init__(downer_sprite)

        if location == 1:
            self.image = load_image('upper_borderline.png', -1)
        elif location == 2:
            self.image = load_image('downer_borderline.png', -1)

        self.rect = self.image.get_rect()

        if location == 1:
            self.rect.y = 0
        elif location == 2:
            self.rect.y = 450


class RedUFO(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(ufo_sprites)
        self.image = load_image('red_UFO.png', -1)
        self.rect = self.image.get_rect()

        self.rect.x = 20
        self.rect.y = 347
        self.moving_up = False
        self.moving_down = False

        self.can_run_up = True
        self.can_run_down = True

        self.vy = 0

    def update(self):
        if self.moving_up:
            self.vy = -5
            self.rect.y += self.vy

        if self.moving_down:
            self.vy = 5
            self.rect.y += self.vy

        self.can_run_up = True
        self.can_run_down = True
        if pygame.sprite.spritecollideany(self, upper_sprite):
            self.can_run_up = False
            self.moving_up = False

        if pygame.sprite.spritecollideany(self, downer_sprite):
            self.can_run_down = False
            self.moving_down = False


class BlueUFO(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(ufo_sprites)
        self.image = load_image('blue_UFO.png', -1)
        self.rect = self.image.get_rect()

        self.rect.x = 907
        self.rect.y = 200

        self.vy = 5

    def update(self):
        pass


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(ball_sprite)
        radius = 20
        self.x = 475
        self.y = 274

        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("orange"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(self.x, self.y, 2 * radius, 2 * radius)

        self.easy_speeds = [-10, -9, -8, -7, 10, 9, 8, 7]
        self.hard_speeds = [-11, -12, -13, -14, 11, 12, 13, 14]

        self.speeds = self.easy_speeds

        self.vx = random.choice(self.speeds)
        self.vy = random.choice(self.speeds)

    def update(self):

        if pygame.sprite.spritecollideany(self, upper_sprite)\
                or pygame.sprite.spritecollideany(self, downer_sprite):
            self.vy = -self.vy

        if pygame.sprite.spritecollideany(self, ufo_sprites):
            self.vx = -self.vx

        self.rect = self.rect.move(self.vx, self.vy)


# functions
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
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


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Cosmo Ball')
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)

    # sprite groups
    starting_screens_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    ufo_sprites = pygame.sprite.Group()
    ball_sprite = pygame.sprite.Group()
    upper_sprite = pygame.sprite.Group()
    downer_sprite = pygame.sprite.Group()

    # images
    background = load_image('background.png')

    upper_border = Border(1)
    downer_border = Border(2)
    red_ufo = RedUFO()
    blue_ufo = BlueUFO()
    ball = Ball()

    # sprites
    start_screen_sprite = pygame.sprite.Sprite()
    start_screen_sprite.image = load_image("start_screen.png")
    start_screen_sprite.rect = start_screen_sprite.image.get_rect()
    start_screen_sprite.rect.x = 0
    start_screen_sprite.rect.y = 0

    level_screen_sprite = pygame.sprite.Sprite()
    level_screen_sprite.image = load_image("level_screen.png")
    level_screen_sprite.rect = level_screen_sprite.image.get_rect()
    level_screen_sprite.rect.x = 0
    level_screen_sprite.rect.y = 0

    starting_screens_sprites.add(level_screen_sprite)
    starting_screens_sprites.add(start_screen_sprite)

    ufo_sprites.draw(screen)
    ball_sprite.draw(screen)

    # variables
    running = True
    fps = 30
    v = 20
    start_screen_moving = 0
    level_screen_moving = 0
    mode = 'start screen'
    untouchable = False
    clock = pygame.time.Clock()

    while running:
        screen.blit(background, (0, 0))

        # THE GAME
        if mode == 'the game screen':
            ufo_sprites.update()
            if level_screen_sprite.rect.x >= 1000:
                ball.speeds = ball.hard_speeds
            elif level_screen_sprite.rect.x <= -1000:
                ball.speeds = ball.easy_speeds
            ball_sprite.update()

        # events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (mode == 'start screen') and not untouchable:
                if pygame.mouse.get_pos()[0] <= 500:
                    start_screen_moving = -20
                else:
                    start_screen_moving = 20
                untouchable = True

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (mode == 'level screen') and not untouchable:
                if pygame.mouse.get_pos()[0] <= 500:
                    level_screen_moving = -20
                    ball.speeds = ball.easy_speeds
                else:
                    level_screen_moving = 20
                    ball.vx = random.choice(ball.hard_speeds)
                    ball.vy = random.choice(ball.hard_speeds) #у меня всё заработало!!!
                untouchable = True

            elif (event.type == pygame.KEYDOWN)\
                    and (mode == 'the game screen')\
                    and (event.key == pygame.K_UP)\
                    and red_ufo.can_run_up:
                red_ufo.moving_up = True
                red_ufo.moving_down = False

            elif (event.type == pygame.KEYDOWN)\
                    and (mode == 'the game screen')\
                    and (event.key == pygame.K_DOWN)\
                    and red_ufo.can_run_down:
                red_ufo.moving_down = True
                red_ufo.moving_up = False

        # update
        if (start_screen_sprite.rect.x == 1000 or start_screen_sprite.rect.x == -1000)\
                and (mode == 'start screen'):
            start_screen_moving = 0
            untouchable = False
            mode = 'level screen'

        if (level_screen_sprite.rect.x == 1000 or level_screen_sprite.rect.x == -1000)\
                and (mode == 'level screen'):
            level_screen_moving = 0
            untouchable = False
            mode = 'the game screen'

        upper_sprite.draw(screen)
        downer_sprite.draw(screen)
        ufo_sprites.draw(screen)
        ball_sprite.draw(screen)

        start_screen_sprite.rect.x += start_screen_moving
        level_screen_sprite.rect.x += level_screen_moving

        starting_screens_sprites.draw(screen)

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
