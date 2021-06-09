import socket

# GUI Window height, width
WINDOW_WIDTH = 853
WINDOW_HEIGHT = 767

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456

ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
