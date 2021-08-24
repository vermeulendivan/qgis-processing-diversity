# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DiversityProcessing
                                 A QGIS plugin
 Diversity processing
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-08-24
        copyright            : (C) 2021 by divan
        email                : vermeulendivan@gmail.com
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

__author__ = 'divan'
__date__ = '2021-08-24'
__copyright__ = '(C) 2021 by divan'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load DiversityProcessing class from file DiversityProcessing.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .diversity_processing import DiversityProcessingPlugin
    return DiversityProcessingPlugin()
