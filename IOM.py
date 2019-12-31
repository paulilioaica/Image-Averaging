# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Paul\Desktop\IOM.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
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


class Ui_Form(QWidget):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 400)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(420, 340, 70, 20))
        self.pushButton.setObjectName("pushButton")
        self.horizontalWidget = QtWidgets.QWidget(Form)
        self.horizontalWidget.setGeometry(QtCore.QRect(30, 30, 300, 300))
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.input = QLineEdit(Form)
        self.input.setGeometry(QtCore.QRect(440,315,20,20))
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label1 = QtWidgets.QLabel(Form)
        self.label1.setGeometry(QtCore.QRect(90, 340, 140, 16))
        self.label1.setObjectName("label")
        self.label2 = QtWidgets.QLabel(Form)
        self.label2.setGeometry(QtCore.QRect(400, 300, 140, 16))
        self.label2.setObjectName("label")
        self.graphicsView = QtWidgets.QLabel(Form)
        self.graphicsView.setGeometry(QtCore.QRect(360, 50, 191, 191))
        self.graphicsView.setObjectName("graphicsView")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(110, 360, 70, 20))
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
        self.pushButton_2.clicked.connect(self.displayImage)
        self.pushButton.clicked.connect(self.mediate_image)
        self.horizontalLayout.addWidget(self.treeview)
        self.horizontalLayout.addWidget(self.listview)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def displayImage(self):
        pictures = set()
        selections = self.listview.selectionModel().selectedIndexes()
        for picture in selections:
            filePath = self.dirModel.filePath(picture)
            if filePath.endswith("jpg") or filePath.endswith("png"):
                pictures.add(filePath)
        print(pictures)
        self.label1.setText("Number of images selected is {}".format(str(len(pictures))))
        if pictures:
            self.pictures = list(pictures)
            self.graphicsView.setPixmap(QtGui.QPixmap(self.pictures[0]).scaled(self.graphicsView.size()))

    def mediate_image(self):
        if self.input.text():
            num_images = int(self.input.text())
            if num_images > len(self.pictures):
                self.label2.setText("Number is bigger than selected pictures, please choose a smaller number")
                return
            self.pictures = self.pictures[:num_images]
            shape = (self.graphicsView.size().height(), self.graphicsView.size().width())
            final_shape = (self.graphicsView.size().height(), self.graphicsView.size().width(),3)
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
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Mediate Image"))
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
