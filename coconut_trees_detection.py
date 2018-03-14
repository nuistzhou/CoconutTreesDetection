# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CoconutTreesDetection
                                 A QGIS plugin
 Application to annotate coconut trees in aerial imagery and do the detection
                              -------------------
        begin                : 2018-03-07
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Ping Zhou
        email                : nuistzhou@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import *
from qgis.core import *

#Import configuration variables
import config


# Initialize Qt resources from file resources.py
import resources

# Import the code for the DockWidget
from coconut_trees_dockwidget_loader import DockWidget
import os.path


class CoconutTreesDetection:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.layer = self.iface.activeLayer()
        self.initConfigFile()
        self.config = config.Config

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        self.dockWidgetAnnotation = DockWidget(self.iface.mainWindow(), self.iface)

        self.uiDockWidgetAnnotation = self.dockWidgetAnnotation.ui


        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CoconutTreesDetection_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&CoconutTreesDetection')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'CoconutTreesDetection')
        self.toolbar.setObjectName(u'CoconutTreesDetection')

        #print "** INITIALIZING CoconutTreesDetection"

        self.pluginIsActive = False
        self.dockwidget = None




    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CoconutTreesDetection', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockWidgetAnnotation)
        icon_path = ':/plugins/CoconutTreesDetection/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'coconutTreesDetection'),
            callback=self.run,
            parent=self.iface.mainWindow())



        self.uiDockWidgetAnnotation.btnLoadAnnotationFile.clicked.connect(self.loadAnnotationFile)

        # Get coordinates of the clicked point
        tool = ClickTool(self.config, self.canvas, self.layer)
        self.iface.mapCanvas().setMapTool(tool)


    def loadAnnotationFile(self):
        QMessageBox.information(self.iface.mainWindow(), "loadAnnotations", "Loading")
        
    def initConfigFile(self):
        config.Config.pixSize = self.layer.rasterUnitsPerPixelX()
        config.Config.topLeftX = self.layer.extent().xMinimum()
        config.Config.topLeftY = self.layer.extent().yMinimum()
      

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING CoconutTreesDetection"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD CoconutTreesDetection"

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&CoconutTreesDetection'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    #--------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""
        self.dockWidgetAnnotation.show()

        """if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING CoconutTreesDetection"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                #self.dockwidget = CoconutTreesDetectionDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()
"""

class ClickTool(QgsMapToolEmitPoint):
    def __init__(self, config, canvas, layer):
        self.config = config  #Application configuration variables
        self.canvas = canvas
        self.layer = layer
        self.point = None
        self.active_editing = False
        QgsMapToolEmitPoint.__init__(self, self.canvas)


    def geoCoord2PixelPosition(self, point):
        if (self.config.pixSize == 1):
            return QgsPoint(int(point.x()), int(point.y()))
        else:
            pixPosX = int(round((point.x() - self.config.topLeftX) / self.config.pixSize))
            pixPosY = int(round((self.config.topLeftY - point.y()) / self.config.pixSize))
            return QgsPoint(self.config.topLeftX + pixPosX * self.config.pixSize, self.config.topLeftY - pixPosY * self.config.pixSize)


    def canvasPressEvent(self, event):
        self.active_editing = True
        if event.button() == Qt.LeftButton:
            self.point = self.toLayerCoordinates(self.layer, event.pos())
            self.point = self.geoCoord2PixelPosition(self.point)
        print self.point.x(), self.point.y()

    def showPolygon(self):

        bounding_points = []
        bounding_points.append(QgsPoint(self.point.x() - self.config.brush_size * self.config.pxlSz,
                                   self.point.y() - (-self.config.brush_size * self.config.pxlSz)))
        bounding_points.append(QgsPoint(self.point.x() + self.config.brush_size * self.config.pxlSz,
                                   self.point.y() - (-self.config.brush_size * self.config.pxlSz)))
        bounding_points.append(QgsPoint(self.point.x() + self.config.brush_size * self.config.pxlSz,
                                   self.point.y() + (-self.config.brush_size * self.config.pxlSz)))
        bounding_points.append(QgsPoint(self.point.x() - self.config.brush_size * self.config.pxlSz,
                                   self.point.y() + (-self.config.brush_size * self.config.pxlSz)))

        tmp_polygon = QgsGeometry.fromPolygon([bounding_points])
        if (self.config.crbands.data[self.index_rb].polygon == None):
            self.config.crbands.data[self.index_rb].polygon = tmp_polygon
        else:
            if self.config.crbands.data[self.index_rb].polygon.intersects(tmp_polygon):
                self.config.crbands.data[self.index_rb].polygon = self.config.crbands.data[self.index_rb].polygon.combine(
                    tmp_polygon)
            else:
                # create new marker if the new tmp_polygon does not have and intersection
                # print "new disjoint marker"
                self.combineIntersectingMarkers()
                self.config.crbands.add_custom_rubber_band(self.cnvs, None, None, self.config.currentClass)
                self.index_rb = self.config.crbands.size() - 1
                self.config.crbands.data[self.index_rb].polygon = tmp_polygon

        self.isEmittingPoint = True

        # print "self.configure.crbands size {}".format(self.configure.crbands.size()) 
        # print "showPolygon index_rb {}".format(self.index_rb)
        self.config.crbands.update_rubber_band(self.index_rb)
