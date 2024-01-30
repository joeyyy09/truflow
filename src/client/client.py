import socket
import os
import threading
from queue import Queue

BUFFER_SIZE = 1024
FILE_NAME_SIZE = 1024
FILE_SIZE_SIZE = 8
CHUNK_SIZE = 4096

# Use a queue for thread-safe communication
message_queue = Queue()

def receive_messages(client_socket: socket.socket) -> int:
    try:
        while True:
            data: str = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            # Display the received message from the client
            print(f"Friend: {data}")
    except (socket.error, KeyboardInterrupt):
        print("\nConnection closed.")
        return 0

def send_messages(client_socket: socket.socket) -> int:
    try:
        while True:
            message = input("You: ")
            client_socket.send(message.encode('utf-8'))
    except (socket.error, KeyboardInterrupt):
        print("\nConnection closed.")
        return 0

def send_files(client_socket: socket.socket):
    try:
        file_name = input("Enter the file name to be sent: ")

        # file name and file size are padded with null values for fixed length
        client_socket.send(file_name.ljust(FILE_NAME_SIZE, '\x00').encode())
        client_socket.send(str(os.path.getsize(file_name)).ljust(FILE_SIZE_SIZE, '\x00').encode())

        # send the file completely
        with open(file_name, "rb") as file:
            sendfile = file.read()
            client_socket.sendall(sendfile)
        print("Data has been sent successfully")

    except Exception as e:
        print(f"Error sending file: {e}")

def receive_files(client_socket: socket.socket):
    try:
        file_name: str = client_socket.recv(FILE_NAME_SIZE).decode().rstrip('\x00')
        file_size = int(client_socket.recv(FILE_SIZE_SIZE).decode().rstrip('\x00'))

        received_data = b""
        while len(received_data) < file_size:
            chunk = client_socket.recv(CHUNK_SIZE)
            if not chunk:
                break
            received_data += chunk

        os.makedirs('recv', exist_ok=True)

        with open(f'recv/{file_name}', 'wb') as file:
            file.write(received_data)

        print("Data has been received successfully")

    except Exception as e:
        print(f"Error receiving file: {e}")

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = input("Enter server's IP address: ")
    server_port = int(input("Enter server's port: "))

    client.connect((server_ip, server_port))

    while True:
        print("\nChoose an option:")
        print("1. Send a file")
        print("2. Receive a file")
        print("3. Chat")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            send_files(client)
        elif choice == "2":
            receive_files(client)
        elif choice == "3":
            chat_thread = threading.Thread(target=receive_messages, args=(client,), daemon=True)
            chat_thread.start()

            send_thread = threading.Thread(target=send_messages, args=(client,), daemon=True)
            send_thread.start()

            chat_thread.join()
            send_thread.join()

        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

    client.close()

if __name__ == "__main__":
    start_client()
