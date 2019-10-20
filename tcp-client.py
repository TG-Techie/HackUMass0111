import socket

host_ip = '172.30.156.47'

data = input('Alice\'s message: ')

alice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

alice.connect((host_ip, 9999))

while True:
    alice.sendall(data.encode())
    print('Bob sent: ' + alice.recv(1024).decode())
    data = input('Alice\'s reply: ')