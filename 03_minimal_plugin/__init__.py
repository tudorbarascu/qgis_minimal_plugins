# encoding: utf-8
#-----------------------------------------------------------
# Copyright (C) 2018 Tudor Bărăscu
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------

from qgis.PyQt.QtWidgets import *
from qgis.core import QgsDataSourceUri, QgsVectorLayer, Qgis


def classFactory(iface):
    return MinimalPlugin(iface)


class MinimalPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction('Execute action!', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        uri = QgsDataSourceUri()
        uri.setConnection("localhost", "5432", "tutorial", "postgres", "any_password")
        uri.setDataSource("topo", "buildings", "geom")

        vl = QgsVectorLayer(uri.uri(), "buildings", "postgres")

        if not vl.isValid():
            self.iface.messageBar().pushMessage("Error", "failed to load buildings",
                                                Qgis.Critical, duration=5)

        else:
            large_footprint_buildings = 0

            for feature in vl.getFeatures():
                if feature.geometry().area() >= 200:
                    large_footprint_buildings += 1

            self.iface.messageBar().pushMessage("The no. of buildings with a footprint of at least 200 sq meters is",
                                                str(large_footprint_buildings), Qgis.Info, duration=5)
