import socket
import sys
import os
import threading

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
    #file size is decoded 
    file_size_bytes = b""
    while True:
        size_chunk = server_socket.recv(1)
        if size_chunk == b"\n":
            break
        file_size_bytes += size_chunk
    file_size = int(file_size_bytes.decode())

    # data is received in chunks and writes in the file
    received_data = b""
    while len(received_data) < file_size:
        chunk = server_socket.recv(4096)
        if not chunk:
            break
        received_data += chunk

    # creates a recv directory if not exists
    os.makedirs('recv', exist_ok=True)

    with open(f'recv/{file_name}', 'wb') as file:
        file.write(received_data)

    print("Data has been received successfully")

def send_files(client_socket):
    # first send the file name and size 
    file_name = input("enter the file name to be sent: ")
    file_size = str(os.path.getsize(file_name)) + '\n'

    client_socket.send(file_name.encode())
    client_socket.send(file_size.encode())
    
    # send the file completely
    with open(file_name,"rb") as file:
            sendfile = file.read()
            client_socket.sendall(sendfile)
    print("Data has been sent successfully")


# Function to start the client and establish a connection with the friend
def start_client():
    # Create a socket object for the client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    friend_ip = input("Enter friend's IP address: ")
    friend_port = int(input("Enter friend's port: "))

    # Connect to the friend's IP and port
    client.connect((friend_ip, friend_port))

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
            chat_thread = threading.Thread(target=chat, args=(client,))
            chat_thread.start()
            chat_thread.join()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

    client.close()

def chat(client_socket):
    try:
        while True:
            receive_messages(client_socket)
            send_messages(client_socket)
    except (socket.error, KeyboardInterrupt):
        print("\nConnection closed.")


 
if __name__ == "__main__":
    start_client()
