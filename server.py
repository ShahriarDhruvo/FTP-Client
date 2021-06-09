import os
import time
import socket
import threading
from constants import *

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the File Server.".encode(FORMAT))

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
            filepath = os.path.join(SERVER_DATA_PATH, name)
            filesize = int(data[2])

            with open(filepath, "wb") as f:
                start_time = time.time()

                data = conn.recv(SIZE)
                totalRecv = len(data)
                f.write(data)

                while totalRecv < filesize:
                    data = conn.recv(SIZE)
                    totalRecv+=len(data)
                    f.write(data)
                    # print("{0:.2f}".format((totalRecv/float(filesize))
                    # *100)+"% DONE")

                end_time = time.time()
            
            print("File DOWNLOAD Complete. Transfer time: " + "{:.2f}".format(end_time - start_time) + "s")
        
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
                    totalRecv+=len(data)
                    f.write(data)
                    # print("{0:.2f}".format((totalRecv/float(filesize))
                    # *100)+"% DONE")

                end_time = time.time()
            
            print("File UPLOAD Complete. Transfer time: " + "{:.2f}".format(end_time - start_time) + "s")
        
        elif cmd == "DELETE":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                if filename in files:
                    os.system(f"rm '{SERVER_DATA_PATH}/{filename}'")
                    send_data += "File deleted successfully."
                else:
                    send_data += "File not found."

            conn.send(send_data.encode(FORMAT))

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

    print(f"[DISCONNECTED]: {addr} disconnected")
    conn.close()

def main():
    print("[STARTING]: Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING]: Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]: {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()
