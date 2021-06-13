import os
import time
import socket
import sys
import threading
#from constants import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (QDialog, QApplication, QFileDialog, 
                             QLabel, QPushButton, QGridLayout)

#### experiment
# GUI Window height, width
WINDOW_WIDTH = 853
WINDOW_HEIGHT = 767

# Time to wait to process previous connection
WAIT_TIME = 1

IP = socket.gethostbyname(socket.gethostname())
PORT = 4457

ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"



class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("ng.ui", self)

        # ScrollArea Lauout
        self.fileListLayout = QGridLayout()
        self.fileListLayout.setAlignment(Qt.AlignTop)
        self.fileListLayout.setVerticalSpacing(15)
        self.scrollArea.setLayout(self.fileListLayout)
        
        # Initial Connect by default address
        self.startServer()

    # Server Connection
    def startServer(self):
        try:
            print("[STARTING]: Server is starting")
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(ADDR)
            self.server.listen()
            self.statusBox.setText(f"[LISTENING]: Server is listening on {IP} : {PORT}.")
            print(f"[LISTENING]: Server is listening on {IP}:{PORT}.")

            thread=threading.Thread(target=self.function, args =())
            thread.start()
            
            print(".............|..........")

    
        # except:
        #     print("[ERROR]: Server is not starting")
        #     self.statusBox.setText(f"[ERROR]: Server Couldn't start")
        except socket.error as error:
            print(error)
    
    def function(self):
        while True:
            try:
                conn,addr= self.server.accept()
                conn.send("OK@Tumi amar Baal.".encode(FORMAT))
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.daemon = True
                thread.start()                    
                print(f"[ACTIVE CONNECTIONS]: {threading.activeCount() - 1}")
                # self.subfunction()

            except socket.error as error:
                print(error)
                break

            except:
                print('bal!!!! hoy na ken re vai')
                break

    # def function(self):
    #     try:
    #         conn,addr= self.server.accept()
    #         print(conn,addr)
    #         thread = threading.Thread(target=self.handle_client, args=(conn, addr))
    #         thread.start()                    
    #         print(f"[ACTIVE CONNECTIONS]: {threading.activeCount() - 1}")

    #     except socket.error as error:
    #         print(error)
    #         self.server.close()

    #     except:
    #         print('bal!!!! hoy na ken re vai')
    #         self.server.close()

    def subfunction(self):
        # 192.168.0.109
        conn,addr= self.server.accept()
        conn.send("OK@Tumi amar Baal.".encode(FORMAT))
        # thread = threading.Thread(target=self.handle_client, args=(conn, addr))
        # thread.start()                    
        # print(f"[ACTIVE CONNECTIONS]: {threading.activeCount() - 1}")
        self.handleClient(conn,addr)



    def handleClient(self,conn,addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        conn.send("OK@Welcome to the File Server.".encode(FORMAT))
        #data = conn.recv(SIZE).decode(FORMAT)


    # # Handle browse button functionality
    # def browseFiles(self):
    #     fname = QFileDialog.getOpenFileName(self, "Select File", "/")
    #     self.fileLocation.setText(fname[0])

    # Handle file style and create download delete buttons
    # def filesLayout(self, index, fileName):
    #     fileNameLabel = QLabel(fileName, self)
    #     fileNameLabel.setAlignment(Qt.AlignCenter)
    #     fileNameLabel.setStyleSheet("QLabel"
    #                         "{"
    #                         "border: 1px hidden grey;"
    #                         "border-radius: 2px;"
    #                         "background-color: lightgrey;"
    #                         "}")
        
    #     # Action Buttons                                
    #     downloadButton = QPushButton('Download', self)
    #     downloadButton.setStyleSheet("background-color: #5bc0de; color: white")

    #     downloadButton.clicked.connect(lambda: self.downloadFile(fileName))

    #     deleteButton = QPushButton('Delete', self)
    #     deleteButton.setStyleSheet("background-color: #d9534f; color: white")

    #     deleteButton.clicked.connect(lambda: self.deleteFile(fileName))

    #     self.fileListLayout.addWidget(fileNameLabel, index, 0, 1, 3)
    #     self.fileListLayout.addWidget(downloadButton, index, 4)
    #     self.fileListLayout.addWidget(deleteButton, index, 5)

    # # Show Server Files
    # def listFiles(self):
    #     self.client.send("LIST".encode(FORMAT))
    #     data = self.client.recv(SIZE).decode(FORMAT)
    #     data = data.split("@")
        
    #     # Clear all previous widget
    #     if data:
    #         for i in reversed(range(self.fileListLayout.count())):
    #             self.fileListLayout.itemAt(i).widget().setParent(None)

    #     if(data[0] != "NULL"):
    #         data = data[1].split("\n")

    #         for i in range(len(data)):
    #             self.filesLayout(i, data[i])
    #     else:
    #         self.statusBox.setText(f"[{data[0]}]: " + data[1])
    
    # def uploadFile(self):
    #     path = self.fileLocation.text()

    #     if not path:
    #         self.statusBox.setText("[NULL]: Select a file directory first")
    #     else:
    #         filename = path.split("/")[-1]
    #         filesize = str(os.path.getsize(path))

    #         send_data = f"UPLOAD@{filename}@{filesize}"
    #         self.client.send(send_data.encode(FORMAT))
            
    #         with open(f"{path}", "rb") as f:
    #             start_time = time.time()

    #             bytesToSend = f.read(SIZE)
    #             self.client.send(bytesToSend)
    #             while len(bytesToSend) !=0:
    #                 bytesToSend = f.read(SIZE)
    #                 self.client.send(bytesToSend)
                
    #             end_time = time.time()

    #         self.statusBox.setText("File UPLOAD Complete. Transfer time: " + "{:.2f}".format(end_time - start_time) + "s")
    #         self.fileLocation.setText(None)
            
    #         time.sleep(WAIT_TIME)
    #         self.listFiles()
    
    # def downloadFile(self, fileName):
    #     downloadLocation = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

    #     path = f"server_data/{fileName}"

    #     fileSize = str(os.path.getsize(path))

    #     send_data = f"DOWNLOAD@{fileName}@{fileSize}@{downloadLocation}"
    #     self.client.send(send_data.encode(FORMAT))

    #     with open(path, "rb") as f:
    #         start_time = time.time()

    #         bytesToSend = f.read(SIZE)
    #         self.client.send(bytesToSend)
    #         while len(bytesToSend) !=0:
    #             bytesToSend = f.read(SIZE)
    #             self.client.send(bytesToSend)
            
    #         end_time = time.time()
        
    #     self.statusBox.setText("File DOWNLOAD Complete. Transfer time: " + "{:.2f}".format(end_time - start_time) + "s")
    
    # def deleteFile(self, fileName):
    #     self.client.send(f"DELETE@{fileName}".encode(FORMAT))

    #     data = self.client.recv(SIZE).decode(FORMAT).split("@")
    #     self.statusBox.setText(f"[{data[0]}]: {data[1]}")
        
    #     time.sleep(WAIT_TIME)
    #     self.listFiles()
        
app = QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(WINDOW_WIDTH)
widget.setFixedHeight(WINDOW_HEIGHT)
widget.show()
sys.exit(app.exec_())




#### experiment

# main raw code 

# def handle_client(conn, addr):
#     print(f"[NEW CONNECTION] {addr} connected.")
#     conn.send("OK@Welcome to the File Server.".encode(FORMAT))

#     while True:
#         data = conn.recv(SIZE).decode(FORMAT)
        
#         if data:
#             print(data + ".....")
        
#         data = data.split("@")
#         cmd = data[0]

#         if cmd == "LIST":
#             files = os.listdir(SERVER_DATA_PATH)
#             send_data = "OK@"

#             if len(files) == 0:
#                 send_data = "NULL@The server directory is empty"
#             else:
#                 send_data += "\n".join(f for f in files)
#             conn.send(send_data.encode(FORMAT))
        
#         elif cmd == "UPLOAD":
#             name = data[1]
            
#             files = os.listdir(SERVER_DATA_PATH)
#             name = name.split(".")[0] + "_(" + str(len(files)) + ")." + name.split(".")[1]
            
#             filepath = os.path.join(SERVER_DATA_PATH, name)
#             filesize = int(data[2])

#             with open(filepath, "wb") as f:
#                 start_time = time.time()

#                 data = conn.recv(SIZE)
#                 totalRecv = len(data)
#                 f.write(data)

#                 while totalRecv < filesize:
#                     data = conn.recv(SIZE)
#                     totalRecv += len(data)
#                     f.write(data)
#                     # print("{0:.2f}".format((totalRecv/float(filesize))
#                     # *100)+"% DONE")

#                 end_time = time.time()
            
#             print("File DOWNLOAD Complete. Transfer time: " + "{:.2f}".format(end_time - start_time) + "s")
        
#         elif cmd == "DOWNLOAD":
#             name, fileSize, path = data[1], data[2], data[3]
#             filePath = os.path.join(path, name)
#             fileSize = int(data[2])

#             with open(filePath, "wb") as f:
#                 start_time = time.time()

#                 data = conn.recv(SIZE)
#                 totalRecv = len(data)
#                 f.write(data)

#                 while totalRecv < fileSize:
#                     data = conn.recv(SIZE)
#                     totalRecv+=len(data)
#                     f.write(data)
#                     # print("{0:.2f}".format((totalRecv/float(filesize))
#                     # *100)+"% DONE")

#                 end_time = time.time()
            
#             print("File UPLOAD Complete. Transfer time: " + "{:.2f}".format(end_time - start_time) + "s")
        
#         elif cmd == "DELETE":
#             files = os.listdir(SERVER_DATA_PATH)
#             send_data = "OK@"
#             filename = data[1]

#             if len(files) == 0:
#                 send_data += "The server directory is empty"
#             else:
#                 if filename in files:
#                     # os.system(f"rm '{SERVER_DATA_PATH}/{filename}'")
#                     os.remove(f"{SERVER_DATA_PATH}/{filename}")
#                     send_data += "File deleted successfully."
#                 else:
#                     send_data += "File not found."

#             conn.send(send_data.encode(FORMAT))

#         elif cmd == "LOGOUT":
#             break
#         elif cmd == "HELP":
#             data = "OK@"
#             data += "LIST: List all the files from the server.\n"
#             data += "UPLOAD <path>: Upload a file to the server.\n"
#             data += "DELETE <filename>: Delete a file from the server.\n"
#             data += "LOGOUT: Disconnect from the server.\n"
#             data += "HELP: List all the commands."

#             conn.send(data.encode(FORMAT))

#     print(f"[DISCONNECTED]: {addr} disconnected")
#     conn.close()

# def main():
#     try:
#         print("[STARTING]: Server is starting")
#         server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server.bind(ADDR)
#         server.listen()
#         print(f"[LISTENING]: Server is listening on {IP}:{PORT}.") 
#         while True:
#             conn, addr = server.accept()
#             thread = threading.Thread(target=handle_client, args=(conn, addr))
#             thread.start()
#             print(f"[ACTIVE CONNECTIONS]: {threading.activeCount() - 1}")

#     except socket.error as error:
#         print(error)

# if __name__ == "__main__":
#     main()
