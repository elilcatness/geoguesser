import pygame as pg


class Button(pg.sprite.Sprite):
    def __init__(self, text: str, pos: tuple, size: tuple, group: pg.sprite.AbstractGroup):
        super(Button, self).__init__(group)
        self.x, self.y = pos
        self.width, self.height = size
        self.text = text
        self.color = 'white'
        self.image = None
        pg.font.init()
        self.draw()

        self.active = True

    def activate(self):
        self.active = True

    def disable(self):
        self.active = False

    def change_text(self, text: str):
        self.text = text
        self.draw()

    def change_color(self, color: str):
        self.color = color
        self.draw()

    def get_text(self) -> str:
        return self.text

    def draw(self):
        screen = pg.Surface((self.width, self.height))
        screen.fill(pg.Color('#3A1D1D'))
        self.rect = pg.Rect((self.x, self.y, self.width, self.height))
        self.image = screen
        font = pg.font.SysFont('Consolas', 24)
        text = font.render(self.text, True, pg.Color(self.color))
        self.image.blit(text, (self.width // 2 - text.get_width() // 2,
                               self.height // 2 - text.get_height() // 2))

    def handle_click(self, pos: tuple):
        x1, y1 = pos
        if ((self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height)
                and self.active):
            self.active = False
            return True
        return False

    def hide(self):
        self.rect.x = -2000
        self.rect.y = -2000

    def show(self):
        self.rect.x = self.x
        self.rect.y = self.y
