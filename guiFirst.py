# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guiFirst.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1046, 537)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblImage = QtGui.QLabel(self.centralwidget)
        self.lblImage.setEnabled(True)
        self.lblImage.setMouseTracking(True)
        self.lblImage.setAcceptDrops(True)
        self.lblImage.setWhatsThis(_fromUtf8(""))
        self.lblImage.setAccessibleDescription(_fromUtf8(""))
        self.lblImage.setAutoFillBackground(True)
        self.lblImage.setText(_fromUtf8(""))
        self.lblImage.setScaledContents(True)
        self.lblImage.setOpenExternalLinks(True)
        self.lblImage.setObjectName(_fromUtf8("lblImage"))
        self.horizontalLayout.addWidget(self.lblImage)
        self.groupBoxFile = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxFile.setAutoFillBackground(True)
        self.groupBoxFile.setObjectName(_fromUtf8("groupBoxFile"))
        self.btnLoad = QtGui.QPushButton(self.groupBoxFile)
        self.btnLoad.setGeometry(QtCore.QRect(20, 30, 75, 23))
        self.btnLoad.setAccessibleDescription(_fromUtf8(""))
        self.btnLoad.setAutoFillBackground(False)
        self.btnLoad.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icon/openFile.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnLoad.setIcon(icon)
        self.btnLoad.setObjectName(_fromUtf8("btnLoad"))
        self.btnSave = QtGui.QPushButton(self.groupBoxFile)
        self.btnSave.setGeometry(QtCore.QRect(130, 30, 75, 23))
        self.btnSave.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icon/saveFile.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSave.setIcon(icon1)
        self.btnSave.setObjectName(_fromUtf8("btnSave"))
        self.btnAdd = QtGui.QPushButton(self.groupBoxFile)
        self.btnAdd.setGeometry(QtCore.QRect(20, 80, 75, 23))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icon/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAdd.setIcon(icon2)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.btnDelete = QtGui.QPushButton(self.groupBoxFile)
        self.btnDelete.setGeometry(QtCore.QRect(130, 80, 75, 23))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icon/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDelete.setIcon(icon3)
        self.btnDelete.setObjectName(_fromUtf8("btnDelete"))
        self.btnOpenImage = QtGui.QPushButton(self.groupBoxFile)
        self.btnOpenImage.setGeometry(QtCore.QRect(20, 130, 217, 24))
        self.btnOpenImage.setWhatsThis(_fromUtf8(""))
        self.btnOpenImage.setAccessibleDescription(_fromUtf8(""))
        self.btnOpenImage.setAutoFillBackground(False)
        self.btnOpenImage.setIcon(icon)
        self.btnOpenImage.setObjectName(_fromUtf8("btnOpenImage"))
        self.horizontalLayout.addWidget(self.groupBoxFile)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1046, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBoxFile.setTitle(_translate("MainWindow", "Annotate", None))
        self.btnAdd.setText(_translate("MainWindow", "Add", None))
        self.btnDelete.setText(_translate("MainWindow", "Delete", None))
        self.btnOpenImage.setText(_translate("MainWindow", "Open image", None))

import guiFirst_rc
