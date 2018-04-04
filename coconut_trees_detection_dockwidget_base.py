# -*- coding: utf-8 -*-

# Form implementation generated from reading ui filePickle 'coconut_trees_detection_dockwidget_base.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this filePickle will be lost!

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

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(356, 247)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.btnAddAnnotation = QtGui.QPushButton(self.dockWidgetContents)
        self.btnAddAnnotation.setGeometry(QtCore.QRect(50, 110, 110, 32))
        self.btnAddAnnotation.setObjectName(_fromUtf8("btnAddAnnotation"))
        self.btnDeleteAnnotation = QtGui.QPushButton(self.dockWidgetContents)
        self.btnDeleteAnnotation.setGeometry(QtCore.QRect(180, 110, 110, 32))
        self.btnDeleteAnnotation.setObjectName(_fromUtf8("btnDeleteAnnotation"))
        self.btnLoadAnnotationFile = QtGui.QPushButton(self.dockWidgetContents)
        self.btnLoadAnnotationFile.setGeometry(QtCore.QRect(50, 50, 110, 32))
        self.btnLoadAnnotationFile.setObjectName(_fromUtf8("btnLoadAnnotationFile"))
        self.btnSaveAnnotationFile = QtGui.QPushButton(self.dockWidgetContents)
        self.btnSaveAnnotationFile.setGeometry(QtCore.QRect(180, 50, 110, 32))
        self.btnSaveAnnotationFile.setObjectName(_fromUtf8("btnSaveAnnotationFile"))


        # #-----------widget test for accessing mouse coordinates, remove later
        # self.textMouseCoords = QtGui.QPlainTextEdit(self.dockWidgetContents)
        # self.textMouseCoords.setGeometry(QtCore.QRect(50, 170, 110, 32))

        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "DockWidget", None))
        self.btnAddAnnotation.setText(_translate("DockWidget", "Add", None))
        self.btnDeleteAnnotation.setText(_translate("DockWidget", "Delete", None))
        self.btnLoadAnnotationFile.setText(_translate("DockWidget", "Load", None))
        self.btnSaveAnnotationFile.setText(_translate("DockWidget", "Save", None))

