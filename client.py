import socket
import sys
import os

# Function to receive messages from the friend
def receive_messages(client_socket):
    try:
        data = client_socket.recv(1024).decode('utf-8')
            
        # Check if data is empty, indicating the client has closed the connection
        if not data:
            print("\nConnection closed.")
            sys.exit()
 
        # Display the received message from the client
        print(f"Friend: {data}")
    except (socket.error, KeyboardInterrupt):
        print("\nConnection closed.")
        sys.exit()


def send_messages(client_socket):
    try:
        message = input("You: ")
        client_socket.send(message.encode('utf-8'))
    except (socket.error, KeyboardInterrupt):
        print("\nConnection closed.")
        sys.exit()

def receive_files(server_socket):
    file_name = server_socket.recv(1024).decode()
    print(file_name)

    file_size_bytes = b""
    while True:
        size_chunk = server_socket.recv(1)
        if size_chunk == b"\n":
            break
        file_size_bytes += size_chunk

    file_size = int(file_size_bytes.decode())

    received_data = b""
    while len(received_data) < file_size:
        chunk = server_socket.recv(4096)
        if not chunk:
            break
        received_data += chunk

    os.makedirs('recv', exist_ok=True)

    with open(f'recv/{file_name}', 'wb') as file:
        file.write(received_data)

    print("Data has been received successfully")

# Function to start the client and establish a connection with the friend
def start_client():
    # Create a socket object for the client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    friend_ip = input("Enter friend's IP address: ")
    friend_port = int(input("Enter friend's port: "))

    # Connect to the friend's IP and port
    client.connect((friend_ip, friend_port))

    receive_files(client)

    thread = 0
    try:
        while True:
            if thread == 1:
                send_messages(client)
                thread = 0
            else:
                receive_messages(client) 
                thread = 1
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        client.close()  
 
if __name__ == "__main__":
    start_client()
