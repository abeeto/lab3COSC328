from socket import *

# Constants for the client directory
CLIENT_DIR = 'client'

class FTPClient:
    def __init__(self, host = "127.0.0.1"):
        self.host = host
        self.sock = None

    def connect(self, port):
        if self.sock is not None:
            print("A connection is already open. Please close it before opening a new one.")
            return
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect((self.host, int(port)))
            print(f"Connected to {self.host}:{port}")
        except Exception as e:
            print(f"Failed to connect to {self.host}:{port} due to: {e}")
            self.sock = None

    def send_command(self, command, args = None):
        if command == "OPEN":
            try: 
                self.open_command(args[0])
            except IndexError:
                print("OPEN command requires a port number. Usage: OPEN <port>")
        if command == "CLOSE":
            self.close_command()
        if command == "QUIT":
            self.quit_command()
        if self.sock: # i.e if it's a PUT or GET command
            # join them back together and send to server side.
            data = command, *args
            data = " ".join(data)
            self.sock.sendall(data.encode("utf-8"))
            response = self.sock.recv(1024).decode("utf-8")
            if command == "GET" and len(args) == 1:
                self.handle_get(response, args)
            elif len(args) > 1:
                print("GET command requires a single filename. Usage: GET <filename>")
            print("Received:", response)


    def handle_get(self, response, args):
        if response == "ERROR404":
            print(f"No file found. Please check the filename and try again.")
            return
        filename = args[0]
        with open(f"{CLIENT_DIR}/{filename}", "w") as file:
            file.write(response)
           
    # commands that are processed on client side: OPEN, CLOSE, QUIT
    def open_command(self, port):
        if self.sock is not None:
            print("A connection is already open. Please close it before opening a new one.")
        else:
            self.connect(port)
    
    def close_command(self):
        if self.sock is not None:
            self.sock.close()
            self.sock = None
            print("Connection closed")
        else:
            print("No open connection to close")
    
    def quit_command(self):
        if self.sock is not None:
            self.close_command()
        print("Goodbye.")
        exit(0)
    
    def run(self):
        while True:
            command, *args = input("FTP> ").split()
            if command:
                self.send_command(command, args)
            if self.sock is None and command != "QUIT":
                print("Looks like there's no connection. Use OPEN command to connect to a server.")

if __name__ == "__main__":
    client = FTPClient()
    client.run()
