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

    def __init__(self, config, canvas, layer, imgArray):
        self.config = config
        self.canvas = canvas
        self.layer = layer
        self.imgArray = imgArray
        self.pointArray = list()
        self.point = None
        self.adding = False # Switch for adding annotations
        self.deleting = False # Switch for deleting annotations
        self.rubberbandsList = list()
        self.annotationList = list()
        self.patchList = list()

        QgsMapTool.__init__(self, self.canvas)

    def geoCoord2PixelPosition(self, point):
        if (self.config.pixSizeX == 1 and self.config.pixSizeY == 1):
            return QgsPoint(int(point.x()), int(point.y()))
        else:
            pixPosX = int(round((point.x() - self.config.topLeftX) / self.config.pixSizeX))
            pixPosY = int(round((self.config.topLeftY - point.y()) / self.config.pixSizeY))
            return QgsPoint(self.config.topLeftX + pixPosX * self.config.pixSizeX,
                            self.config.topLeftY - pixPosY * self.config.pixSizeY)

    def mapCoords2PixelCoords(self, coordsList):
        """Convert a geometry's map coordinates into a list of pixels' coordinates
        coordsList: a list of bounding points of the geometry"""
        pixelCoordsList = list()
        for i, coords in enumerate(coordsList):
            if i % 2 == 0:
                pixPosX = int(round((coords[0] - self.config.topLeftX) / self.config.pixSizeX))
                pixPosY = int(round((self.config.topLeftY - coords[1]) / self.config.pixSizeY))
                pixelCoordsList.append((pixPosX, pixPosY))
            else:
                continue
        return pixelCoordsList

    def extractPatchAsArray(self, boundingBoxPointsCoordsList):
        topLeftX, topLeftY = boundingBoxPointsCoordsList[0]
        bottomRightX, bottomRightY = boundingBoxPointsCoordsList[1]
        patchArray = self.imgArray[topLeftY: bottomRightY, topLeftX : bottomRightX, :]
        return patchArray

    def canvasPressEvent(self, event):
        self.point = self.canvas.getCoordinateTransform()
        self.point = self.point.toMapCoordinates(event.pos().x(), event.pos().y())

        if self.adding == True:
            # self.pointArray.append((self.point.x(), self.point.y()))
            self.boundingBoxPointsCoords = self.generateBoundingPointsCoordinates()

            self.rubberband = self.createRubberbands(self.boundingBoxPointsCoords)
            self.rubberband.show()

            # Add this annotation to self.annotationList
            self.annotationList.append(self.boundingBoxPointsCoords)

            # Add rubberband to the self.rubberbandsList
            self.rubberbandsList.append(self.rubberband)

            # Return bounding box top-left and bottom-right point pixel coordinates

            pointsArrayList = self.mapCoords2PixelCoords(self.boundingBoxPointsCoords)
            self.patchList.append(self.extractPatchAsArray(pointsArrayList))


        elif self.deleting == True:
            # Remove the rubberband from the canvas and also delete from the dictionary, pickle file
            self.removeRubberband()

    def canvasDoubleClickEvent(self, QMouseEvent):

        """Try to deactivate the tool after doble clicking on the canvas
        Not finished yet..."""
        # self.adding = False
        # self.deactivate()

    def removeRubberband(self):
        """Remove certain rubberband when clicking on in the boundingbox
        @type rubberband: QgsRubberBand"""
        # rubberbands = [i for i in self.canvas.scene().items() if isinstance(i, QgsRubberBand)]
        for i, annotation in enumerate(self.annotationList):
            pt1_x, pt1_y = annotation[0]
            pt3_x, pt3_y = annotation[2]

            if ((self.point.x() <= pt3_x) and (self.point.x() >= pt1_x) and
                (self.point.y() <= pt1_y) and (self.point.y() >= pt3_y)):

                self.annotationList.pop(i)
                self.canvas.scene().removeItem(self.rubberbandsList[i])
                self.rubberbandsList.pop(i)
                self.patchList.pop(i)
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




