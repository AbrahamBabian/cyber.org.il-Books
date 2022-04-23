#   Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020
# implementation:
# Avi Babian
# 21/04/2022
import glob
import os
import shutil
import socket
import subprocess

import pyautogui

import protocol

IP = "0.0.0.0"
PHOTO_PATH = r"C:\Screenshots\screenshot.png"  # The path + filename where the screenshot at the server should be saved


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    # Use protocol.check_cmd first
    if not protocol.check_cmd(cmd):
        return False, "", []
    # Then make sure the params are valid -->FUNC (UPON) CHECKS PARAMS TOO
    if cmd[:3] == "DIR":
        path = cmd[4:]
        return True, "DIR", [path]
    if cmd[:6] == "DELETE":
        path = cmd[7:]
        return True, "DELETE", [path]
    if cmd[:4] == "COPY":
        list_of_words = cmd.split() #DOESNT WORK WITH FILES THAT HAVE SPACES IN THEIR PATHS
        path1 = list_of_words[1]
        path2 = list_of_words[2]
        return True, "COPY", [path1, path2]
    if cmd[:7] == "EXECUTE":
        path = cmd[8:]
        return True, "EXECUTE", [path]
    if cmd.strip() == "TAKE_SCREENSHOT":
        return True, "TAKE_SCREENSHOT", []
    if cmd.strip() == "SEND_PHOTO":
        return True, "SEND_PHOTO", []
    if cmd.strip() == "EXIT":
        return True, "EXIT", []
    # (6)
    return False, "", []


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """
    if command == "DIR":
        response = str(glob.glob(params[0]))
    if command == "DELETE":
        os.remove(params[0])
        response = "File got deleted"
    if command == "COPY": #COPY C:\Hi\bye.txt C:\Bye\ola.txt
        shutil.copy(params[0], params[1])
        response = "File got copied"
    if command[:7] == "EXECUTE": # e.g. EXECUTE C:\Program Files\Sublime Text\sublime_text.exe
        subprocess.Popen(params)
        response = "Software got executed"
    if command == "TAKE_SCREENSHOT":
        image = pyautogui.screenshot()
        image.save(PHOTO_PATH)
        response = "Screenshot applied and saved"
    if command == "SEND_PHOTO":
        response = str(len(str(os.path.getsize(PHOTO_PATH))))
    if command == "EXIT":
        response = "Server is closing"
    return response


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client Connected")

    # (1)
    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:
                print("Client sent: " + cmd)
                # (6)

                # prepare a response using "handle_client_request"
                response = handle_client_request(command, params)
                # add length field using "create_msg"
                response = protocol.create_msg(response)
                # send to client
                client_socket.send(response)
                if command == 'SEND_PHOTO':
                    # Send the data itself to the client
                    client_socket.send(str(os.path.getsize(PHOTO_PATH)).encode())
                    photo = open(PHOTO_PATH, "rb")
                    binary_data = photo.read()
                    client_socket.send(binary_data)
                    photo.close()
                    # (9)

                if command == 'EXIT':
                    break
            else:
                # prepare proper error to client
                response = '0025Bad command or parameters'
                # send to client
                client_socket.send(response.encode())
        else:
            # prepare proper error to client
            response = '0032Packet not according to protocol'
            # send to client
            client_socket.send(response.encode())
            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
