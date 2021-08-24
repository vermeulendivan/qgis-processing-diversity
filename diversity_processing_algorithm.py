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

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        source = self.parameterAsSource(parameters, self.INPUT, context)
        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT,
                context, source.fields(), source.wkbType(), source.sourceCrs())

        # Compute the number of steps to display within the progress bar and
        # get features from source
        total = 100.0 / source.featureCount() if source.featureCount() else 0
        features = source.getFeatures()

        for current, feature in enumerate(features):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break

            # Add a feature in the sink
            sink.addFeature(feature, QgsFeatureSink.FastInsert)

            # Update the progress bar
            feedback.setProgress(int(current * total))

        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {self.OUTPUT: dest_id}

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

















