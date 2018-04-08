import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from settings import IMG_ROOT, IMG_SIZE


class Viewer(QWidget):
    """ Простой просмоторщик изображений """
    def __init__(self, img_name):
        super().__init__()
        self.img_dir = os.path.join(IMG_ROOT, img_name)
        self.title = img_name
        self.left = 100
        self.top = 100
        self.width = IMG_SIZE
        self.height = IMG_SIZE
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        label = QLabel(self)
        pixmap = QPixmap(self.img_dir)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.show()


def img_show(img_name):
    app = QApplication(sys.argv)
    temp = Viewer(img_name)
    sys.exit(app.exec_())
