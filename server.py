import socket
import threading

# Function to handle communication with a connected client
def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            
            # Check if data is empty, indicating the client has closed the connection
            if not data:
                print("\nConnection closed.")
                break
            
            # Display the received message from the client
            print(f"Friend: {data}")
        except (socket.error, KeyboardInterrupt):
            print("\nConnection closed.")
            break
        
        try:
            message = input("You: ")
            client_socket.send(message.encode('utf-8'))
        except (socket.error, KeyboardInterrupt):
            print("\nConnection closed.")
            break

# Function to start the server
def start_server():
    # Create a socket object for the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the server to the specified IP and port
    server.bind(('0.0.0.0', 5555))
    

    server.listen(1)
    
    print("Server listening on port 5555")

    # Accept a client connection
    client, addr = server.accept()
    print(f"Accepted connection from {addr}")

    # Start a thread to handle communication with the connected client
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()

if __name__ == "__main__":
    start_server()
