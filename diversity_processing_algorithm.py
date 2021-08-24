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
"""

__author__ = 'divan'
__date__ = '2021-08-24'
__copyright__ = '(C) 2021 by divan'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingOutputString)

from .diversity_functions import *

class DiversityProcessingAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    POLYLAYER = "POLYLAYER"
    CATEGORYFIELD = "CATEGORYFIELD"
    POINTLAYER = "POINTLAYER"
    SPECIESFIELD = "SPECIESFIELD"
    
    SUMMARY_DICTIONARY = "SUMMARY_DICTIONARY"
    SUMMARY_HTML = "SUMMARY_HTML"

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.POLYLAYER,
                self.tr('Polygon layer'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )

        # We add a feature field.
        self.addParameter(
            QgsProcessingParameterField(
                self.CATEGORYFIELD,
                self.tr('Category field'),
                None,
                self.POLYLAYER,
                QgsProcessingParameterField.String
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.POINTLAYER,
                self.tr('Point layer'),
                [QgsProcessing.TypeVectorPoint]
            )
        )

        # We add a feature field.
        self.addParameter(
            QgsProcessingParameterField(
                self.SPECIESFIELD,
                self.tr('Species field'),
                None,
                self.POINTLAYER,
                QgsProcessingParameterField.String
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.SUMMARY_HTML,
                self.tr("Output HTML file"),
                'HTML Files (*.html)'
            )
        )
        
        self.addOutput(
            QgsProcessingOutputString(
                self.SUMMARY_DICTIONARY,
                self.tr("Results (string)")
            )
        )
        

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        lyrPoly = self.parameterAsSource(parameters, self.POLYLAYER, context)
        lyrPoint = self.parameterAsSource(parameters, self.POINTLAYER, context)
        
        fldCategory = self.parameterAsString(parameters, self.CATEGORYFIELD, context)
        fldSpecies = self.parameterAsString(parameters, self.SPECIESFIELD, context)

        outFile = self.parameterAsFileOutput(parameters, self.SUMMARY_HTML, context)

        total = lyrPoly.featureCount()
        current = 0

        dctMain = {}
        for poly in lyrPoly.getFeatures():
            if feedback.isCanceled():
                feedback.push.pushInfo("Operation cancelled by user")
                break
            
            sCategory = poly.attribute(fldCategory)
            feedback.pushInfo("Category: {}".format(sCategory))
                
            dctSummary = dc_summarizePoly(poly, lyrPoint, fldSpecies)
            feedback.pushDebugInfo("Summary: {}".format(dctSummary))
                
            dctMain = dc_mergeDictionaries(dctMain, sCategory, dctSummary)
            
            current += 1
            feedback.setProgress((current/total)*100)
            feedback.setProgressText("Currently on polygon {} out of {}".format(current, total))
        
        feedback.pushInfo(str(dctMain))
        
        if not feedback.isCanceled():
            f = open(outFile, "w")
            f.write(dc_resultHTML(dctMain, lyrPoly.sourceName(), fldCategory))
            f.close()
        
        return {self.SUMMARY_DICTIONARY: str(dctMain),
                self.SUMMARY_HTML: outFile}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Diversity Calculator'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Diversity'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return DiversityProcessingAlgorithm()

    def helpUrl(self):
        return "https://github.com/vermeulendivan/qgis-processing-diversity"
    
    def shortHelpString(self):
        str = """
        Calculates species diversity
        """

    def shortDescription(self):
        return "Calculates species diversity"

    def icon(self):
        return QIcon("icon.png")

















