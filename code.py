# -*- coding:utf8 -*-
from settings import *
from viewer import img_show
from figures import Triangle, Point
import random
from math import floor, fabs, ceil


class Bitmap:
    """ Класс реализующий методы работы с массивом пикселей - битмапом """
    def __init__(self):
        self.bitmap = [[BLACK_PIXEL] * IMG_SIZE for i in range(0, IMG_SIZE)]
        self.filename = "bitmap.pgm"

    class Line:
        """ Реализует все необходимые для рисования параметры отрезка """
        def __init__(self, p1: Point, p2: Point):
            reverse_points = p1.x > p2.x  # какая точка левее
            if reverse_points:  # рисуем слева на право, для этого если нужно меняем точки местами
                p1, p2 = p2, p1
            # если по оси y рост быстрее чем по х то нужно в качестве основной оси использовать у
            # иначе линия будет прирывистой
            self.change_axis = fabs(p1.y - p2.y) > fabs(p1.x - p2.x)  # рост по y больше чем по х

            self.x1, self.x2, self.y1, self.y2 = p1.x, p2.x, p1.y, p2.y  # векторыне координаты точек (дробные)
            self.dx = (self.x2 - self.x1)      # дельта х
            self.dy = fabs(self.y2 - self.y1)  # дельта у
            # self.k = self.dy / self.dx         # угловой коэф. прямой

            self.x_start, self.y_start = floor(self.x1), floor(self.y1)  # координаты точек в битмапе (растровые)
            self.x_end, self.y_end = floor(self.x2), floor(self.y2)

    def draw_line(self, p1: Point, p2: Point):
        """ Нарисовать линию в битмапе по алгоритму Ву
            Рисовать будем слева на право по оси с наибольшей скоростью роста
            (иначе линия будет прирывистой)

            Ещё один нюанс. Если проекция отрезка на ось x меньше проекции на ось y
            или начало и конец отрезка переставлены местами, то алгоритм не будет работать.
            Чтобы этого не случилось, нужно проверять направление вектора и его наклон,
            а потом по необходимости менять местами координаты отрезка, поворачивать оси,
            и, в конечном итоге, сводить всё к двум случаям.

            Для оптимизации расчётов, применяют трюк с умножением всех дробных переменных на dx = (x1 — x0).
            Тогда на каждом шаге ошибка будет изменяться на dy = (y1 — y0) вместо углового коэффициента
            и на dx вместо единицы. *Расчеты с угловым коэф. иногда приводили к "перескакиванию" через 1 пиксель.
            Источник: www.habrahabr.ru/post/185086/
        """
        line = self.Line(p1, p2)  # координаты точек упорядоченные согласно условиям метода
        # Если рост y больше чем рост x то меняем оси
        if line.change_axis:
            x_step = 1 if line.x_start < line.x_end else -1
            y_step = 1 if line.y_start < line.y_end else -1
            x = x2 = line.x_start
            gradient = line.dx/line.dy
            diff = line.dy/2

            for y in range(line.y_start, line.y_end + y_step, y_step):
                color2 = round(WHITE_PIXEL * (x2 % 1))
                color1 = 255 - color2
                self.bitmap[y][ceil(x2)] = color2
                self.bitmap[y][floor(x2)] = color1

                # self.bitmap[y][x] = WHITE_PIXEL
                x2 += gradient * x_step
                diff -= line.dx
                if diff < 0:
                    x += x_step
                    diff += line.dy

        # Рост x больше чем рост по y
        else:
            y_step = 1 if line.y_start < line.y_end else -1
            gradient = line.dy/line.dx
            y = y2 = line.y_start
            diff = line.dx/2
            for x in range(line.x_start, line.x_end + 1):
                color2 = round(WHITE_PIXEL * (y2 % 1))
                color1 = 255 - color2
                self.bitmap[ceil(y2)][x] = color2
                self.bitmap[floor(y2)][x] = color1
                y2 += gradient * y_step
                diff -= line.dy
                if diff < 0:
                    y += y_step
                    diff += line.dx

    def add_noize(self, prob:float):
        """ Добавить шум к битмапу с вероятностью prob зашумления каждого пикселя """
        for y in range(0, IMG_SIZE):
            for x in range(0, IMG_SIZE):
                noize = random.uniform(0, 1) <= prob
                if noize:
                    self.bitmap[y][x] = random.randint(0, IMG_MODE)

    def filter(self):
        b = [[BLACK_PIXEL] * IMG_SIZE for i in range(0, IMG_SIZE)]
        for y in range(IMG_SIZE-2):
            for x in range(IMG_SIZE-2):
                pair_intensity = 255 - self.bitmap[y][x]
                # print(x, y, pair_intensity)
                if self.bitmap[y][x+1] == pair_intensity:
                    b[y][x], b[y][x+1] = self.bitmap[y][x], self.bitmap[y][x+1]
                    print(pair_intensity, self.bitmap[y][x+1])
                elif self.bitmap[y+1][x] == pair_intensity:
                    b[y][x], b[y+1][x] = self.bitmap[y][x], self.bitmap[y+1][x]

        self.bitmap = b[:]

        return

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
bitmap.draw_line(triangle.p1, triangle.p2)
bitmap.draw_line(triangle.p2, triangle.p3)
bitmap.draw_line(triangle.p3, triangle.p1)
# p1 = Point(x=10, y=3)
# p2 = Point(x=2, y=8)
# p3 = Point(x=13, y=13)
# bitmap.draw_line(p1, p2)
# bitmap.draw_line(p2, p3)
# bitmap.draw_line(p3, p1)
bitmap.save()
bitmap.add_noize(0.6)
bitmap.save("bitmap2.pgm")
bitmap.filter()
bitmap.save("bitmap3.pgm")
# bitmap.show()

