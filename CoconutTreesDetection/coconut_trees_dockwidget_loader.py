# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ActiveClassificationDialog
                                 A QGIS plugin
 Active classification description
                             -------------------
        begin                : 2014-05-28
        copyright            : (C) 2014 by John Edgar Vargas
        email                : jvargasmu@gmail.com
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

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *
from coconut_trees_detection_dockwidget_base import Ui_DockWidget


class DockWidget(QDockWidget):
	def __init__(self, parent, iface):
		QDockWidget.__init__(self)
		
		# initialize plugin directory
		self.plgnDir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/CoconutTreesDetection"
		# locale name
		self.lclNm = QSettings().value("locale/userLocale")[0:2] 
		# path to locale
		lclPth = "" 
		if QFileInfo(self.plgnDir).exists(): 
			lclPth = self.plgnDir + "/i18n/coconuttreesdetection_" + self.lclNm + ".qm" 
		if QFileInfo(lclPth).exists(): 
			self.trnsltr = QTranslator() 
			self.trnsltr.load(lclPth) 
			if qVersion() > '4.3.3': 
				QCoreApplication.installTranslator(self.trnsltr)
		
		self.ui = Ui_DockWidget()
		self.ui.setupUi(self)
