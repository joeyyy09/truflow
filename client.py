import socket
import threading
import sys

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            print(f"Friend: {data}")
        except (socket.error, KeyboardInterrupt):
            print("\nConnection closed.")
            break
        sys.stdout.write("You: ")
        sys.stdout.flush()

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    friend_ip = input("Enter friend's IP address: ")
    friend_port = int(input("Enter friend's port: "))

    client.connect((friend_ip, friend_port))

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
