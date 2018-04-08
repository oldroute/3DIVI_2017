from math import sqrt, pow, fabs
from settings import *
from random import randint, random


class Point:
    """ Случайная точка из массива PIXELS_NUM с дробными координатами (x,y) """
    def __init__(self, px_number: int=None):
        self.px_number = px_number if px_number else randint(0, PIXELS_NUM)
        self.x = self.px_number % PIXELS_OFFSET + random()
        self.y = self.px_number // PIXELS_OFFSET + random()

    def __str__(self):
        return "[%s, %s]" % (self.x, self.y)


class Segment:
    """ Отрезок из двух точек
        если точки случайные и длина отрезка получилась < MIN_SEGMENT_LENGTH
        то возьмем новые случайные точки и пересчитаем длину """

    def __set_correct_data(self):
        p1 = self.p1 if self.p1 else Point() # если одна из точек не задана(или обе) то возьмем случайные
        p2 = self.p2 if self.p2 else Point()
        length = sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2))
        incorrect_length = length < MIN_SEGMENT_LENGTH
        if self.is_rand and incorrect_length:
            return self.__set_correct_data()
        else:
            self.p1, self.p2, self.length = p1, p2, length
            self.vx = self.p2.x - self.p1.x
            self.vy = self.p2.y - self.p1.y
            return True

    def __init__(self, p1: Point=None, p2: Point=None):
        self.is_rand = not bool(p1 and p2)  # одна или обе точки случайные
        self.p1, self.p2 = p1, p2  # точки отрезка
        self.vx = self.vy = None   # координаты вектора
        self.length = None         # длина отрезка
        self.__set_correct_data()

    def __str__(self):
        return "\nКоординаты отрезка [%s, %s]----[%s, %s]\nДлина отрезка %s\nКоординаты вектора --[%s, %s]-->"\
               % (round(self.p1.x), round(self.p1.y), round(self.p2.x), round(self.p2.y),
                  round(self.length), round(self.vx), round(self.vy))


class Pair:
    """ Два отрезка из одной точки (две стороны треугольника)
        если один из отрезков случайный и угол между их векторами неверный
        то возьмем другой(другие) отрезки и пересчитаем"""

    def __calc_cos_angle(self):
        segment1 = self.segment1 if self.segment1 else Segment()
        segment2 = self.segment2 if self.segment2 else Segment(p1=segment1.p1)  # задаем общую точку двум отрезкам
        scalar = segment1.vx * segment2.vx + segment1.vy * segment2.vy          # скалярное произвежение векторов
        cos_angle = fabs(scalar/(segment1.length * segment2.length))            # cos угла между векторами отезков
        incorrect_angle = cos_angle < MIN_COS_ANGLE or cos_angle > MAX_COS_ANGLE
        if self.is_rand and incorrect_angle:
            return self.__calc_cos_angle()
        else:
            self.segment1, self.segment2 = segment1, segment2
            return cos_angle

    def __init__(self, segment1: Segment=None, segment2: Segment=None):
        self.is_rand = not bool(segment1 and segment2)     # один или оба отрезка случайные
        self.segment1, self.segment2 = segment1, segment2  # отрезки в паре, начинаются в одной точке
        self.cos_angle = self.__calc_cos_angle()           # cos угла меж векторов отрезков

    def __str__(self):
        return "\nОтрезок 1:%s\n\nОтрезок 2:%s\nУгол между векторами:%s\n" % \
               (self.segment1, self.segment2, self.cos_angle)


class Triangle:
    """ Треуголная фигура удовл. условиям """
    def __set_correct_data(self):
        pair1 = Pair()  # Берем пару отрезков удовл. условиям
        segment3 = Segment(pair1.segment2.p2, pair1.segment1.p2)  # Строим третий отрезок соед. концы первых двух
        incorrect_length = segment3.length < MIN_SEGMENT_LENGTH   # Проверяем условие длины для отрезка
        if incorrect_length:
            return self.__set_correct_data()
        pair2 = Pair(pair1.segment2, segment3)                    # Создаем пару отрезков включая второй и третий
        cos_angle3 = pi - (pair2.cos_angle + pair1.cos_angle)     # Проверяем условие угла для пары
        incorrect_cos_angle = cos_angle3 < MIN_COS_ANGLE
        if incorrect_cos_angle:
            return self.__set_correct_data()
        else:                                                     # Все 3 отрезка удовл. условиям и треугольник готов
            self.lengths = (pair1.segment1.length, pair1.segment2.length, segment3.length)
            self.points = (pair1.segment1.p1, pair1.segment1.p2, pair1.segment2.p2)
            self.angles = (pair1.cos_angle/ONE_ANGLE_DEGREE, pair2.cos_angle/ONE_ANGLE_DEGREE, cos_angle3/ONE_ANGLE_DEGREE)
            return True

    def __init__(self):
        self.lengths = tuple  # Длины сторон(отрезков)
        self.points = tuple   # Точки с координатами
        self.angles = tuple   # углы между сторон
        self.__set_correct_data()

    def __str__(self):
        return "\nТочки:\nA: %s\nB: %s\nC: %s" \
               "\nДлины:\nAB: %s\nBC: %s\nCA: %s"\
               "\nУглы:\nABC: %s\nBCA: %s\nCAB: %s"\
               % (self.points[0], self.points[1], self.points[2],
                  self.lengths[0], self.lengths[1], self.lengths[2],
                  self.angles[0], self.angles[1], self.angles[2])

