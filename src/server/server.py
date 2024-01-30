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
shared_files = {}

def get_shared_files_list():
    shared_files_list = []
    for client_socket in shared_files:
        shared_files_list.extend(shared_files[client_socket])
    return list(set(shared_files_list))  # Remove duplicates using set

def accept_connections(server: socket.socket):
    while True:
        # Accept a client connection
        client, addr = server.accept()
        print(f"Accepted connection from {addr}")

        # Start a thread to handle communication with the connected client
        communication_thread = threading.Thread(target=handle_communication, args=(client,))
        communication_thread.start()

def handle_communication(client_socket: socket.socket):
    try:
        while True:
            # Trim the null values and decode the file name and file size
            file_name: str = client_socket.recv(FILE_NAME_SIZE).decode().rstrip('\x00')
            file_size = int(client_socket.recv(FILE_SIZE_SIZE).decode().rstrip('\x00'))

            # data is received in chunks and writes in the file
            received_data = b""
            while len(received_data) < file_size:
                chunk = client_socket.recv(CHUNK_SIZE)
                if not chunk:
                    break
                received_data += chunk

            # creates a recv directory if not exists
            os.makedirs('recv', exist_ok=True)

            with open(f'recv/{file_name}', 'wb') as file:
                file.write(received_data)

            print("Data has been received successfully")

    except Exception as e:
        print(f"Error receiving file: {e}")

    finally:
        client_socket.close()

def start_server():
    # Create a socket object for the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configuring the socket to reuse addresses and immediately transmit data
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    # Bind the server to the specified IP and port
    server.bind((SERVER_IP, SERVER_PORT))

    # Maximum connects up to 5 clients
    server.listen(5)

    print(f"Server listening on port {SERVER_PORT}")

    while True:
        # Accept a client connection
        client, addr = server.accept()
        print(f"Accepted connection from {addr}")

        # Add the client socket to the dictionary
        client_sockets[addr] = client

def send_files_to_client(client_addr, file_name):
    try:
        # Check if the file exists
        if not os.path.exists(file_name):
            print(f"Error: File '{file_name}' does not exist.")
            return

        file_size = str(os.path.getsize(file_name))

        # file name and file size are padded with null values for fixed length
        client_socket = client_sockets.get(client_addr)
        if client_socket:
            client_socket.send(file_name.ljust(FILE_NAME_SIZE, '\x00').encode())
            client_socket.send(file_size.ljust(FILE_SIZE_SIZE, '\x00').encode())

            # send the file completely
            with open(file_name, "rb") as file:
                sendfile = file.read()
                client_socket.sendall(sendfile)
                print("Data has been sent successfully")

    except Exception as e:
        print(f"Error sending file: {e}")

def start_shared_files_thread():
    while True:
        # Send shared files list to all connected clients periodically
        for client_socket in client_sockets.values():
            try:
                shared_file_list = get_shared_files_list()
                client_socket.send(json.dumps(shared_file_list).encode('utf-8'))
            except (socket.error, OSError):
                pass

        time.sleep(1)  # Optional: Adjust the sleep time between sending shared files list

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    shared_files_thread = threading.Thread(target=start_shared_files_thread, daemon=True)
    shared_files_thread.start()

    server_thread.join()
