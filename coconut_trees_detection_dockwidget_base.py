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

        # Add load and save buttons
        self.btnLoadAnnotationFile = QtGui.QPushButton(self.dockWidgetContents)
        self.btnLoadAnnotationFile.setGeometry(QtCore.QRect(50, 50, 110, 32))
        self.btnLoadAnnotationFile.setObjectName(_fromUtf8("btnLoadAnnotationFile"))
        self.btnSaveAnnotationFile = QtGui.QPushButton(self.dockWidgetContents)
        self.btnSaveAnnotationFile.setGeometry(QtCore.QRect(180, 50, 110, 32))
        self.btnSaveAnnotationFile.setObjectName(_fromUtf8("btnSaveAnnotationFile"))

        # Add Coco and Non coco annotation buttons
        self.btnAddAnnotationCoco = QtGui.QPushButton(self.dockWidgetContents)
        self.btnAddAnnotationCoco.setGeometry(QtCore.QRect(50, 110, 110, 32))
        self.btnAddAnnotationCoco.setObjectName(_fromUtf8("btnAddAnnotationCoco"))
        self.btnAddAnnotationNoncoco = QtGui.QPushButton(self.dockWidgetContents)
        self.btnAddAnnotationNoncoco.setGeometry(QtCore.QRect(180, 110, 110, 32))
        self.btnAddAnnotationNoncoco.setObjectName(_fromUtf8("btnAddAnnotationNoncoco"))

        # Delete button
        self.btnDeleteAnnotation = QtGui.QPushButton(self.dockWidgetContents)
        self.btnDeleteAnnotation.setGeometry(QtCore.QRect(50, 170, 110, 32))
        self.btnDeleteAnnotation.setObjectName(_fromUtf8("btnDeleteAnnotation")
                                               )
        self.btnDeleteAllAnnotation = QtGui.QPushButton(self.dockWidgetContents)
        self.btnDeleteAllAnnotation.setGeometry(QtCore.QRect(180, 170, 110, 32))
        self.btnDeleteAllAnnotation.setObjectName(_fromUtf8("btnDeleteAllAnnotation"))

        # Process and classify buttons
        self.btnPreprocess = QtGui.QPushButton(self.dockWidgetContents)
        self.btnPreprocess.setGeometry(QtCore.QRect(50, 230, 110, 32))
        self.btnPreprocess.setObjectName(_fromUtf8("btnPreprocess"))
        self.btnClassify = QtGui.QPushButton(self.dockWidgetContents)
        self.btnClassify.setGeometry(QtCore.QRect(180, 230, 110, 32))
        self.btnClassify.setObjectName(_fromUtf8("btnClassify"))

        # Visualize
        self.btnVisualize = QtGui.QPushButton(self.dockWidgetContents)
        self.btnVisualize.setGeometry(QtCore.QRect(50, 290, 110, 32))
        self.btnVisualize.setObjectName(_fromUtf8("btnVisualize"))
        self.btnTest = QtGui.QPushButton(self.dockWidgetContents)
        self.btnTest.setGeometry(QtCore.QRect(180, 290, 110, 32))
        self.btnTest.setObjectName(_fromUtf8("btnTest"))

        # Validate
        self.btnValidate = QtGui.QPushButton(self.dockWidgetContents)
        self.btnValidate.setGeometry(QtCore.QRect(50, 350, 110, 32))
        self.btnValidate.setObjectName(_fromUtf8("btnValidate"))


        # #-----------widget test for accessing mouse coordinates, remove later
        # self.textMouseCoords = QtGui.QPlainTextEdit(self.dockWidgetContents)
        # self.textMouseCoords.setGeometry(QtCore.QRect(50, 170, 110, 32))

        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "DockWidget", None))
        self.btnAddAnnotationCoco.setText(_translate("DockWidget", "Add Coconut", None))
        self.btnDeleteAnnotation.setText(_translate("DockWidget", "Delete", None))
        self.btnLoadAnnotationFile.setText(_translate("DockWidget", "Load", None))
        self.btnSaveAnnotationFile.setText(_translate("DockWidget", "Save", None))
        self.btnClassify.setText(_translate("DockWidget", "Classify", None))
        self.btnPreprocess.setText(_translate("DockWidget", "Preprocess", None))
        self.btnAddAnnotationNoncoco.setText(_translate("DockWidget", "Add Others", None))
        self.btnDeleteAllAnnotation.setText(_translate("DockWidget", "Delete All", None))
        self.btnVisualize.setText(_translate("DockWidget", "Visualize", None))
        self.btnTest.setText(_translate("DockWidget", "Run Test", None))
        self.btnValidate.setText(_translate("DockWidget", "Run Validation", None))





