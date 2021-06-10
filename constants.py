import socket

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
