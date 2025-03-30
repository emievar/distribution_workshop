import socket
import threading

def handle_client(conn, addr):
    print(f"Connection established with {addr}") #connected to server
    conn.sendall(b"Hello from server!") 

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates sockets
    server_socket.bind(("localhost", 12345)) #binds socket to 12345
    server_socket.listen()
    print("Server is listening on port 12345...")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr)) #individual clients are handled seperately
        thread.start()

if __name__ == "__main__":
    start_server()