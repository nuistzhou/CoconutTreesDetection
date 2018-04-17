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
        self.point = self.geoCoord2PixelPosition(self.point)
        # if event.button() == Qt.LeftButton and self.adding == True:
        if self.adding == True:
            self.pointArray.append((self.point.x(), self.point.y()))
            self.boundingBoxPointsCoords = self.generateBoundingPointsCoordinates()
            self.createRubberbands(self.boundingBoxPointsCoords)
            self.showPolygon()
            self.addAnnotationsToList()

        elif self.deleting == True:
            # Remove the rubberband from the canvas and also delete from the dictionary, pickle file
            self.removeRubberband()

    def canvasDoubleClickEvent(self, QMouseEvent):
        pass
        """Try to deactivate the tool after doble clicking on the canvas
        Not finished yet..."""
        # self.adding = False
        # self.deactivate()

    def removeRubberband(self):
        """Remove certain rubberband when clicking on in the boundingbox
        @type rubberband: QgsRubberBand"""
        removed_index = int()
        for i,rubberband in enumerate(self.rubberbandsList):
            print rubberband.asGeometry()
            # print self.point.geometryType()
            print type(self.point)
            # if rubberband.asGeometry().contains(QgsGeometry.fromPoint(self.point)):
            if True:
            # if QgsGeometry.fromPoint(self.point).within(rubberband.asGeometry()):
                print '%%@%%##'
                # removed_index = i
                # self.canvas.scene().removeItem(rubberband)
                # del self.rubberbandsList[removed_index]
                # del self.annotationList[removed_index]
                for i in range(len(self.rubberbandsList)):
                    self.rubberbandsList[i].reset()
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

        print self.point.x(), self.point.y()
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
        self.rubberbandsList.append(self.polygon)
    def showPolygon(self):
        """ Shown an boundinbox defined.
        It would be nice to be designed as an size-adjustable polygon for user when annotating... """
        # self.polygon.asGeometry()
        self.polygon.show()


    def addAnnotationsToList(self):
        """ Add every newly given annotation to a defined List"""
        self.annotationList.append(self.boundingBoxPointsCoords)

    def loadRubberbandsFromAnnotationList(self):
        for annotation in self.annotationList:
            self.createRubberbands(annotation)

    # def deleteAnnotationsWhenClickedInside(self):
    #     pass
    #     # for index, coordsList in self.annotationList.iteritems():
    #     #     top_left_x = coordsList[0][0]
    #     #     top_left_y = coordsList[0][1]
    #     #     bottom_right_x = coordsList[3][0]
    #     #     bottom_right_y = coordsList[3][1]
    #     #     self.polygon.reset()
    #     #     if  (top_left_x <= self.point.x() <= bottom_right_x) and
    #     #         (top_left_y >= self.point.y() >= bottom_right_y):



