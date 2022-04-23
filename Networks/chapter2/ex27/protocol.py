#   Ex. 2.7 template - protocol
# implementation:
# Avi Babian
# 21/04/2022
import glob
import os

LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    CHECKS FOR CMD AND PARAMS
    """
    # (3)
    if data[:3] == "DIR":
        path = data[4:]
        return glob.glob(path)
    if data[:6] == "DELETE":
        path = data[7:]
        return os.path.isfile(path)
    if data[:4] == "COPY": #DIRNAMES MUSTNT HAVE WHITESPACES
        list_of_words = data.split()
        if len(list_of_words) != 3:
            return False
        path1 = list_of_words[1]
        path2 = list_of_words[2]
        return os.path.isfile(path1) and os.path.exists(os.path.dirname(path2))
    if data[:7] == "EXECUTE":
        path = data[8:]
        return os.path.isfile(path)
    if data == "TAKE_SCREENSHOT":
        return True
    if data == "SEND_PHOTO":
        return True
    if data == "EXIT":
        return True
    return False


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    # (4)
    length = str(len(data))
    zfill_length = length.zfill(4)
    message = zfill_length + data
    return message.encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    length = my_socket.recv(4).decode()
    if not length.isnumeric():
        return False, "Error"
    return True, my_socket.recv(int(length)).decode()


