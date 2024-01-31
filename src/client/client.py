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
    else:
        print("Failed to start client. Exiting....")
