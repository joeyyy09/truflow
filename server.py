import socket
import threading

def handle_client(client_socket, address):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            print(f"Connection closed by {address}")
            break
        print(f"Received from {address}: {data}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(2)
    print("Server listening on port 5555")

    while True:
        client, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()
