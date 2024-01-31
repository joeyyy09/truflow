import socket
import threading

BUFFER_SIZE = 1024

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = input("Enter server's IP address: ")
    server_port = int(input("Enter server's port: "))

    client.connect((server_ip, server_port))
    return client

def create_chat_socket():
    chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_port = int(input("Enter chat port: "))
    chat_socket.bind(('0.0.0.0', chat_port))
    chat_socket.listen(1)

    print(f"Waiting for a connection on chat port {chat_port}")
    chat_conn, chat_addr = chat_socket.accept()
    print(f"Connected to {chat_addr} for chatting.")
    return chat_conn

def start_client1():
    client = connect_to_server()
    chat_conn = create_chat_socket()

    # Start a thread to handle receiving messages
    threading.Thread(target=receive_messages, args=(chat_conn,)).start()

    # Start sending messages
    while True:
        message = input("You: ")
        chat_conn.send(message.encode('utf-8'))

def receive_messages(chat_conn):
    while True:
        message = chat_conn.recv(BUFFER_SIZE).decode('utf-8')
        print(f"Client 2: {message}")

if __name__ == "__main__":
    start_client1()
