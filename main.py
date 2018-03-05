import sys
from PyQt4 import QtCore, QtGui, uic
from guiFirst import *


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.btnOpenImage.clicked.connect(self.loadImage)


    def loadImage(self):

        fileImage = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                      'c:\\', "Image files (*.tif *.png *.jpg)")
        self.lblImage.setPixmap(QtGui.QPixmap(fileImage))
        self.lblImage.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())