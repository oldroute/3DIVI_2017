from math import sqrt, pow, fabs, acos, pi
from settings import *
from random import randint, random, uniform


class Point:
    """ Точка, если координата не указана то берется случайная
        в интервале [0, PIXELS_NUM) с дробными координатами """
    def __init__(self, x: int=None, y: int=None):
        self.x = x if x else uniform(0, IMG_SIZE-1)
        self.y = y if y else uniform(0, IMG_SIZE-1)

    def __str__(self):
        return "[%s, %s]" % (self.x, self.y)


class Line:
    """ Отрезок, если точка отрезка не указана, то берется случайная """

    def __init__(self, p1: Point=None, p2: Point=None):
        self.p1, self.p2 = p1, p2    # точки отрезка
        fixed_points = p1 and p2     # обе точки фиксированные
        if fixed_points:
            self.length = sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2))
        else:  # если одна из точек не указана то генерируем случайную линию
            while True:
                _p1 = p1 if p1 else Point()  # если одна из точек не задана(или обе) то возьмем случайные
                _p2 = p2 if p2 else Point()
                _length = sqrt(pow(_p1.x - _p2.x, 2) + pow(_p1.y - _p2.y, 2)) # формула длины отрезка
                if (_length >= MIN_LINE_LENGTH) and (_length <= MAX_LINE_LENGTH):
                    self.p1, self.p2, self.length = _p1, _p2, _length
                    break
        self.vx = self.p2.x - self.p1.x  # координаты вектора
        self.vy = self.p2.y - self.p1.y

    def __str__(self):
        return "\n Отрезок (%s, %s)----(%s, %s)\nДлина %s\nКоординаты вектора --(%s, %s)-->"\
               % (round(self.p1.x), round(self.p1.y), round(self.p2.x), round(self.p2.y),
                  round(self.length), round(self.vx), round(self.vy))


class Pair:
    """ Два отрезка из одной точки (две стороны треугольника)
        """

    def __init__(self, line1: Line=None, line2: Line=None, max_angle: float=120.0):
        self.line1 = line1
        self.line2 = line2   # задаем общую точку двум отрезкам
        fixed_lines = bool(line1 and line2)     # фиксированные отрезки

        if fixed_lines:
            scalar = line1.vx * line2.vx + line1.vy * line2.vy          # скалярное произвежение векторов
            self.cos_angle = (scalar/(line1.length * line2.length))     # cos угла между векторами отезков
            self.angle = acos(self.cos_angle)/(pi/180)
        else:
            while True:
                _line1 = line1 if line1 else Line()
                _line2 = line2 if line2 else Line(p1=_line1.p2)
                scalar = _line1.vx * _line2.vx + _line1.vy * _line2.vy
                _cos_angle = (scalar/(_line1.length * _line2.length))
                _angle = acos(_cos_angle)/(pi/180)  # по значению косинуса восстановим значение угла в градусах
                correct_angle = (_angle >= MIN_ANGLE) and (_angle <= max_angle)
                if correct_angle:
                    self.line1, self.line2, self.cos_angle, self.angle = _line1, _line2, _cos_angle, _angle
                    break

    def __str__(self):
        return "\nОтрезок 1:%s\n\nОтрезок 2:%s\nУгол между векторами:%s\n" % \
               (self.line1, self.line2, self.angle)


class Triangle:
    """
        Треуголная фигура удовл. условиям мин. длины сторон и мин угла
        условие длины стороны проверяется при построении каждой линии
        условие мин. угла проверяется при построении пары
    """
    def __init__(self):
        _pair1 = Pair()
        self.p1, self.p2, self.p3 = _pair1.line1.p1, _pair1.line1.p2, _pair1.line2.p2

