from random import shuffle
from dotenv import load_dotenv

import pygame as pg

from button import Button
from city_parser import parse_cities
from loader import Loader
from static_image import get_image_of_city


class Slide(pg.sprite.Sprite):
    def __init__(self, name: str, img: pg.Surface, screen: pg.Surface):
        super(Slide, self).__init__()
        self.name = name
        self.image = img
        self.rect = self.image.get_rect()
        self.screen_width = screen.get_width()
        self.rect.x = self.screen_width
        self.velocity = 10
        self.move_side = 'idle'

    def get_name(self) -> str:
        return self.name

    def get_image(self) -> pg.Surface:
        return self.image

    def get_pos(self) -> tuple:
        return self.rect.x, self.rect.y

    def move(self, state: str):
        self.move_side = state
        self.rect.x = self.screen_width if self.move_side == 'left' else -self.screen_width

    def show(self):
        self.rect.x = 0

    def is_moving(self) -> bool:
        return self.move_side in ('right', 'left')

    def guess(self, answer: str):
        return self.name == answer

    def update(self, *args, **kwargs):
        if self.move_side == 'left' and self.rect.x >= 0:
            self.rect.x -= self.velocity
            if self.rect.x <= 0:
                self.move_side = 'idle'
        elif self.move_side == 'right' and self.rect.x <= -self.velocity:
            if self.rect.x >= -self.velocity:
                self.move_side = 'idle'
            self.rect.x += self.velocity


def finish(score: int, total: int, screen: pg.Surface, font: pg.font.Font, background: pg.Surface):
    screen.fill('black')
    screen.blit(background, (0, 0))
    screen.blit(background, (0, 300))
    first_text = font.render('Вы набрали %d очков из %d' % (score, total), True, pg.Color('red'))
    second_text = font.render('Чтобы начать заново,', True, pg.Color('red'))
    third_text = font.render('нажмите пробел', True, pg.Color('red'))
    width, height = screen.get_size()
    screen.blit(first_text, (width // 2 - first_text.get_width() // 2,
                             height // 2 - first_text.get_height() // 2 -
                             second_text.get_height()))
    screen.blit(second_text, (width // 2 - second_text.get_width() // 2,
                              height // 2 - second_text.get_height() // 2 +
                              second_text.get_height()))
    screen.blit(third_text, (width // 2 - third_text.get_width() // 2,
                             height // 2 - second_text.get_height() // 2 +
                             second_text.get_height() * 2))
    pg.display.flip()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                return True


def main():
    cities = parse_cities()
    if not cities:
        return 'Не удалось загрузить города (проверьте соединение с интернетом)'
    choices = cities[10:]
    cities = cities[:10]
    img = get_image_of_city(cities[0], 'sat')
    if isinstance(img, str):
        return img

    pg.init()
    img = pg.image.load(img)
    width, height = img.get_width(), int(img.get_height() * 1.6)
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption('GeoGuesser by elilcat v1.0')
    current_slide = Slide(cities[0], img, screen)
    prev_slide = current_slide
    img_height = img.get_height()
    btn_positions = [(int(width * 0.025), int(img_height * 1.2)), (int(width * 0.515), int(img_height) * 1.2),
                     (int(width * 0.025), int(img_height * 1.4)), (int(width * 0.515), int(img_height) * 1.4)]
    buttons = pg.sprite.Group()
    current_choices = choices[:3] + [current_slide.get_name()]
    shuffle(current_choices)
    for i in range(4):
        if current_choices[0] in choices:
            choices.pop(choices.index(current_choices[0]))
        Button(current_choices.pop(0), btn_positions[i], (275, 40), buttons)
    background = Loader.load_image('background.jpg')
    font = pg.font.SysFont('Consolas', 36)
    correct_text = font.render('Верный ответ, +1 балл', True, pg.Color('green'))
    correct_text_pos = (width // 2 - correct_text.get_width() // 2, int(height * 0.05))
    miss_text = font.render('Неверный ответ', True, pg.Color('red'))
    miss_text_pos = (width // 2 - miss_text.get_width() // 2, int(height * 0.05))
    current_slide.show()
    clock = pg.time.Clock()
    fps = 60
    running = True
    score = 0
    clicked, guessed = False, False
    while running:
        screen.fill('black')
        screen.blit(background, (0, img_height))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.handle_click(event.pos):
                        clicked = True
                        if current_slide.guess(btn.get_text()):
                            guessed = True
                            score += 1
                        else:
                            guessed = False
                        correct_btn = list(filter(lambda x: current_slide.guess(x.get_text()),
                                                  buttons))[0]
                        correct_btn.change_color('green')
                        correct_btn.disable()
                        miss_btns = list(filter(lambda x: not current_slide.guess(x.get_text()),
                                                buttons))
                        for mis_btn in miss_btns:
                            mis_btn.change_color('red')
                            mis_btn.disable()
                        break
            elif (event.type == pg.KEYDOWN and event.key == pg.K_SPACE
                  and clicked and not current_slide.is_moving()):
                clicked = False
                prev_slide = current_slide
                idx = cities.index(prev_slide.get_name()) + 1
                try:
                    img = get_image_of_city(cities[idx], 'sat')
                except IndexError:
                    if not finish(score, len(cities), screen, font, background):
                        return
                    main()
                if isinstance(img, str):
                    return img
                current_slide = Slide(cities[idx], pg.image.load(img), screen)
                current_slide.move('left')
                current_choices = choices[:3] + [current_slide.get_name()]
                shuffle(current_choices)
                for btn in buttons:
                    if current_choices[0] in choices:
                        choices.pop(choices.index(current_choices[0]))
                    btn.change_color('white')
                    btn.change_text(current_choices.pop(0))
                    btn.activate()
        for slide in (prev_slide, current_slide):
            slide.update()
            screen.blit(slide.get_image(), slide.get_pos())
        if clicked and guessed:
            screen.blit(correct_text, correct_text_pos)
        elif clicked and not guessed:
            screen.blit(miss_text, miss_text_pos)
        buttons.update()
        buttons.draw(screen)
        clock.tick(fps)
        pg.display.flip()
    pg.quit()


if __name__ == '__main__':
    load_dotenv()
    callback = main()
    if callback:
        print(callback)
