import socket
import sys
import os
import threading

SERVER_IP = "0.0.0.0"
PORT = 5555

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

def send_files(client_socket):
    # first send the file name and size 
    file_name = input("enter the file name to be sent: ")
    file_size = str(os.path.getsize(file_name))

    client_socket.send(file_name.ljust(1024,'\x00').encode())
    client_socket.send(file_size.ljust(8,'\x00').encode())
    
    # send the file completely
    with open(file_name,"rb") as file:
            sendfile = file.read()
            client_socket.sendall(sendfile)
    print("Data has been sent successfully")

def receive_files(server_socket):
    file_name = server_socket.recv(1024).decode().rstrip('\x00')
    file_size = int(server_socket.recv(8).decode().rstrip('\x00'))
   
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

# Function to start the server
def start_server():
    # Create a socket object for the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the server to the specified IP and port
    server.bind((SERVER_IP, PORT))
    
    server.listen(1)
    
    print(f"Server listening on port {PORT}")

    # Accept a client connection
    client, addr = server.accept()
    print(f"Accepted connection from {addr}")
    
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

    server.close()

def chat(client_socket):
    try:
        while True:
            receive_messages(client_socket)
            send_messages(client_socket)
    except (socket.error, KeyboardInterrupt):
        print("\nConnection closed.")

if __name__ == "__main__":
    start_server()
