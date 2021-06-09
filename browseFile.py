import sys
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (QDialog, QApplication, QFileDialog, 
                             QLabel, QPushButton, QGridLayout)

from constants import *
# from client import *

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui.ui", self)

        # Default Address
        self.ipField.setText(socket.gethostbyname(socket.gethostname()))
        self.portField.setText("4456")

        self.browse.clicked.connect(self.browseFiles)
        self.connect.clicked.connect(self.connectClient)
        self.upload.clicked.connect(self.uploadFile)

        self.fileListLayout = QGridLayout()
        self.scrollArea.setLayout(self.fileListLayout)
        
        # Initial Connect
        self.connectClient()

    def connectClient(self):
        # Server Connection
        try:
            IP = self.ipField.text()
            PORT = int(self.portField.text())

            ADDR = (IP, PORT)

            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(ADDR)

            data = self.client.recv(SIZE).decode(FORMAT)
            cmd, msg = data.split("@")

            if cmd == "DISCONNECTED":
                # self.statusBox.setText(f"[SERVER]: {msg}\n" +
                # "[DISCONNECTED]: Disconnected from the server")
                self.client.close()
            elif cmd == "OK":
                self.statusBox.setText(f"[SUCCESS]: {msg}")
            
            self.listFiles()
            
        except socket.error as error:
            self.statusBox.setText(f"{error}")
        except:
            self.statusBox.setText(f"[ERROR]: Invalid Address")

    def browseFiles(self):
        fname = QFileDialog.getOpenFileName(self, "Select File", "/")
        self.fileLocation.setText(fname[0])

    def filesLayout(self, index, fileName):
        fileNameLabel = QLabel(" " + fileName, self)
            
        # x_position = 30
        # y_position = 180
        # label_width = 581
        # label_height = 33

        # fileNameLabel.setGeometry(x_position, y_position+(i*50), label_width, label_height)
        fileNameLabel.setAlignment(Qt.AlignCenter)
        
        fileNameLabel.setStyleSheet("QLabel"
                            "{"
                            "border: 2px hidden grey;"
                            "border-radius: 2px;"
                            "background-color: lightgrey;"
                            "}")
        
        # Action Buttons                                
        # button_width = 95
        # button_height = 34

        downloadButton = QPushButton('Download', self)
        # downloadButton.setGeometry(x_position + 600, y_position+(i*50), button_width, button_height)
        downloadButton.setStyleSheet("background-color: #8081e8")

        deleteButton = QPushButton('Delete', self)
        # deleteButton.setGeometry(x_position + 700, y_position+(i*50), button_width, button_height)
        deleteButton.setStyleSheet("background-color: #ed727d")

        deleteButton.clicked.connect(lambda: self.deleteFile(fileName))

        self.fileListLayout.addWidget(fileNameLabel, index, 0, 1, 3)
        self.fileListLayout.addWidget(downloadButton, index, 4)
        self.fileListLayout.addWidget(deleteButton, index, 5)

    def listFiles(self):
        # Show Server Files
        self.client.send("LIST".encode(FORMAT))
        data = self.client.recv(SIZE).decode(FORMAT)
        data = data.split("@")

        data = data[1].split("\n")

        for i in range(len(data)):
            self.filesLayout(i, data[i])
    
    def uploadFile(self):
        path = self.fileLocation.text()

        with open(f"{path}", "r") as f:
            text = f.read()

        filename = path.split("/")[-1]
        send_data = f"UPLOAD@{filename}@{text}"
        self.client.send(send_data.encode(FORMAT))
        
        self.update()
    
    def update(self):
        data = self.client.recv(SIZE).decode(FORMAT).split("@")
        self.statusBox.setText(f"[{data[0]}]: {data[1]}")
        self.listFiles()

    def deleteFile(self, fileName):
        self.client.send(f"DELETE@{fileName}".encode(FORMAT))

        self.update()

app = QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(WINDOW_WIDTH)
widget.setFixedHeight(WINDOW_HEIGHT)
widget.show()
sys.exit(app.exec_())
