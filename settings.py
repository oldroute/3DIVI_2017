import os
from math import pi, cos

PROJECT_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Destiny")  # Директория проекта
IMG_ROOT = os.path.join(PROJECT_ROOT, "img")  # директория папки с изображениями
try:
    os.stat(IMG_ROOT)
except:
    os.mkdir(IMG_ROOT)

IMG_SIZE = PIXELS_OFFSET = 500  # кол-во пикселей в строке
PIXELS_NUM = IMG_SIZE * IMG_SIZE             # кол-во пикселей в изображении
IMG_MODE = WHITE_PIXEL = 255    # цветовой режим
BLACK_PIXEL = 0                 # черный пиксель

MIN_ANGLE = 30
MIN_LINE_LENGTH = 100           # минимальная длина стороны треугольника
MAX_LINE_LENGTH = IMG_SIZE
