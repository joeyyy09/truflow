import socket
import os
import json
import threading
import time

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5555
SERVER_PORT2 = 5556
BUFFER_SIZE = 1024
FILE_NAME_SIZE = 1024
FILE_SIZE_SIZE = 8
CHUNK_SIZE = 4096

# Dictionary to store the status of each client
all_clients= {}
all_clients2 = {}
# client for general communication between sevrer and client
# client2 for online and heartbeat functionality

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

        recv_message = client.recv(BUFFER_SIZE).decode().rstrip('\x00')
        client_name = recv_message[5:-11]

        # Add the client socket to the dictionary
        all_clients[client_name] = client

def establishing_connection(client_socket: socket.socket):

    client_name = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    address = all_clients[client_name]
    client.send(address.encode('utf-8'))

def start_server2():
    # Server socket for sending who is online to the client
    server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the server to the specified IP and port
    server_socket2.bind((SERVER_IP, SERVER_PORT2))

    # Maximum connects up to 5 clients
    server_socket2.listen(5)

    print(f"Server listening on port {SERVER_PORT2}")

    while True:
        # Accept a client connection
        client2, addr = server_socket2.accept()
        print(f"Accepted connection from {addr}")

        recv_message = client2.recv(BUFFER_SIZE).decode().rstrip('\x00')
        client_name = recv_message[5:-11]

        # Add the client socket to the dictionary
        all_clients2[client_name] = client2

def Heart_Beat_Function():
    global all_clients2
    while True:
        # To store current online users
        temp_dict = {}
        for client2 in all_clients2.values():
            message = client2.recv(BUFFER_SIZE).decode().rstrip('\x00')
            client_name = message[5:-11]
            temp_dict[client_name] = client2
        
        # update online users
        all_clients2 = temp_dict

        serialized_data = json.dumps(list(all_clients2.keys()))

        for client2 in all_clients2.values():
            client2.send(serialized_data.ljust(BUFFER_SIZE,'\x00').encode('utf-8'))
        
        print(all_clients2.keys())

        # Perform hearbeat at a rate of 10seconds
        time.sleep(10.0)

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread2 = threading.Thread(target=start_server2, daemon=True)
    heart_beat = threading.Thread(target=Heart_Beat_Function, daemon=True)

    heart_beat.start()
    server_thread.start()
    server_thread2.start()

    server_thread.join()
    server_thread2.join()
    heart_beat.join()

