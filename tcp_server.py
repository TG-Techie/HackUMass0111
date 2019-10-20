import socketserver

class Bob_Handler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            # self.request - TCP socket connected to the client
            print("Alice sent: " + self.request.recv(1024).decode())
            # just send back ACK for data arrival confirmation
            self.request.sendall(input("Enter Bob's reply: ").encode())

if __name__ == "__main__":
    PORT = 9999

    # Init the TCP server object, bind it to the localhost on 9999 port
    tcp_server = socketserver.TCPServer(('localhost', PORT), Bob_Handler)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()