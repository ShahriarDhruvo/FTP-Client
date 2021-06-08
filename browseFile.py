import sys
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog

WINDOW_WIDTH = 853
WINDOW_HEIGHT = 619

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui.ui", self)
        self.browse.clicked.connect(self.browseFiles)

    def browseFiles(self):
        fname = QFileDialog.getOpenFileName(self, "Select File", "/")
        self.fileLocation.setText(fname[0])

app = QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(WINDOW_WIDTH)
widget.setFixedHeight(WINDOW_HEIGHT)
widget.show()
sys.exit(app.exec_())
