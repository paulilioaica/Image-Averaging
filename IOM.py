from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout
import numpy as np
from PyQt5.QtGui import QIcon
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import qimage2ndarray
from PIL import Image

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

BUTTONS_WIDTH = 0.048
BUTTONS_HEIGHT = 0.027

TEXT_WIDTH = 0.2
TEXT_HEIGHT = 0.012


class Ui_Form(QWidget):
    def setupUi(self, Form):
        sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
        screen_width = sizeObject.width()
        screen_height = sizeObject.height()
        Form.setObjectName("Image Averaging")
        Form.setFixedSize(800, 500)

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(
            QtCore.QRect(480, 340, BUTTONS_WIDTH * screen_width, BUTTONS_HEIGHT * screen_height))
        self.pushButton.setObjectName("pushButton")

        self.horizontalWidget = QtWidgets.QWidget(Form)
        self.horizontalWidget.setGeometry(QtCore.QRect(30, 30, 300, 300))
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.input = QLineEdit(Form)
        self.input.setGeometry(QtCore.QRect(530, 315, 0.01 * screen_width, 0.015 * screen_height))

        self.label1 = QtWidgets.QLabel(Form)
        self.label1.setGeometry(QtCore.QRect(90, 340, TEXT_WIDTH * screen_width, TEXT_HEIGHT * screen_height))
        self.label1.setObjectName("label")
        self.label2 = QtWidgets.QLabel(Form)
        self.label2.setGeometry(QtCore.QRect(470, 300, TEXT_WIDTH * screen_width, TEXT_HEIGHT * screen_height))
        self.label2.setObjectName("label")

        self.graphicsView = QtWidgets.QLabel(Form)
        self.graphicsView.setGeometry(QtCore.QRect(430, 30, 270, 270))
        self.graphicsView.setObjectName("graphicsView")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(
            QtCore.QRect(110, 360, BUTTONS_WIDTH * screen_width, BUTTONS_HEIGHT * screen_height))
        self.pushButton_2.setObjectName("pushButton_2")

        self.treeview = QTreeView()
        self.listview = QListView()
        self.listview.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.path = QDir.rootPath()

        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(QDir.rootPath())
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)

        self.fileModel = QFileSystemModel()
        self.fileModel.setFilter(QDir.NoDotAndDotDot | QDir.Files)

        self.treeview.setModel(self.dirModel)
        self.listview.setModel(self.fileModel)

        self.treeview.setRootIndex(self.dirModel.index(self.path))
        self.listview.setRootIndex(self.fileModel.index(self.path))

        self.treeview.clicked.connect(self.on_clicked)
        self.pushButton_2.clicked.connect(self.display_image)
        self.pushButton.clicked.connect(self.average)
        self.horizontalLayout.addWidget(self.treeview)
        self.horizontalLayout.addWidget(self.listview)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def display_image(self):
        pictures = set()
        selections = self.listview.selectionModel().selectedIndexes()
        for picture in selections:
            filePath = self.dirModel.filePath(picture)
            if filePath.endswith("jpg") or filePath.endswith("png") or filePath.endswith("jfif"):
                pictures.add(filePath)
        print(pictures)
        self.label1.setText("Number of images selected is {}".format(str(len(pictures))))
        if pictures:
            self.pictures = list(pictures)
            self.graphicsView.setPixmap(QtGui.QPixmap(self.pictures[0]).scaled(self.graphicsView.size()))

    def average(self):
        if self.input.text():
            num_images = int(self.input.text())
            if num_images > len(self.pictures):
                self.label2.setText("Number is bigger than selected pictures")
                return
            self.pictures = self.pictures[:num_images]
            shape = (self.graphicsView.size().height(), self.graphicsView.size().width())
            final_shape = (self.graphicsView.size().width(), self.graphicsView.size().height(), 3)
            pils = []
            for pic in self.pictures:
                pils.append(np.array(Image.open(pic).resize(shape)))
            final_image = np.zeros(final_shape)
            for pil in pils:
                final_image += pil
            final_image /= num_images
            qimg = qimage2ndarray.array2qimage(final_image)
            pixmap = QPixmap.fromImage(qimg)
            self.graphicsView.setPixmap(pixmap)

    def on_clicked(self, index):
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        self.listview.setRootIndex(self.fileModel.setRootPath(path))

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Image Averaging", "Image Averaging" ))
        self.pushButton.setText(_translate("Form", "Average Images"))
        self.label1.setText(_translate("Form", "Number of images selected:"))
        self.label2.setText(_translate("Form", "Select number of images to use"))
        self.pushButton_2.setText(_translate("Form", "Choose images"))
        self.input.setText(_translate("Form", ""))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

