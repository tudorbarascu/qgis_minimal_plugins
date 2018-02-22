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

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *
from qgis.core import QgsDataSourceUri, QgsVectorLayer


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
            print("failed to load buildings!")
            QMessageBox.error(None, "Plugin minimal 02", "failed to load buildings!")

        count = 0

        for entitate in vl.getFeatures():
            count += 1

        QMessageBox.information(None, "Plugin minimal 02", "No. of buildings: " + str(count))
