import os
import sys
import time
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
        fileNameLabel.setAlignment(Qt.AlignCenter)
        fileNameLabel.setStyleSheet("QLabel"
                            "{"
                            "border: 1px hidden grey;"
                            "border-radius: 2px;"
                            "background-color: lightgrey;"
                            "}")
        
        # Action Buttons                                
        downloadButton = QPushButton('Download', self)
        downloadButton.setStyleSheet("background-color: #8081e8")

        downloadButton.clicked.connect(lambda: self.downloadFile(fileName))

        deleteButton = QPushButton('Delete', self)
        deleteButton.setStyleSheet("background-color: #ed727d")

        deleteButton.clicked.connect(lambda: self.deleteFile(fileName))

        self.fileListLayout.addWidget(fileNameLabel, index, 0, 1, 3)
        self.fileListLayout.addWidget(downloadButton, index, 4)
        self.fileListLayout.addWidget(deleteButton, index, 5)

    # Show Server Files
    def listFiles(self):
        self.client.send("LIST".encode(FORMAT))
        data = self.client.recv(SIZE).decode(FORMAT)
        data = data.split("@")

        if(data[0] != "NULL"):
            data = data[1].split("\n")

            for i in range(len(data)):
                self.filesLayout(i, data[i])
        else:
            self.statusBox.setText(f"[{data[0]}]: " + data[1])
    ###############################################################    
    def uploadFile(self):
        path = self.fileLocation.text()

        if not path:
            self.statusBox.setText("[NULL]: Select a file directory first")
        else:
            filename = path.split("/")[-1]
            filesize = str(os.path.getsize(path))

            send_data = f"UPLOAD@{filename}@{filesize}"
            self.client.send(send_data.encode(FORMAT))
            
            with open(f"{path}", "rb") as f:
                start_time = time.time()

                bytesToSend = f.read(SIZE)
                self.client.send(bytesToSend)
                while len(bytesToSend) !=0:
                    bytesToSend = f.read(SIZE)
                    self.client.send(bytesToSend)
                
                end_time = time.time()

            self.statusBox.setText("File transfer Complete. Transfer time: " + "{:.2f}".format(end_time - start_time) + "s")
            self.fileLocation.setText(None)
            # self.listFiles()
    
    def downloadFile(self, fileName):
        downloadLocation = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        path = f"server_data/{fileName}"

        with open(f"{path}", "rb") as f:
            text = f.read()

        filename = path.split("/")[-1]
        send_data = f"DOWNLOAD@{filename}@{text}@{downloadLocation}"
        self.client.send(send_data.encode(FORMAT))
    ###############################################################
    
    def update(self):
        data = self.client.recv(SIZE).decode(FORMAT).split("@")
        self.statusBox.setText(f"[{data[0]}]: {data[1]}")
        self.listFiles()

    def deleteFile(self, fileName):
        self.client.send(f"DELETE@{fileName}".encode(FORMAT))

        # self.update()
        
app = QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(WINDOW_WIDTH)
widget.setFixedHeight(WINDOW_HEIGHT)
widget.show()
sys.exit(app.exec_())
