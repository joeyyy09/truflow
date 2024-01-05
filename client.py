import socket
import threading
import sys

# Function to receive messages from the friend
def receive_messages(client_socket):
    while True:
        try:
            # Receive data from the friend and decode it
            data = client_socket.recv(1024).decode('utf-8')
            print(f"Friend: {data}")
        except (socket.error, KeyboardInterrupt):
            print("\nConnection closed.")
            break
        sys.stdout.write("You: ")
        sys.stdout.flush()

# Function to start the client and establish a connection with the friend
def start_client():
    # Create a socket object for the client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    friend_ip = input("Enter friend's IP address: ")
    friend_port = int(input("Enter friend's port: "))

    # Connect to the friend's IP and port
    client.connect((friend_ip, friend_port))

    # Start a thread to receive messages from the friend
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    try:
        while True:
            message = input("You: ")
            client.send(message.encode('utf-8'))
    except (socket.error, KeyboardInterrupt):
        print("\nConnection closed.")
        client.close()

if __name__ == "__main__":
    start_client()
