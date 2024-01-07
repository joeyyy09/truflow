import socket
import sys
import os

SERVER_IP = "0.0.0.0"
PORT = 6666

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
    file_name = input("enter the file name to be sent: ")
    file_size = str(os.path.getsize(file_name)) + '\n'

    client_socket.send(file_name.encode())
    client_socket.send(file_size.encode())
    
    with open(file_name,"rb") as file:
            sendfile = file.read()
            client_socket.sendall(sendfile)
    print("Data has been sent successfully")


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
    
    send_files(client)

    thread = 1
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
        server.close()

if __name__ == "__main__":
    start_server()
