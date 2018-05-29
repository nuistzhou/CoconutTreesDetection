# Import Qt modules
from qgis.core import *
from qgis.gui import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from PyQt4 import QtCore,QtGui, QtOpenGL
from PyQt4 import QtCore,QtGui,QtOpenGL

import argparse
import os,sys,time
import math
import numpy as np
# Import the compiled UI module
from ui_visualization import Ui_Visualization
from tools import getTSNEFeatures

from config import Parameters
from functools import partial

import matplotlib.pyplot as plt


class Node(QtGui.QGraphicsItem):

    def __init__(self, app, graphWidget, node_id, cluster_label=None, label=None, fullpath=None, table_widget=None):
        super(Node, self).__init__()
        self.app = app
        self.graph = graphWidget
        self.table_widget = table_widget

        self.node_id = node_id
        self.cluster_label = cluster_label
        self.label = label
        self.fullpath = fullpath
        self.color_rgb = [0, 0, 255]

        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QtGui.QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(2)

    def get_cluster_label(self):
        return self.cluster_label

    def set_cluster_label(self, cluster_label):
        self.cluster_label = cluster_label

    def get_label(self):
        return self.label

    def set_label(self, label):
        self.label = label

    def get_fullpath(self):
        return self.fullpath

    def set_fullpath(self, fullpath):
        self.fullpath = fullpath

    def set_color_rgb(self, color_rgb):
        self.color_rgb = color_rgb

    def update_color(self, color_rgb):
        self.color_rgb = color_rgb
        self.update()

    def boundingRect(self):
        adjust = 2.0
        return QtCore.QRectF(-10 - adjust, -10 - adjust, 23 + adjust,
                             23 + adjust)

    def shape(self):
        path = QtGui.QPainterPath()
        # path.addEllipse(-1, -1, 4, 4)
        path.addEllipse(0, 0, 4, 4)
        return path

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(self.color_rgb[0], self.color_rgb[1], self.color_rgb[2]))
        painter.drawEllipse(0, 0, 4, 4)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
        painter.drawEllipse(0, 0, 4, 4)

    def mousePressEvent(self, event):
        super(Node, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        # self.update()
        super(Node, self).mouseReleaseEvent(event)
        print "ID Node {} fullpath {}".format(self.node_id, self.fullpath)


class GraphWidget(QtGui.QGraphicsView):
    def __init__(self, app, parent, main_window):
        super(GraphWidget, self).__init__(parent)
        self.main_window = main_window
        self.app = app

        self.scene = QtGui.QGraphicsScene(self)
        self.scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)

        self.setScene(self.scene)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        # self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        # self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.scale(1.0, 1.0)
        self.setDragMode(QGraphicsView.RubberBandDrag)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin_selector = QPoint()
        self.end_selector = QPoint()

    def wheelEvent(self, event):
        # self.scaleView(math.pow(2.0, -event.delta() / 240.0))
        # self.scaleView(math.pow(2.0, event.delta() / 240.0)) # current
        # pass
        """
        Zoom in or out of the view.
        """

        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        self.setTransformationAnchor(QtGui.QGraphicsView.NoAnchor)
        self.setResizeAnchor(QtGui.QGraphicsView.NoAnchor)

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Zoom
        if event.delta() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.scale(zoomFactor, zoomFactor)

        # Get the new position
        newPos = self.mapToScene(event.pos())

        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())

    def drawBackground(self, painter, rect):
        # Shadow.
        sceneRect = self.sceneRect()
        rightShadow = QtCore.QRectF(sceneRect.right(), sceneRect.top() + 5, 5,
                                    sceneRect.height())
        bottomShadow = QtCore.QRectF(sceneRect.left() + 5, sceneRect.bottom(),
                                     sceneRect.width(), 5)
        if rightShadow.intersects(rect) or rightShadow.contains(rect):
            painter.fillRect(rightShadow, QtCore.Qt.darkGray)
        if bottomShadow.intersects(rect) or bottomShadow.contains(rect):
            painter.fillRect(bottomShadow, QtCore.Qt.darkGray)

        # Fill.
        gradient = QtGui.QLinearGradient(sceneRect.topLeft(),
                                         sceneRect.bottomRight())
        gradient.setColorAt(0, QtCore.Qt.white)
        gradient.setColorAt(1, QtCore.Qt.lightGray)
        painter.fillRect(rect.intersect(sceneRect), QtGui.QBrush(gradient))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRect(sceneRect)

    def scaleView(self, scaleFactor):
        print scaleFactor
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.origin_selector = QPoint(event.pos())
            self.rubberBand.setGeometry(QRect(self.origin_selector, QSize()))
            self.rubberBand.show()

    def mouseMoveEvent(self, event):

        if not self.origin_selector.isNull():
            self.rubberBand.setGeometry(QRect(self.origin_selector, event.pos()).normalized())

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.rubberBand.hide()
            self.end_selector = QPoint(event.pos())
            self.main_window.showWidgets(self.origin_selector, self.end_selector)


class Visualization(QtGui.QDialog, Ui_Visualization):
    def __init__(self, config):
        # QtGui.QDialog.__init__(self)
        super(Visualization, self).__init__(None)
        self.config = config
        self.setupUi(self)
        self.graphicsViewProjection.setStyleSheet("border: 1px solid black")
        self.graphicsViewProjection.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.graphicsViewProjection.setInteractive(True)
        # Initialize components
        self.graph_widget = GraphWidget(self.config, self.graphicsViewProjection, self)
        self.graph_widget.setDragMode(QtGui.QGraphicsView.RubberBandDrag)

        self.default_img_size = 256
        self.default_thumb_img_size = 256  # 192

        # Origin and end selection points
        self.origin_selector = QPoint()
        self.end_selector = QPoint()

        # set other attribute values
        self.node_list = []
        self.selected_nodes = []
        self.selected_node_for_annotation = None

        self.default_node_color = [0, 0, 255]
        self.selected_node_color = [255,255,0]  # [255, 255, 0]
        self.name_classes = ["Impervious", "Building", "Low vegetation", "Tree", "Car", "Background"]
        # setup image editor
        self.editor_layers = []
        self.current_labeled_nodes = []  # list of indexes in the list of selected nodes
        self.superpixel_index_rubber_band = []
        self.temp_rubber_band = None
        self.transparent_color = QColor(0, 0, 0, 0)
        # self.default_color = QColor(255, 0, 0, 50)
        self.default_color = QColor(0, 255, 0, 50)
        self.color_array = ["#ffffff", "#0000ff"]
        self.color_array_decimal = [[0, 0, 255], [255, 0, 0]]
        # superpixel variables
        self.coarse_sups_centers = None
        self.coarse_sups = None
        self.coarse_sups_idxs = None
        self.sup_polygons = None
        self.classification_map = None

    def getGraphWidget(self):
        return self.graph_widget


    def clear_temporal_rubber_band(self):
        if self.temp_rubber_band is not None:
            self.temp_rubber_band.reset(QGis.Polygon)
        self.temp_rubber_band = None


    def updateNodes(self, points, cluster_labels=None, labels=None, fullpaths=None, coarse_sups=None,
                    coarse_sups_centers=None,
                    coarse_sups_idxs=None, sup_polygons=None, classification_map=None, confidence_map=None):

        # node_features = [[-50, -50], [0, -50], [50, -50], [-50, 0], [0,0], [50, 0], [-50, 50], [0, 50], [50, 50]]
        # add nodes to the canvas
        self.points = points
        self.cluster_labels = cluster_labels
        self.labels = labels
        self.fullpaths = fullpaths
        self.coarse_sups = coarse_sups
        self.coarse_sups_centers = coarse_sups_centers
        self.coarse_sups_idxs = coarse_sups_idxs
        self.sup_polygons = sup_polygons
        self.num_nodes = len(points)
        self.node_list = []
        self.selected_nodes = []
        for i in range(self.num_nodes):

            node = Node(self.config, self, i)
            if cluster_labels is not None:
                node.set_cluster_label(cluster_labels[i])

            if self.labels is not None:
                node.set_label(self.labels[i])
                # if classification_map is not None:
                node.set_color_rgb(self.color_array_decimal[self.labels[i]])

            if fullpaths is not None:
                node.set_fullpath(fullpaths[i])

            self.node_list.append(node)

        for i in range(self.num_nodes):
            self.graph_widget.scene.addItem(self.node_list[i])

        for i in range(self.num_nodes):
            node = self.node_list[i]
            node.setPos(self.points[i, 0], self.points[i, 1])

        self.setWindowTitle("Nodes")
        # set Scene bounding box
        margin_bbox = 100
        x_min = np.min(self.points[:, 0]) - margin_bbox
        y_min = np.min(self.points[:, 1]) - margin_bbox
        x_max = np.max(self.points[:, 0]) + margin_bbox
        y_max = np.max(self.points[:, 1]) + margin_bbox
        width_bbox = x_max - x_min
        height_bbox = y_max - y_min
        self.graph_widget.setSceneRect(x_min, y_min, width_bbox, height_bbox)
        self.graph_widget.setMinimumSize(width_bbox, height_bbox)

    def showWidgets(self, origin_selector, end_selector):
        self.origin_selector = origin_selector
        self.end_selector = end_selector
        print "origin selector x, y: {}, {}".format(self.origin_selector.x(), self.origin_selector.y())
        print "end selector x, y: {}, {}".format(self.end_selector.x(), self.end_selector.y())
        # get list of selected widgets
        origin_selector_loc = self.graph_widget.mapToScene(self.origin_selector)
        end_selector_loc = self.graph_widget.mapToScene(self.end_selector)

        print "origin_selector_loc x, y: {}, {}".format(origin_selector_loc.x(), origin_selector_loc.y())
        print "end_selector_loc x, y: {}, {}".format(end_selector_loc.x(), end_selector_loc.y())

        new_selected_nodes = []
        for i in range(len(self.points)):
            point = self.points[i]
            if point[0] >= origin_selector_loc.x() and point[0] <= end_selector_loc.x() and point[
                1] >= origin_selector_loc.y() and point[1] <= end_selector_loc.y():
                new_selected_nodes.append(i)

        # unselect previous selected nodes
        for i in range(len(self.selected_nodes)):
            index_node = self.selected_nodes[i]
            if self.labels is not None:
                self.node_list[index_node].update_color(self.color_array_decimal[self.labels[index_node] - 1])
            else:
                self.node_list[index_node].update_color(self.default_node_color)

        # show new selected nodes with different color
        self.selected_nodes = new_selected_nodes
        for i in range(len(self.selected_nodes)):
            index_node = self.selected_nodes[i]
            self.node_list[index_node].update_color(self.selected_node_color)

        # show widgets
        numSelectedSamples = len(self.selected_nodes)
        print "numSelectedSamples {}".format(numSelectedSamples)
        print "verticalHeader ok"
        projection_name_classes = ["None"]
        for i in range(len(self.name_classes)):
            projection_name_classes.append(self.name_classes[i])

        # clear labeled nodes
        self.current_labeled_nodes = []


