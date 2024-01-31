import socket
import os
import json
import threading
import time

SERVER_IP = "0.0.0.0"
SERVER_PORT = 6666
BUFFER_SIZE = 1024
FILE_NAME_SIZE = 1024
FILE_SIZE_SIZE = 8
CHUNK_SIZE = 4096

# Dictionary to store the status of each client
client_sockets = {}


def start_server():
    # Create a socket object for the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configuring the socket to reuse addresses and immediately transmit data
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    # Bind the server to the specified IP and port
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # Maximum connects up to 5 clients
    server_socket.listen(5)

    print(f"Server listening on port {SERVER_PORT}")

    while True:
        # Accept a client connection
        client, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")

        # Add the client socket to the dictionary
        client_sockets[addr] = client



if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    server_thread.join()
