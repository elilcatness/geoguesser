import pygame as pg
from PIL import Image

from city_parser import parse_cities
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

    def update(self, *args, **kwargs):
        if self.move_side == 'left' and self.rect.x >= 0:
            self.rect.x -= self.velocity
            if self.rect.x <= 0:
                self.move_side = 'idle'
        elif self.move_side == 'right' and self.rect.x <= -self.velocity:
            if self.rect.x >= -self.velocity:
                self.move_side = 'idle'
            self.rect.x += self.velocity


def main():
    cities = parse_cities()
    if not cities:
        return 'Не удалось загрузить города (проверьте соединение с интернетом)'
    img = get_image_of_city(cities[0], 'sat')
    if isinstance(img, str):
        return img

    pg.init()
    img = pg.image.load(img)
    screen = pg.display.set_mode(img.get_size())
    pg.display.set_caption('GeoGuesser by elilcat v1.0')
    current_slide = Slide(cities[0], img, screen)
    prev_slide = None
    current_slide.show()
    while pg.event.wait().type != pg.QUIT:
        pass
    pg.quit()
    clock = pg.time.Clock()
    fps = 60
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    #         elif ((event.type == pg.KEYDOWN and (event.key == pg.K_RIGHT or event.key == pg.K_d))
    #               or (event.type == pg.MOUSEBUTTONDOWN and event.button == 4)):
    #             if not current_slide.is_moving():
    #                 prev_slide = current_slide
    #                 current_slide = slides[(slides.index(current_slide) + 1) % len(slides)]
    #                 current_slide.move('left')
    #         elif ((event.type == pg.KEYDOWN and (event.key == pg.K_LEFT or event.key == pg.K_a))
    #               or (event.type == pg.MOUSEBUTTONDOWN and event.button == 1)):
    #             if not current_slide.is_moving():
    #                 prev_slide = current_slide
    #                 current_slide = slides[(slides.index(current_slide) - 1) % len(slides)]
    #                 current_slide.move('right')
        for slide in (prev_slide, current_slide):
            slide.update()
            screen.blit(slide.get_image(), slide.get_pos())
        clock.tick(fps)
        pg.display.flip()
    pg.quit()


if __name__ == '__main__':
    callback = main()
    if callback:
        print(callback)