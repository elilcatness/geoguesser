import os

import pygame as pg

from exceptions import ImageNotFoundError


class Loader:
    @staticmethod
    def load_image(filename: str) -> pg.Surface:
        try:
            img = pg.image.load(os.path.join('data', 'img', filename))
        except FileNotFoundError:
            raise ImageNotFoundError('Не удалось загрузить файл изображения %s' % filename)
        return img
