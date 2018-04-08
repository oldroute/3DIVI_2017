import os
from math import pi

PROJECT_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Destiny")  # Директория проекта
IMG_ROOT = os.path.join(PROJECT_ROOT, "img")  # директория папки с изображениями
try:
    os.stat(IMG_ROOT)
except:
    os.mkdir(IMG_ROOT)

IMG_SIZE = PIXELS_OFFSET = 500  # кол-во пикселей в строке
PIXELS_NUM = 250000             # кол-во пикселей в изображении
IMG_MODE = 255                  # цветовой режим
BLACK_PIXEL = 0                 # черный пиксель
MIN_COS_ANGLE = pi/6            # минимальный угол 30 градусов
MAX_COS_ANGLE = 2*pi/3          # максимальный угол 120 (иначе другой угол треугольника < 30 градусов)
ONE_ANGLE_DEGREE = pi/180     # 1 градус в радианах (для перевода из радиан в градусы, нужно только для отладки)
MIN_SEGMENT_LENGTH = 100        # минимальная длина стороны треугольника
