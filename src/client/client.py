import socket
import os
import threading
from queue import Queue

BUFFER_SIZE = 1024
FILE_NAME_SIZE = 1024
FILE_SIZE_SIZE = 8
CHUNK_SIZE = 4096


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = input("Enter server's IP address: ")
    server_port = int(input("Enter server's port: "))

    client.connect((server_ip, server_port))


if __name__ == "__main__":
    start_client()
