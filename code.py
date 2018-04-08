import os
from settings import *
from viewer import img_show
from figures import Triangle, Point
import random
from math import ceil, floor, fabs
from itertools import cycle




# class RasterLine:
#
#     def __init__(self, p1: Point, p2: Point):
#         if p1.x > p2.x:
#             # Изменение порядка точек, чтобы отрезок начинался слева, кончался справа
#             self.x1, self.x2, self.y1, self.y2 = round(p2.x), round(p1.x), round(p2.y), round(p1.y)
#         else:
#             self.x1, self.x2, self.y1, self.y2 = round(p1.x), round(p2.x), round(p1.y), round(p2.y)


class Bitmap:
    """ Класс реализующий методы работы с массивом пикселей - битмапом """
    def __init__(self):
        self.bitmap = [[BLACK_PIXEL] * IMG_SIZE for i in range(0, IMG_SIZE)]
        self.filename = "bitmap.pgm"

    class Line:

        def __init__(self, p1: Point, p2: Point):
            # print("x1=", p1.x, "y1=", p1.y)
            # print("x2=", p2.x, "y2=", p2.y)
            reverse_points = p1.x > p2.x  # какая точка левее
            if reverse_points:  # рисуем слева на право, для этого если нужно меняем точки местами
                p1, p2 = p2, p1
            # если по оси y рост быстрее чем по х то нужно в качестве основной оси использовать у
            # иначе линия будет прирывистой
            self.change_axis = fabs(p1.y - p2.y) > fabs(p1.x - p2.x)  # рост по y больше чем по х

            self.x1, self.x2, self.y1, self.y2 = p1.x, p2.x, p1.y, p2.y  # векторыне координаты точек (дробные)
            self.dx = (self.x2 - self.x1)
            self.dy = fabs(self.y2 - self.y1)
            self.k = self.dy / self.dx  # угловой коэф. прямой

            self.x_start, self.y_start = floor(self.x1), floor(self.y1)  # координаты точек в битмапе (растровые)
            self.x_end, self.y_end = floor(self.x2), floor(self.y2)
            print(self.x_start, self.y_start)
            print(self.x_end, self.y_end)

    def draw_line(self, p1: Point, p2: Point):
        """ Нарисовать линию в битмапе по алгоритму Ву
            Рисовать будем слева на право по оси с наибольшей скоростью роста
            (иначе линия будет прирывистой)
        """
        line = self.Line(p1, p2)  # координаты точек упорядоченные согласно условиям метода
        print()
        if line.change_axis:
            print(line.change_axis)
            x = line.x_start
            diff = line.dy/2
            print("dx=", line.dx, "dy=", line.dy)
            y_step = 1
            x_step = 1
            if line.y_start > line.y_end:
                y_step = -1
            print("start", line.y_start, "end", line.y_end)
            for y in range(line.y_start, line.y_end + y_step, y_step):
                print("diff", diff, "step", y_step)
                print("xy", x, y)
                self.bitmap[y][x] = 255
                diff -= line.dx
                if diff < 0:
                    x += x_step
                    diff += line.dy
        else:
            y = line.y_start
            diff = line.dx/2
            ystep = 1 if line.y_start < line.y_end else -1
            print("x1=", line.x1, "x2=", line.x2, "diff=", diff)
            print("y1=", line.y1, "y2=", line.y2, "k=", line.k, "dx=", line.dx, "dy=", line.dy)
            for x in range(line.x_start, line.x_end + 1):
                self.bitmap[y][x] = 255
                diff -= line.dy
                if diff < 0:
                    y += ystep
                    diff += line.dx




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

bitmap.draw_line(triangle.points[0], triangle.points[1])

# bitmap.add_noize(0.001)
bitmap.save()
# bitmap.show()

