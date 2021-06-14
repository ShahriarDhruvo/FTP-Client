import os
import sys
import time
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
    QDialog,
    QApplication,
    QFileDialog,
    QLabel,
    QPushButton,
    QGridLayout,
)

from constants import *


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("clientGUI.ui", self)

        # Default Address
        # socket.gethostbyname(socket.gethostname())
        # f"{PORT}"
        self.ipField.setText("")
        self.portField.setText("")

        # Some Action Buttons
        self.browse.clicked.connect(self.browseFiles)
        self.connect.clicked.connect(self.connectClient)
        self.upload.clicked.connect(self.uploadFile)
        self.logout.clicked.connect(self.logout_fun)

        # ScrollArea Layout
        self.fileListLayout = QGridLayout()
        self.fileListLayout.setAlignment(Qt.AlignTop)
        self.fileListLayout.setVerticalSpacing(15)
        self.scrollArea.setLayout(self.fileListLayout)

        # Initial Connect by default address
        #self.connectClient()

    # Server Connection
    def connectClient(self):
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

    # Handle browse button functionality
    def browseFiles(self):
        fname = QFileDialog.getOpenFileName(self, "Select File", "/")
        self.fileLocation.setText(fname[0])

    # Handle file style and create download delete buttons
    def filesLayout(self, index, fileName, empty=False):
        if not empty:
            fileNameLabel = QLabel(fileName, self)
            fileNameLabel.setAlignment(Qt.AlignCenter)
            fileNameLabel.setStyleSheet(
                "QLabel"
                "{"
                "border: 1px hidden grey;"
                "border-radius: 2px;"
                "background-color: lightgrey;"
                "}"
            )

            # Action Buttons
            downloadButton = QPushButton("Download", self)
            downloadButton.setStyleSheet("background-color: #5bc0de; color: white")

            downloadButton.clicked.connect(lambda: self.downloadFile(fileName))

            deleteButton = QPushButton("Delete", self)
            deleteButton.setStyleSheet("background-color: #d9534f; color: white")

            deleteButton.clicked.connect(lambda: self.deleteFile(fileName))

            self.fileListLayout.addWidget(fileNameLabel, index, 0, 1, 3)
            self.fileListLayout.addWidget(downloadButton, index, 4)
            self.fileListLayout.addWidget(deleteButton, index, 5)
        else:
            fileNameLabel = QLabel("The server directory is empty", self)
            fileNameLabel.setAlignment(Qt.AlignCenter)
            fileNameLabel.setFixedHeight(40)
            fileNameLabel.setStyleSheet(
                "QLabel"
                "{"
                "border: 1px hidden grey;"
                "border-radius: 2px;"
                "background-color: lightgrey;"
                "}"
            )

            self.fileListLayout.addWidget(fileNameLabel, 0, 1)

    # Show Server Files
    def listFiles(self):
        self.client.send("LIST".encode(FORMAT))
        data = self.client.recv(SIZE).decode(FORMAT)
        data = data.split("@")

        # Clear all the widgets from the scrollArea if server send any updated list
        if data:
            for i in reversed(range(self.fileListLayout.count())):
                self.fileListLayout.itemAt(i).widget().setParent(None)

        if data[0] != "NULL":
            data = data[1].split("\n")

            for i in range(len(data)):
                self.filesLayout(i, data[i])
        else:
            self.filesLayout(0, "", True)
        
        # To Refresh server side's file list
        self.client.send("FINISHED".encode(FORMAT))

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

                while len(bytesToSend) != 0:
                    bytesToSend = f.read(SIZE)
                    self.client.send(bytesToSend)

                end_time = time.time()

            self.statusBox.setText(
                "File UPLOAD Complete. Transfer time: "
                + "{:.2f}".format(end_time - start_time)
                + "s"
            )
            self.fileLocation.setText(None)

            time.sleep(WAIT_TIME)
            self.listFiles()

    def downloadFile(self, fileName):
        downloadLocation = str(
            QFileDialog.getExistingDirectory(self, "Select Directory")
        )

        path = f"server_data/{fileName}"

        fileSize = str(os.path.getsize(path))

        send_data = f"DOWNLOAD@{fileName}@{fileSize}@{downloadLocation}"
        self.client.send(send_data.encode(FORMAT))

        with open(path, "rb") as f:
            start_time = time.time()

            bytesToSend = f.read(SIZE)
            self.client.send(bytesToSend)

            while len(bytesToSend) != 0:
                bytesToSend = f.read(SIZE)
                self.client.send(bytesToSend)

            end_time = time.time()

        self.statusBox.setText(
            "File DOWNLOAD Complete. Transfer time: "
            + "{:.2f}".format(end_time - start_time)
            + "s"
        )

    def deleteFile(self, fileName):
        self.client.send(f"DELETE@{fileName}".encode(FORMAT))

        data = self.client.recv(SIZE).decode(FORMAT).split("@")
        self.statusBox.setText(f"[{data[0]}]: {data[1]}")

        time.sleep(WAIT_TIME)
        self.listFiles()
    
    # # new features

    # to clear scroll area
    def emptyList(self):
        for i in reversed(range(self.fileListLayout.count())):
            self.fileListLayout.itemAt(i).widget().setParent(None)

    # this method handles logout functionality
    def logout_fun(self):
        self.client.send("LOGOUT".encode(FORMAT))
        self.ipField.setText("")
        self.portField.setText("")
        print("[DISCONNECTED] Disconnected from the server.")
        self.client.close()
        self.emptyList()
        #sys.exit()

app = QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(WINDOW_WIDTH)
widget.setFixedHeight(WINDOW_HEIGHT)
widget.show()
sys.exit(app.exec_())
