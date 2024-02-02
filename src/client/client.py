import socket
import os
import threading
import time
import json
from queue import Queue

BUFFER_SIZE = 1024
FILE_NAME_SIZE = 1024
FILE_SIZE_SIZE = 8
CHUNK_SIZE = 4096
SERVER_PORT = 5555
SERVER_PORT2 = 5556

online_users = {}

client_details = {}

def starting_connection_for_chat(client_socket:socket.socket,chat_socket:socket.socket):
    message = input("Enter the name of the user: ")
    client_socket.send(message.encode('utf-8'))
    received_data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    host, port = received_data.split(',')
    print(f"Host: {host}, Port: {port}")
    chat_socket.connect((host, int(port)))

def receiving_connection_for_chat(client_socket:socket.socket)->socket.socket:
    client, addr = client_socket.accept()
    print(f"Connection Accepted ")
    return client_socket


def send_messages(chat_socket: socket.socket) -> int:
    try:
        message = input("You: ")
        chat_socket.send(message.encode('utf-8'))
        return 1
    except (socket.error, KeyboardInterrupt):
        print("\nConnection closed.")
        return 0

def receive_messages(chat_socket: socket.socket) -> int:
    try:
        data: str = chat_socket.recv(BUFFER_SIZE).decode('utf-8')
            
        # Display the received message from the client
        print(f"Friend: {data}")
        return 1
    except (socket.error, KeyboardInterrupt):
        print("\nConnection closed.")
        return 0

def start_client() -> tuple[socket.socket,socket.socket]:
    try:
        # Client Socket for general communication with the server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        your_name = input("Enter your username: ")
        server_ip = input("Enter server's IP address: ")
        client_details["name"] = your_name
        
        print("Connecting to server...") # Added for debugginf to be removed
        client.connect((server_ip, SERVER_PORT))
        message = "I am "+client_details["name"]+" for online"
        client.send(message.ljust(BUFFER_SIZE,'\x00').encode('utf-8'))

        # Client socket for recieving who is online from the server
        client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Connecting to server (2nd socket)...") # Added for debugginf to be removed
        client2.connect((server_ip, SERVER_PORT2))
        message = "I am "+client_details["name"]+" for online"
        client2.send(message.ljust(BUFFER_SIZE,'\x00').encode('utf-8'))

        
        
        while True:

            print(" Enter 1 to start a chat\n Enter 2 to receive a chat")
            choice  = input("\nEnter your choice: ") 

            if choice == "1":
                chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                starting_connection_for_chat(client,chat_socket)
                send_messages(chat_socket)
                receive_messages(chat_socket)
                chat_socket.close()

            if choice == "2":
                
                receive_socket = receiving_connection_for_chat(client)
                receive_messages(receive_socket)
                send_messages(receive_socket)
                receive_socket.close()

            else:
                print("enter a valid option")

        return client, client2

    except Exception as e:
        print("Error in start_client function in client.py: ",e)
        return None, None

def Heart_Beat_Function(client2: socket.socket):
    global online_users
    
    try:
        while True:
            message = "I am "+client_details["name"]+" for online"
            client2.send(message.ljust(BUFFER_SIZE,'\x00').encode('utf-8'))

            serialized_data = client2.recv(BUFFER_SIZE).decode().rstrip('\x00')
            deserialized_data:list = json.loads(serialized_data)

            # Update online users
            online_users = deserialized_data

            print(online_users)

            # Perform hearbeat at a rate of 10seconds
            time.sleep(10.0)
    
    except Exception as e:
        print("Error in heart_beat_function in client.py: ",e)

if __name__ == "__main__":
    client, client2 = start_client()

    if client and client2:
        heart_beat = threading.Thread(target=Heart_Beat_Function,args= (client2,), daemon=True)
        heart_beat.start()
        heart_beat.join()
    else:
        print("Failed to start client. Exiting....")
