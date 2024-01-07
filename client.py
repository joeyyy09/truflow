import socket
import sys
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
    file_name = input(str("enter the name of the file: "))
    file = open(file_name,"wb")
    file_data = server_socket.recv(1024)
    file.write(file_data)
    file.close()
    print("data has been received successfully")

# Function to start the client and establish a connection with the friend
def start_client():
    # Create a socket object for the client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    friend_ip = input("Enter friend's IP address: ")
    friend_port = int(input("Enter friend's port: "))

    # Connect to the friend's IP and port
    client.connect((friend_ip, friend_port))

    receive_file_thread = threading.Thread(target=receive_files, args=(client,))
    receive_file_thread.start()
    receive_file_thread.join()

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
        client.close()  
 
if __name__ == "__main__":
    start_client()
