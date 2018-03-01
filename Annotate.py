import sys
from PyQt4 import QtCore, QtGui, uic
import guiAnnotate as guiPy


class MyApp(QtGui.QMainWindow, guiPy.Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        guiPy.Ui_MainWindow.__init__(self)
        self.setupUi(self)


    def openSlot(self):
        # This function is called when the user clicks File->Open.
        filename = QtGui.QFileDialog.getOpenFileName()
        print(filename)
        # Do your pixmap stuff here.


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())