import os
from settings import *
from viewer import img_show
from figures import Triangle, Point
import random
from math import fabs
from itertools import cycle


class Bitmap:
    """ Класс реализующий методы работы с массивом пикселей - битмапом """
    def __init__(self):
        self.bitmap = [[BLACK_PIXEL] * IMG_SIZE for i in range(0, IMG_SIZE)]
        self.filename = "bitmap.pgm"

    def draw_line(self, p1: Point, p2: Point):
        """ Нарисовать линию в битмапе по алгоритму Ву
            учитывая что битмап это список точек """
        # a = p1, b = p2
        # x1, x2 = p1.x, p2.x
        # y1, y2 = p1.y, p2.y
        # if p1.x > p2.x:
        #     x1, x2 = x2, x1
        #     y1, y2 = y2, y1
        # x_range = x2 - x1
        # k = (y2 - y1)/(x2 - x1)  # угловой коэф. прямой
        #
        # for px in range():
        #     self.bitmap(x)

        # print(p1.px_number, p2.px_number)

        # print("k", k)

    def add_noize(self, prob:float):
        """ Добавить шум к битмапу с вероятностью prob зашумления каждого пикселя """
        for y in range(0, IMG_SIZE):
            for x in range(0, IMG_SIZE):
                noize = random.uniform(0, 1) <= prob
                if noize:
                    self.bitmap[y][x] = random.randint(0, IMG_MODE)

    def save(self, filename=None):
        """ Сохарнить битмап в pgm файл """
        if filename: self.filename = filename
        str_bitmap = "P2\n%d %d\n%d\n" % (IMG_SIZE, IMG_SIZE, IMG_MODE)
        for y in range(0, IMG_SIZE):
            str_bitmap += " ".join([str(self.bitmap[y][x]) for x in range(0, IMG_SIZE)]) + "\n"
        file = open(os.path.join(IMG_ROOT, self.filename), "w")
        file.write(str_bitmap)
        file.close()

    def show(self):
        img_show(self.filename)

triangle = Triangle()
bitmap = Bitmap()

# bitmap.draw_line(triangle.points[0], triangle.points[1])

bitmap.add_noize(0.001)
bitmap.save()
bitmap.show()

