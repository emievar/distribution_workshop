import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 12345))

while True:
  message = client_socket.recv(1024)
  print("Message from server:", message.decode())
  if input("Exit to close:").strip().lower() == "exit":
    break

  client_socket.close()