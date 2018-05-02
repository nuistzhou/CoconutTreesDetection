import os
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
        self.rubberbandsList = list()
        self.annotationList = list()

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
        self.point = self.canvas.getCoordinateTransform()
        self.point = self.point.toMapCoordinates(event.pos().x(), event.pos().y())

        # self.point = self.geoCoord2PixelPosition(self.point)
        # if event.button() == Qt.LeftButton and self.adding == True:
        if self.adding == True:
            # self.pointArray.append((self.point.x(), self.point.y()))
            self.boundingBoxPointsCoords = self.generateBoundingPointsCoordinates()
            self.rubberband = self.createRubberbands(self.boundingBoxPointsCoords)
            self.rubberband.show()

            # Add this annotation to self.annotationList
            self.annotationList.append(self.boundingBoxPointsCoords)

            # Add rubberband to the self.rubberbandsList
            self.rubberbandsList.append(self.rubberband)


        elif self.deleting == True:
            # Remove the rubberband from the canvas and also delete from the dictionary, pickle file
            self.removeRubberband()

    def canvasDoubleClickEvent(self, QMouseEvent):

        # print vertex_items
        """Try to deactivate the tool after doble clicking on the canvas
        Not finished yet..."""
        # self.adding = False
        # self.deactivate()

    def removeRubberband(self):
        """Remove certain rubberband when clicking on in the boundingbox
        @type rubberband: QgsRubberBand"""
        rubberbands = [i for i in self.canvas.scene().items() if isinstance(i, QgsRubberBand)]

        print len(self.annotationList)
        print len(rubberbands)
        for i, annotation in enumerate(self.annotationList):
            pt1_x, pt1_y = annotation[0]
            pt3_x, pt3_y = annotation[2]

            if ((self.point.x() <= pt3_x) and (self.point.x() >= pt1_x) and
                (self.point.y() <= pt1_y) and (self.point.y() >= pt3_y)):

                print "Top left:", pt1_x, pt1_y
                print "Bottom right:", pt3_x, pt3_y
                print "Clicked point:", self.point.x(), self.point.y()

                self.annotationList.pop(i)
                self.canvas.scene().removeItem(rubberbands[i])
                break

        with open(Parameters.annotationFile, 'w') as f:
             pickle.dump(self.annotationList, f)

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
        """Create and return the rubberband object"""
        boundingQgsPtsList = list()
        self.polygon = QgsRubberBand(self.canvas, True)  # True means a polygon
        self.polygon.setBorderColor(QColor(255, 0, 0))
        self.polygon.setFillColor(QColor(0, 0, 0, 0))
        self.polygon.setLineStyle(Qt.DotLine)
        self.polygon.setWidth(3)

        for pt_x, pt_y in boundingPoints:
            boundingQgsPtsList.append(QgsPoint(pt_x, pt_y))
        self.polygon.addGeometry(QgsGeometry.fromPolygon([boundingQgsPtsList]), None)
        return self.polygon

    def displayAnnotations(self):
        rubberbands = [i for i in self.canvas.scene().items() if isinstance(i, QgsRubberBand)]
        for rubberband in rubberbands:
            self.canvas.scene().removeItem(rubberband)

        self.rubberbandsList = list()
        for annotation in self.annotationList:
            rubberband = self.createRubberbands(annotation)
            self.rubberbandsList.append(rubberband)
            rubberband.show()




