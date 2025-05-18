import socket

def send_message(sock, message):
    """Helper function to send properly formatted messages"""
    sock.sendall(f"{message}\n\0".encode())

def receive_message(sock):
    """Helper function to receive and parse messages"""
    data = sock.recv(1024).decode().strip('\0\n')
    return data

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 50000))
    
    try:
        # Handshake with the server
        send_message(client_socket, "HELO")
        print("send: HELO")
        helo_response = receive_message(client_socket)
        print("receive(",helo_response,")")
        
        username = "47077999"
        send_message(client_socket, f"AUTH {username}")
        print(f"send: AUTH {username}")
        auth_response = receive_message(client_socket)
        print("receive(",auth_response,")")
        
        while True:
            send_message(client_socket, "REDY")
            response = receive_message(client_socket)
            
            if response == "NONE":
                print("No more jobs to schedule")
                break
            elif response.startswith("JOBN"):
                print(f"Received job: {response}")
                send_message(client_socket, "GOOD")
            elif response == "ERR":
                print("Server returned error")
                break
            else:
                print(f"Unexpected response: {response}")
                break
            
        # Graceful termination
        send_message(client_socket, "QUIT")
        quit_response = receive_message(client_socket)
        print(f"Server response to QUIT: {quit_response}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    main()