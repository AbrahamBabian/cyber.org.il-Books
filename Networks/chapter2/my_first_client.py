import socket

my_socket = socket.socket()
my_socket.connect(('127.0.0.1', 8820))


send = input("Please enter your input: ")
my_socket.send(send.encode())
data = my_socket.recv(1024).decode()

if data == "" and send != data:
    while data == "" and send != data:
        send = input("The connection got lost, please enter your input again: ")
        my_socket.send(send.encode())
        data = my_socket.recv(1024).decode()

print("Server said: " + data)

my_socket.close()