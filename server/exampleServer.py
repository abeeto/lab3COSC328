import os
from socket import *

# Constants for the server directory
SERVER_DIR = 'server'

class FTPServer:
    def __init__(self, host='127.0.0.1', port=8000):
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        print(f"Server listening on {self.host}:{self.port}")

    def handle_client(self, conn, addr):
        with conn:
            print("Connected by", addr)
            print("conn:", conn)
            while True:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    break
                print(f"Received: {data}")
                command, *args = data.split()
                if command == "QUIT":
                    break
                response = self.process_command(command, args)
                conn.sendall(response.encode("utf-8"))

    def process_command(self, command, args):
        if command == "GET":
            return self.handle_get(args)
        elif command == "PUT":
            return self.handle_put(args)
        return "OK"
    
    def handle_get(self, args):
        filename = args[0]
        if os.path.isfile(f"{SERVER_DIR}/{filename}"):
            with open(f"{SERVER_DIR}/{filename}", "r") as file:
                # return the filename and contents of file
                return file.read()
        else:
            return f"File {filename} not found"

    def handle_put(self, args):
        return "PUT command processed"

    
    def start(self):
        conn, addr = self.sock.accept()
        self.handle_client(conn, addr)

if __name__ == "__main__":
    server = FTPServer()
    server.start()
