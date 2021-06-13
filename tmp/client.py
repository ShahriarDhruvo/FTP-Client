import os
import time
import socket
from constants import *

def connectClient():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")

        if cmd == "DISCONNECTED":
            print(f"[SERVER]: {msg}")
            break
        elif cmd == "OK":
            print(f"{msg}")

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "HELP":
            client.send(cmd.encode(FORMAT))
        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break
        elif cmd == "LIST":
            client.send(cmd.encode(FORMAT))
        elif cmd == "DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))
        elif cmd == "UPLOAD":
            path = data[1]
            filename = path.split("/")[-1]
            filesize = str(os.path.getsize(path))

            send_data = f"{cmd}@{filename}@{filesize}"
            client.send(send_data.encode(FORMAT))

            with open(f"{path}", "rb") as f:
                bytesToSend = f.read(1024)
                client.send(bytesToSend)
                while len(bytesToSend) !=0:
                    bytesToSend = f.read(1024)
                    client.send(bytesToSend)

            # path = data[1]

            # filename = path.split("/")[-1]
            # file_size = os.path.getsize(path)

            # # Sending file details
            # send_data = f"UPLOAD@{filename}@{file_size}"
            # client.send(send_data.encode(FORMAT))

            # with open(f"{path}", "rb") as file:
            #     c = 0

            #     data = file.read(SIZE)
            #     while len(data) > 0:
            #         print(len(data), "Pathaisi")

            #         client.send(data)
            #         data = file.read(SIZE)
            #         # c += len(data)

            #     print("Pathano shas")
            # path = data[1]

            # with open(f"{path}", "r") as f:
            #     text = f.read()

            # filename = path.split("/")[-1]
            # send_data = f"{cmd}@{filename}@{text}"
            # client.send(send_data.encode(FORMAT))

    print("[DISCONNECTED] Disconnected from the server.")
    client.close()

if __name__ == "__main__":
    connectClient()
