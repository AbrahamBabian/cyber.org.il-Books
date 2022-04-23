"""EX 2.6 server implementation
   Author: Avi Babian
   Date: 19/04/2022
"""
import datetime
import random
import socket
import protocol

NAME = "Avi's Server"

def create_server_rsp(cmd):
    """Based on the command, create a proper response"""
    if cmd == "EXIT":
        response = "Server got closed"
    elif cmd == "TIME":
        response = str(datetime.datetime.now())
    elif cmd == "NAME":
        response = NAME
    elif cmd == "RAND":
        response = str(random.randint(1, 10))

    length = str(len(response))
    zfill_length = length.zfill(2)
    response = zfill_length + response

    return response


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    while True:
        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:
            # 1. Print received message V
            # 2. Check if the command is valid
            # 3. If valid command - create response
            print("Client sent: " + cmd)
            if protocol.check_cmd(cmd):
                response = create_server_rsp(cmd)
            else:
                response = "Wrong command"
        else:
            response = "Wrong protocol"
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage
        # Handle EXIT command, no need to respond to the client
        if cmd == "EXIT":
            break
        # Send response to the client
        client_socket.send(response.encode())
    print("Closing\n")

    # Close sockets
    server_socket.close()
    client_socket.close()

if __name__ == "__main__":
    main()
