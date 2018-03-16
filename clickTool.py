import pickle
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *



class ClickTool(QgsMapTool):

    def __init__(self, config, canvas, layer):
        self.config = config
        self.canvas = canvas
        self.layer = layer
        self.pointArray = list()
        self.point = None
        self.polygon = QgsRubberBand(self.canvas, True)
        self.adding = False
        QgsMapTool.__init__(self, self.canvas)

    def geoCoord2PixelPosition(self, point):
        if (self.config.pixSizeX == 1 and self.config.pixSizeY == 1):
            return QgsPoint(int(point.x()), int(point.y()))
        else:
            pixPosX = int(round((point.x() - self.config.topLeftX) / self.config.pixSizeX))
            pixPosY = int(round((self.config.topLeftY - point.y()) / self.config.pixSizeY))
            return QgsPoint(self.config.topLeftX + pixPosX * self.config.pixSizeX,
                            self.config.topLeftY - pixPosY * self.config.pixSizeY)
            # return QgsPoint(pixPosX, pixPosY)

    def canvasPressEvent(self, event):

        if event.button() == Qt.LeftButton and self.adding == True:
            self.point = self.canvas.getCoordinateTransform()
            self.point = self.point.toMapCoordinates(event.pos().x(), event.pos().y())
            self.point = self.geoCoord2PixelPosition(self.point)
            self.pointArray.append((self.point.x(), self.point.y()))
            print self.point.x(), self.point.y()
            self.showPolygon()

    def canvasDoubleClickEvent(self, QMouseEvent):
        """Try to deactivate the tool after doble clicking on the canvas
        Not finished yet..."""
        self.adding = False
        self.deactivate()

    def removeRubberband(self):
        """Remove certain rubberband when clicking on in the boundingbox"""
        pass



    def showPolygon(self):
        """ Shown an boundinbox defined.
        It would be nice to be designed as an size-adjustable polygon for user when annotating... """
        self.polygon.setBorderColor(QColor(255, 0, 0))
        self.polygon.setFillColor(QColor(0, 0, 0, 0))
        self.polygon.setLineStyle(Qt.DotLine)
        self.polygon.setWidth(3)
        bounding_points = []
        bounding_points.append(QgsPoint(self.point.x() - self.config.boundingboxSize * self.config.pixSizeX,
                                        self.point.y() - (-self.config.boundingboxSize * self.config.pixSizeY)))
        bounding_points.append(QgsPoint(self.point.x() + self.config.boundingboxSize * self.config.pixSizeX,
                                        self.point.y() - (-self.config.boundingboxSize * self.config.pixSizeY)))
        bounding_points.append(QgsPoint(self.point.x() + self.config.boundingboxSize * self.config.pixSizeX,
                                        self.point.y() + (-self.config.boundingboxSize * self.config.pixSizeY)))
        bounding_points.append(QgsPoint(self.point.x() - self.config.boundingboxSize * self.config.pixSizeX,
                                        self.point.y() + (-self.config.boundingboxSize * self.config.pixSizeY)))

        self.polygon.setToGeometry(QgsGeometry.fromPolygon([bounding_points]), None)
        self.addAnnotationsToDict(bounding_points)


    def addAnnotationsToDict(self, pts_list):
        """ Add every newly given annotation to a defined dictionary"""
        annotation_dict = {1 : pts_list}
        pickle_file_name = "annotations.pickle"
        try:
            pkl = pickle.load(open(pickle_file_name, "rb"))
        except(OSError, IOError):
            pickle.dump(annotation_dict, open(pickle_file_name, 'wb'))


    def saveAnnotationDictToFile(self):
        """ Save annotations to a pickle file"""



        pass