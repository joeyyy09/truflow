import socket
import os
import json
import threading
import time

BUFFER_SIZE = 1024
FILE_NAME_SIZE = 1024
FILE_SIZE_SIZE = 8
CHUNK_SIZE = 4096

# It shows the messages received from the socket i.e, 
# client_socket which is passed as a function parameter 
def receive_messages(client_socket: socket.socket) -> int:
    try:
        data: str = client_socket.recv(BUFFER_SIZE).decode('utf-8')
 
        # Display the received message from the client
        print(f"Friend: {data}")
        return 1
    except (socket.error, KeyboardInterrupt):
        print("\nConnection closed.")
        return 0

# It sends messages to the socket i.e, client_socket 
# which is passed as a function parameter 
def send_messages(client_socket: socket.socket) -> int:
    try:
        message = input("You: ")
        client_socket.send(message.encode('utf-8'))
        return 1
    except (socket.error, KeyboardInterrupt):
        print("\nConnection closed.")
        return 0

# It sends the files to the socket i.e, 
# client_socket which is passed as a function parameter 
def send_files(client_socket: socket.socket):
    try:
        file_name = input("enter the file name to be sent: ")

        # Check if the file exists
        if not os.path.exists(file_name):
            print(f"Error: File '{file_name}' does not exist.")
            return
        
        file_size = str(os.path.getsize(file_name))

        # file name and file size are padded with null values for fixed length
        client_socket.send(file_name.ljust(FILE_NAME_SIZE,'\x00').encode())
        client_socket.send(file_size.ljust(FILE_SIZE_SIZE,'\x00').encode())

        # send the file completely
        with open(file_name,"rb") as file:
                sendfile = file.read()
                client_socket.sendall(sendfile)
        print("Data has been sent successfully")

    except Exception as e:
        print(f"Error sending file: {e}")

# It receives files from the socket i.e, 
# client_socket which is passed as a function parameter 
def receive_files(client_socket: socket.socket):
    try:
         # Trim the null values and decode the file name and file size
        file_name: str = client_socket.recv(FILE_NAME_SIZE).decode().rstrip('\x00')
        file_size = int(client_socket.recv(FILE_SIZE_SIZE).decode().rstrip('\x00'))

        # data is received in chunks and writes in the file
        received_data = b""
        while len(received_data) < file_size:
            chunk = client_socket.recv(CHUNK_SIZE)
            if not chunk:
                break
            received_data += chunk

        # creates a recv directory if not exists
        os.makedirs('recv', exist_ok=True)

        with open(f'recv/{file_name}', 'wb') as file:
            file.write(received_data)

        print("Data has been received successfully")

    except Exception as e:
        print(f"Error receiving file: {e}")

def view_shared_files(client_socket: socket.socket, shared_folder: str):
    try:
        client_socket.send("5".encode('utf-8'))  # Send option 5 to request shared files list
        shared_files_list = json.loads(client_socket.recv(BUFFER_SIZE).decode('utf-8'))
        print(f"Shared Files in {shared_folder}: {shared_files_list}")

    except Exception as e:
        print(f"Error viewing shared files: {e}")

# Add a function to continuously share files from the specified folder
def share_all_files(client_socket: socket.socket, shared_folder: str):
    try:
        while True:
            for file_name in os.listdir(shared_folder):
                file_path = os.path.join(shared_folder, file_name)

                if os.path.isfile(file_path):
                    send_files(client_socket, file_path)
                time.sleep(1)  #  Adjust the sleep time between file sharing
    except KeyboardInterrupt:
        pass


def chat(client_socket: socket.socket):
    while True:
        s = send_messages(client_socket)
        r = receive_messages(client_socket)
        if r == 0 or s == 0: return
        
def start_client():
    # Create a socket object for the client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    friend_ip = input("Enter friend's IP address: ")
    friend_port = int(input("Enter friend's port: "))
    shared_folder = input("Enter the path of the folder you want to share: ")


    if not os.path.exists(shared_folder):
        print(f"Error: Shared folder '{shared_folder}' does not exist.")
        return


    # Connect to the friend's IP and port
    client.connect((friend_ip, friend_port))
    # Start a thread to continuously share files from the specified folder
    share_thread = threading.Thread(target=share_all_files, args=(client, shared_folder), daemon=True)
    share_thread.start()

    while True:
        print("\nChoose an option:")
        print("1. Send a file")
        print("2. Receive a file")
        print("3. Chat")
        print("4. View Shared Files")
        print("5. Exit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == "1":
            send_files(client)
        elif choice == "2":
            receive_files(client)
        elif choice == "3":
            chat(client)
        elif choice == "4":
            view_shared_files(client, shared_folder)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

    client.close()
 
if __name__ == "__main__":
    start_client()
