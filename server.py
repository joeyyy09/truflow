import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print("\nConnection closed.")
                break
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

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(1)
    print("Server listening on port 5555")

    client, addr = server.accept()
    print(f"Accepted connection from {addr}")

    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()

if __name__ == "__main__":
    start_server()
