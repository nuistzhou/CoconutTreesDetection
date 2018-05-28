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
        self.addingCoco = False
        self.addingNoncoco = False
        self.deleting = False # Switch for deleting annotations
        self.rubberbandsCocoList = list()
        self.rubberbandsNoncocoList = list()
        self.annotationCocoList = list()
        self.annotationNoncocoList = list()
        self.patchArrayCocoList = list()
        self.patchArrayNoncocoList = list()

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

        if self.addingCoco == True or self.addingNoncoco == True:
            # self.pointArray.append((self.point.x(), self.point.y()))
            self.boundingBoxPointsCoords = self.generateBoundingPointsCoordinates()
            pointsArrayList = self.mapCoords2PixelCoords(self.boundingBoxPointsCoords)

            # Add this annotation to self.annotationCocoList
            if self.addingCoco == True:
                self.rubberband = self.createRubberbands(self.boundingBoxPointsCoords, 'red')
                self.rubberband.show()
                self.annotationCocoList.append(self.boundingBoxPointsCoords)

                # Add rubberband to the self.rubberbandsCocoList
                self.rubberbandsCocoList.append(self.rubberband)

                # Return bounding box top-left and bottom-right point pixel coordinates

                self.patchArrayCocoList.append(self.extractPatchAsArray(pointsArrayList))
            else:

                self.rubberband = self.createRubberbands(self.boundingBoxPointsCoords, 'blue')
                self.rubberband.show()

                self.annotationNoncocoList.append(self.boundingBoxPointsCoords)

                # Add rubberband to the self.rubberbandsCocoList
                self.rubberbandsNoncocoList.append(self.rubberband)

                # Return bounding box top-left and bottom-right point pixel coordinates

                self.patchArrayNoncocoList.append(self.extractPatchAsArray(pointsArrayList))


        elif self.deleting == True:
            # Remove the rubberband from the canvas and also delete from the dictionary, pickle file
            self.removeRubberband()

    def canvasDoubleClickEvent(self, QMouseEvent):

        """Try to deactivate the tool after doble clicking on the canvas
        Not finished yet..."""
        # self.addingCoco = False
        # self.deactivate()

    def removeRubberband(self):
        """Remove certain rubberband when clicking on in the boundingbox
        @type rubberband: QgsRubberBand"""
        # rubberbands = [i for i in self.canvas.scene().items() if isinstance(i, QgsRubberBand)]
        for i, annotation in enumerate(self.annotationCocoList):
            pt1_x, pt1_y = annotation[0]
            pt3_x, pt3_y = annotation[2]

            if ((self.point.x() <= pt3_x) and (self.point.x() >= pt1_x) and
                (self.point.y() <= pt1_y) and (self.point.y() >= pt3_y)):

                #
                # print "Number of coco_annot {0}".format(len(self.annotationCocoList))
                # print "Number of coco_rubberbands {0}".format(len(self.rubberbandsCocoList))

                self.annotationCocoList.pop(i)
                self.canvas.scene().removeItem(self.rubberbandsCocoList[i])
                self.rubberbandsCocoList.pop(i)
                #
                # print "After removal:"
                # print "Number of coco_annot {0}".format(len(self.annotationCocoList))
                # print "Number of coco_rubberbands {0}".format(len(self.rubberbandsCocoList))

                self.patchArrayCocoList.pop(i)

                # Write change to the pickle file
                with open(Parameters.annotationCocoFile, 'w') as f:
                    pickle.dump(self.annotationCocoList, f)
                return

        for i, annotation in enumerate(self.annotationNoncocoList):
            pt1_x, pt1_y = annotation[0]
            pt3_x, pt3_y = annotation[2]

            if ((self.point.x() <= pt3_x) and (self.point.x() >= pt1_x) and
                (self.point.y() <= pt1_y) and (self.point.y() >= pt3_y)):

                self.annotationNoncocoList.pop(i)
                self.canvas.scene().removeItem(self.rubberbandsNoncocoList[i])
                self.rubberbandsNoncocoList.pop(i)
                self.patchArrayNoncocoList.pop(i)
                # Write change to the pickle file
                with open(Parameters.annotationNoncocoFile, 'w') as f:
                    pickle.dump(self.annotationNoncocoList, f)
                return
    def deleteAllAnnnotaions(self):
        """Delete all annotations!"""
        rubberbands = [i for i in self.canvas.scene().items() if isinstance(i, QgsRubberBand)]
        for rubberband in rubberbands:
            self.canvas.scene().removeItem(rubberband)
        self.annotationNoncocoList = list()
        self.annotationCocoList = list()
        self.rubberbandsCocoList = list()
        self.rubberbandsNoncocoList = list()
        self.patchArrayCocoList = list()
        self.patchArrayNoncocoList = list()


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

    def createRubberbands(self, boundingPoints, color):
        """Create and return the rubberband object"""
        boundingQgsPtsList = list()
        self.polygon = QgsRubberBand(self.canvas, True)  # True means a polygon
        if color == 'red':
            self.polygon.setBorderColor(QColor(255, 0, 0))
        elif color == 'blue':
            self.polygon.setBorderColor(QColor(0, 0, 255))
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

        self.rubberbandsCocoList = list()
        self.rubberbandsNoncocoList = list()

        for annotation in self.annotationCocoList:
            rubberband = self.createRubberbands(annotation, 'red')
            self.rubberbandsCocoList.append(rubberband)
            rubberband.show()
            pointsArrayList = self.mapCoords2PixelCoords(annotation)
            self.patchArrayCocoList.append(self.extractPatchAsArray(pointsArrayList))


        for annotation in self.annotationNoncocoList:
            rubberband = self.createRubberbands(annotation, 'blue')
            self.rubberbandsNoncocoList.append(rubberband)
            rubberband.show()
            pointsArrayList = self.mapCoords2PixelCoords(annotation)
            self.patchArrayNoncocoList.append(self.extractPatchAsArray(pointsArrayList))




