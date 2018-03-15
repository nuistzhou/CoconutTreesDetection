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

        if event.button() == Qt.LeftButton:
            self.point = self.canvas.getCoordinateTransform()
            self.point = self.point.toMapCoordinates(event.pos().x(), event.pos().y())
            self.point = self.geoCoord2PixelPosition(self.point)
            self.pointArray.append((self.poin.x(), self.point.y()))
            print self.point.x(), self.point.y()
            self.showPolygon()

    def canvasDoubleClickEvent(self, QMouseEvent):
        """Try to deactivate the tool after doble clicking on the canvas
        Not finished yet..."""
        self.deactivate()

    def removeRubberband(self):
        """Remove certain rubberband when clicking on in the boundingbox"""
        pass



    def showPolygon(self):
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

        # if (self.config.crbands.data[self.index_rb].polygon == None):
        #     self.config.crbands.data[self.index_rb].polygon = tmp_polygon
        # else:
        #     if self.config.crbands.data[self.index_rb].polygon.intersects(tmp_polygon):
        #         self.config.crbands.data[self.index_rb].polygon = self.config.crbands.data[self.index_rb].polygon.combine(
        #             tmp_polygon)
        #     else:
        #         # create new marker if the new tmp_polygon does not have and intersection
        #         # print "new disjoint marker"
        #         self.combineIntersectingMarkers()
        #         self.config.crbands.add_custom_rubber_band(self.cnvs, None, None, self.config.currentClass)
        #         self.index_rb = self.config.crbands.size() - 1
        #         self.config.crbands.data[self.index_rb].polygon = tmp_polygon
        #
        # self.isEmittingPoint = True
        #
        # # print "self.configure.crbands size {}".format(self.configure.crbands.size())
        # # print "showPolygon index_rb {}".format(self.index_rb)
        # self.config.crbands.update_rubber_band(self.index_rb)