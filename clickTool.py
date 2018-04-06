import pickle
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from config import Parameters



class ClickTool(QgsMapTool):

    def __init__(self, config, canvas, layer):
        self.config = config
        self.canvas = canvas
        self.layer = layer
        self.pointArray = list()
        self.point = None
        self.adding = False # Switch for adding annotations
        self.deleting = False # Switch for deleting annotations
        self.rubberbandsDict = dict()
        self.rubberbandsFound = 0
        self.annotationDict = dict()
        self.annotationDictLen = len(self.annotationDict)
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

        # if event.button() == Qt.LeftButton and self.adding == True:
        if self.adding == True:
            self.point = self.canvas.getCoordinateTransform()
            self.point = self.point.toMapCoordinates(event.pos().x(), event.pos().y())
            self.point = self.geoCoord2PixelPosition(self.point)
            self.pointArray.append((self.point.x(), self.point.y()))
            self.boundingBoxPointsCoords = self.generateBoundingPointsCoordinates()
            self.createRubberbands(self.boundingBoxPointsCoords)
            self.showPolygon()
            self.addAnnotationsToDict()

    def canvasDoubleClickEvent(self, QMouseEvent):
        pass
        """Try to deactivate the tool after doble clicking on the canvas
        Not finished yet..."""
        # self.adding = False
        # self.deactivate()

    def removeRubberband(self):
        """Remove certain rubberband when clicking on in the boundingbox"""
        pass


    def generateBoundingPointsCoordinates(self):
        """Generate the 4 bounding points around the clicked point
        In the QGIS canvas coordinates system, the starting point is Bottom-Left, then increases along
        both axises"""
        list_bounding_points_coords = []

        # Top Left
        list_bounding_points_coords.append((self.point.x() - self.config.boundingboxSize * self.config.pixSizeX,
                                        self.point.y() - (-self.config.boundingboxSize * self.config.pixSizeY)))
        # Top Right
        list_bounding_points_coords.append((self.point.x() + self.config.boundingboxSize * self.config.pixSizeX,
                                        self.point.y() - (-self.config.boundingboxSize * self.config.pixSizeY)))

        # Bottom Right
        list_bounding_points_coords.append((self.point.x() + self.config.boundingboxSize * self.config.pixSizeX,
                                            self.point.y() + (-self.config.boundingboxSize * self.config.pixSizeY)))

        # Bottom Left
        list_bounding_points_coords.append((self.point.x() - self.config.boundingboxSize * self.config.pixSizeX,
                                            self.point.y() + (-self.config.boundingboxSize * self.config.pixSizeY)))


        return list_bounding_points_coords

    def createRubberbands(self, boundingPoints):
        boundingQgsPtsList = list()
        self.polygon = QgsRubberBand(self.canvas, True)  # True means a polygon
        self.polygon.setBorderColor(QColor(255, 0, 0))
        self.polygon.setFillColor(QColor(0, 0, 0, 0))
        self.polygon.setLineStyle(Qt.DotLine)
        self.polygon.setWidth(3)

        for pt_x, pt_y in boundingPoints:
            boundingQgsPtsList.append(QgsPoint(pt_x, pt_y))
        self.polygon.addGeometry(QgsGeometry.fromPolygon([boundingQgsPtsList]), None)
        self.rubberbandsDict[self.rubberbandsFound] = self.polygon
        self.rubberbandsFound += 1
    def showPolygon(self):
        """ Shown an boundinbox defined.
        It would be nice to be designed as an size-adjustable polygon for user when annotating... """
        self.polygon.asGeometry()

    def addAnnotationsToDict(self):
        """ Add every newly given annotation to a defined dictionary"""
        self.annotationDict[self.annotationDictLen + 1] = self.boundingBoxPointsCoords

    def deleteAnnotationsWhenClickedInside(self):
        pass
        # for index, coordsList in self.annotationDict.iteritems():
        #     top_left_x = coordsList[0][0]
        #     top_left_y = coordsList[0][1]
        #     bottom_right_x = coordsList[3][0]
        #     bottom_right_y = coordsList[3][1]
        #     self.polygon.reset()
        #     if  (top_left_x <= self.point.x() <= bottom_right_x) and
        #         (top_left_y >= self.point.y() >= bottom_right_y):



