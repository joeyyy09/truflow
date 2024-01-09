import socket
import os

SERVER_IP = "0.0.0.0"
PORT = 5555
all_clients: list[socket.socket] = []

# Function to receive messages from the friend
def receive_messages(client_socket):
    try:
        data = client_socket.recv(1024).decode('utf-8')
            
        # Check if data is empty, indicating the client has closed the connection
        if not data:
            print("\nConnection closed.")
            return 0
 
        # Display the received message from the client
        print(f"Friend: {data}")
        return 1
    except (socket.error, KeyboardInterrupt):
        print("\nConnection closed.")
        return 0

def send_messages(client_socket):
    try:
        message = input("You: ")
        client_socket.send(message.encode('utf-8'))
        return 1
    except (socket.error, KeyboardInterrupt):
        print("\nConnection closed.")
        return 0

def send_files(client_socket):
    try:
        file_name = input("enter the file name to be sent: ")

        # Check if the file exists
        if not os.path.exists(file_name):
            print(f"Error: File '{file_name}' does not exist.")
            return
        
        file_size = str(os.path.getsize(file_name))

        # file name and file size are padded with null values for fixed length
        client_socket.send(file_name.ljust(1024,'\x00').encode())
        client_socket.send(file_size.ljust(8,'\x00').encode())

        # send the file completely
        with open(file_name,"rb") as file:
                sendfile = file.read()
                client_socket.sendall(sendfile)
        print("Data has been sent successfully")

    except Exception as e:
        print(f"Error sending file: {e}")

def receive_files(server_socket):
    try:
         # Trim the null values and decode the file name and file size
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

    except Exception as e:
        print(f"Error receiving file: {e}")

def chat(client_socket):
    while True:
        r = receive_messages(client_socket)
        s = send_messages(client_socket)
        if r == 0 or s == 0: return

def accept_connections(server: socket.socket):
    while len(all_clients) < 2:
         # Accept a client connection
        client, addr = server.accept()
        print(f"Accepted connection from {addr}")
        all_clients.append(client)

# Function to start the server
def start_server():
        # Create a socket object for the server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the server to the specified IP and port
        server.bind((SERVER_IP, PORT))
        
        server.listen(5)
        
        print(f"Server listening on port {PORT}")

        accept_connections(server)

        while True:
            client_choice = int(input(f"Enter a number below {len(all_clients)} "))
            if(client_choice >= len(all_clients)):
                print('\nError: Invalid choice')
                break
                
            while True:
                print("\nChoose an option:")
                print("1. Send a file")
                print("2. Receive a file")
                print("3. Chat")
                print("4. Exit")

                choice = input("Enter your choice (1/2/3/4): ")

                if choice == "1":
                    send_files(all_clients[client_choice])
                elif choice == "2":
                    receive_files(all_clients[client_choice])
                elif choice == "3":
                    chat(all_clients[client_choice])
                elif choice == "4":
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")

        server.close()


if __name__ == "__main__":
    start_server()
