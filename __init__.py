# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CoconutTreesDetection
                                 A QGIS plugin
 Application to annotate coconut trees in aerial imagery and do the detection
                             -------------------
        begin                : 2018-03-07
        copyright            : (C) 2018 by Ping Zhou
        email                : nuistzhou@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load CoconutTreesDetection class from filePickle CoconutTreesDetection.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .coconut_trees_detection import CoconutTreesDetection
    return CoconutTreesDetection(iface)
