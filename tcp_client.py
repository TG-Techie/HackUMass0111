import socket

host_ip, server_port = "127.0.0.1", 9999
data = input("Alice's message: ")

# Initialize a TCP client socket using SOCK_STREAM
alice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

alice.connect((host_ip, server_port))

while True:
    alice.sendall(data.encode())
    print("Bob sent: " + alice.recv(1024).decode())
    data = input("Alice's reply: ")
