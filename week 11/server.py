import socket

class DSServer:
    def __init__(self, port=50000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', port))
        self.socket.listen()
        print(f"DS-Server is listening on port {port}")
        self.jobs = [
            "JOBN 1 1024 200 4",
            "JOBN 2 2048 500 1",
            "NONE"
        ]
        self.job_index = 0
        
    def send_message(self, conn, message):
        """Helper function to send properly formatted messages"""
        print(f"Sending: {message}")
        conn.sendall(f"{message}\n\0".encode())

    def receive_message(self, conn):
        """Helper function to receive and parse messages"""
        data = conn.recv(1024).decode().strip('\0\n')
        print(f"Received raw: {data!r}")
        return data
        
    def handle_client(self, conn):
        try:
            while True:
                data = self.receive_message(conn)
                if not data:
                    break
                    
                if data == "HELO":
                    self.send_message(conn, "GOOD")
                elif data.startswith("AUTH"):
                    self.send_message(conn, "GOOD")
                elif data == "REDY":
                    if self.job_index < len(self.jobs):
                        job = self.jobs[self.job_index]
                        self.send_message(conn, job)
                        self.job_index += 1
                    else:
                        self.send_message(conn, "NONE")
                elif data == "GOOD":
                    continue  # Client acknowledged the job
                elif data == "QUIT":
                    self.send_message(conn, "QUIT")
                    break
                else:
                    self.send_message(conn, "ERR")
        finally:
            conn.close()
            print("Client connection closed")

    def run(self):
        try:
            while True:
                conn, addr = self.socket.accept()
                print(f"Connection from {addr}")
                self.handle_client(conn)
                self.job_index = 0  # Reset jobs for new client
        except KeyboardInterrupt:
            print("\nServer shutting down...")
        finally:
            self.socket.close()
            print("Server shutdown complete")

if __name__ == "__main__":
    server = DSServer()
    server.run()