#   Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020
# implementation:
# Avi Babian
# 21/04/2022


import socket
from ex27 import protocol
from ex27 import server

IP = "127.0.0.1"
SAVED_PHOTO_LOCATION = r"C:\Screenshots2\screenshot.png" # The path + filename where the copy of the screenshot at the client should be saved

def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    # (8) treat all responses except SEND_PHOTO
    length = int(my_socket.recv(4).decode())
    response = my_socket.recv(length).decode()
    if cmd == "EXIT":
        print("Client is closing")
    elif response != "" and cmd != "SEND_PHOTO":
        print(response)
    #TAKE_SCREENSHOT
    # (10) treat SEND_PHOTO

    elif cmd == "SEND_PHOTO":
        response = my_socket.recv(int(response))
        response = my_socket.recv(int(response))
        photo = open(SAVED_PHOTO_LOCATION, "wb")
        photo.write(response)
        photo.close()
        print("Photo got sent!")
    else:
        print("Response not valid")

def main():
    # open socket with the server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, protocol.PORT))
    # (2)

    # print instructions
    print('Welcome to remote computer application. Available commands are: ')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR (With Pattern Matching, e.g. \'C:\*\')\nDELETE\nCOPY\nEXECUTE (Enter full path)\nEXIT\n\n*DIRS MUSTNT CONTAIN WHITESPACES WHILE USING COPY*\n')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol.check_cmd(cmd):
            packet = protocol.create_msg(cmd)
            my_socket.send(packet)
            handle_server_response(my_socket, cmd)
        else:
            print("Not a valid command, or missing parameters\n")
        if cmd == "EXIT":
            break

    my_socket.close()

if __name__ == '__main__':
    main()