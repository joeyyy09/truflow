import socket
import os
import threading
from queue import Queue

BUFFER_SIZE = 1024
FILE_NAME_SIZE = 1024
FILE_SIZE_SIZE = 8
CHUNK_SIZE = 4096

def start_client2():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = input("Enter server's IP address: ")
    server_port = int(input("Enter server's port: "))

    client.connect((server_ip, server_port))

    # Create a separate socket for chatting
    chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_port = int(input("Enter chat port: "))
    chat_socket.connect(('0.0.0.0', chat_port))

    # Start a thread to handle receiving messages
    threading.Thread(target=receive_messages, args=(chat_socket,)).start()

    # Start sending messages
    while True:
        message = input("You: ")
        chat_socket.send(message.encode('utf-8'))

def receive_messages(chat_socket):
    while True:
        message = chat_socket.recv(BUFFER_SIZE).decode('utf-8')
        print(f"Client 1: {message}")

if __name__ == "__main__":
    start_client2()
