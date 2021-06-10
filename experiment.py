import os
import time
import socket
import sys
import threading
from constants import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (QDialog, QApplication, QFileDialog, 
                             QLabel, QPushButton, QGridLayout)

#### experiment

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("ng.ui", self)
        #button 
        self.startServer.clicked.connect(self.startServer_fun)

        # ScrollArea Lauout
        self.fileListLayout = QGridLayout()
        self.fileListLayout.setAlignment(Qt.AlignTop)
        self.fileListLayout.setVerticalSpacing(15)
        self.scrollArea.setLayout(self.fileListLayout)

    def startServer_fun(self):
        self.statusBox.setText("Server Started")
        os.system('python server.py')

app = QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(WINDOW_WIDTH)
widget.setFixedHeight(WINDOW_HEIGHT)
widget.show()
sys.exit(app.exec_())
