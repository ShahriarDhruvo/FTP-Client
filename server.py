import os
import sys
import time
import threading
from PyQt5.QtCore import QThread, pyqtSignal, Qt
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
        loadUi("serverGUI.ui", self)

        # Default Address
        self.ipField.setText(socket.gethostbyname(socket.gethostname()))
        self.portField.setText(f"{PORT}")

        # Some Action Buttons
        self.startServerButton.clicked.connect(self.startServer)
        self.stopServerButton.clicked.connect(self.stopServer)

        # Application Status
        self.status_text = ""

        # ScrollArea Layout
        self.fileListLayout = QGridLayout()
        self.fileListLayout.setAlignment(Qt.AlignTop)
        self.fileListLayout.setVerticalSpacing(15)
        self.scrollArea.setLayout(self.fileListLayout)

        # Initial Connect by default address
        self.startServer()

    def stopServer(self):
        self.handleStatus("[STOP]: The server has been stopped")
        self.server.close()

    # Status handler
    def handleStatus(self, text):
        if text:
            self.status_text += str(text) + "\n"
            self.statusBox.setText(self.status_text)

            print(text)

    def listFiles(self):
        # Clear all the widgets from the scrollArea
        for i in reversed(range(self.fileListLayout.count())):
            self.fileListLayout.itemAt(i).widget().setParent(None)

        files = os.listdir(SERVER_DATA_PATH)

        if len(files) == 0:
            self.filesLayout(0, "", True)
        else:
            data = next(os.walk(SERVER_DATA_PATH), (None, None, []))[2]

            for i in range(len(data)):
                self.filesLayout(i, data[i])

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
            deleteButton = QPushButton("Delete", self)
            deleteButton.setStyleSheet("background-color: #d9534f; color: white")

            deleteButton.clicked.connect(lambda: self.deleteFile(fileName))

            self.fileListLayout.addWidget(fileNameLabel, index, 0, 1, 4)
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

    def deleteFile(self, fileName):
        files = os.listdir(SERVER_DATA_PATH)
        status = ""

        if fileName in files:
            os.remove(f"{SERVER_DATA_PATH}/{fileName}")
            status += "File deleted successfully"
        else:
            status += "File not found"

        self.handleStatus(status)
        self.listFiles()

    # Starting Server Connection
    def startServer(self):
        try:
            self.handleStatus("[STARTING]: Server is starting")
            self.clientCount.setText(str(0))

            IP = self.ipField.text()
            PORT = int(self.portField.text())

            ADDR = (IP, PORT)

            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(ADDR)
            self.server.listen()

            self.handleStatus(f"[LISTENING]: Server is listening on {IP} : {PORT}")

            connectionThread = threading.Thread(target=self.checkConnection)
            connectionThread.start()

            self.listFiles()

        except socket.error as error:
            self.handleStatus(error)

    def checkConnection(self):
        while True:
            status = ""

            try:
                conn, addr = self.server.accept()

                clientThread = threading.Thread(
                    target=self.handleClient, args=(conn, addr)
                )
                clientThread.start()

                self.clientCount.setText(str(threading.activeCount() - 2))

            except socket.error as error:
                status = str(error)

            except:
                status = "[Error]: Unknown connection error, try again..."

            # if status:
            #     # So that we can call parent thread's handleStatus function from a child thread
            #     self.statusThread = StatusThread(status)
            #     self.statusThread.update_status.connect(self.handleStatus)
            #     self.statusThread.start()

    def handleClient(self, conn, addr):
        status = f"[NEW CONNECTION]: {addr} connected"

        conn.send("OK@Welcome to the File Server".encode(FORMAT))

        while True:
            data = conn.recv(SIZE).decode(FORMAT)

            data = data.split("@")
            cmd = data[0]

            if cmd == "LIST":
                files = os.listdir(SERVER_DATA_PATH)
                send_data = "OK@"

                if len(files) == 0:
                    send_data = "NULL@The server directory is empty"
                else:
                    send_data += "\n".join(f for f in files)
                conn.send(send_data.encode(FORMAT))

            elif cmd == "UPLOAD":
                name = data[1]

                files = os.listdir(SERVER_DATA_PATH)
                name = (
                    name.split(".")[0]
                    + "_("
                    + str(len(files))
                    + ")."
                    + name.split(".")[1]
                )

                filepath = os.path.join(SERVER_DATA_PATH, name)
                filesize = int(data[2])

                with open(filepath, "wb") as f:
                    start_time = time.time()

                    data = conn.recv(SIZE)
                    totalRecv = len(data)
                    f.write(data)

                    while totalRecv < filesize:
                        data = conn.recv(SIZE)
                        totalRecv += len(data)
                        f.write(data)
                        # print("{0:.2f}".format((totalRecv/float(filesize))
                        # *100)+"% DONE")

                    end_time = time.time()

                status += (
                    "File DOWNLOAD Complete. Transfer time: "
                    + "{:.2f}".format(end_time - start_time)
                    + "s"
                )

            elif cmd == "DOWNLOAD":
                name, fileSize, path = data[1], data[2], data[3]
                filePath = os.path.join(path, name)
                fileSize = int(data[2])

                with open(filePath, "wb") as f:
                    start_time = time.time()

                    data = conn.recv(SIZE)
                    totalRecv = len(data)
                    f.write(data)

                    while totalRecv < fileSize:
                        data = conn.recv(SIZE)
                        totalRecv += len(data)
                        f.write(data)
                        # print("{0:.2f}".format((totalRecv/float(filesize))
                        # *100)+"% DONE")

                    end_time = time.time()

                status += (
                    "File UPLOAD Complete. Transfer time: "
                    + "{:.2f}".format(end_time - start_time)
                    + "s"
                )

            elif cmd == "DELETE":
                files = os.listdir(SERVER_DATA_PATH)
                send_data = "OK@"
                filename = data[1]

                if filename in files:
                    os.remove(f"{SERVER_DATA_PATH}/{filename}")
                    send_data += "File deleted successfully"
                else:
                    send_data += "File not found"

                conn.send(send_data.encode(FORMAT))

                status += f"{filename} has been deleted"

            elif cmd == "FINISHED":
                thread = UpdateThread()
                thread.update.connect(self.listFiles)
                thread.start()

            elif cmd == "LOGOUT":
                break

            elif cmd == "HELP":
                data = "OK@"
                data += "LIST: List all the files from the server.\n"
                data += "UPLOAD <path>: Upload a file to the server.\n"
                data += "DELETE <filename>: Delete a file from the server.\n"
                data += "LOGOUT: Disconnect from the server.\n"
                data += "HELP: List all the commands."

                conn.send(data.encode(FORMAT))

            if status:
                self.statusThread = UpdateThread(status, self)
                self.statusThread.update.connect(self.handleStatus)
                self.statusThread.start()

                status = ""

        # self.statusThread = StatusThread(f"[DISCONNECTED]: {addr} disconnected")
        # self.statusThread.update_status.connect(self.handleStatus)
        # self.statusThread.start()

        conn.close()


class UpdateThread(QThread):
    update = pyqtSignal(str)

    def __init__(self, status="", parent=None):
        QThread.__init__(self, parent)
        self.status = status

    def run(self):
        self.update.emit(self.status)


app = QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(WINDOW_WIDTH)
widget.setFixedHeight(WINDOW_HEIGHT)
widget.show()
sys.exit(app.exec_())
