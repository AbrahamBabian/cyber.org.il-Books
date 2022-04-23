"""EX 2.6 protocol implementation
   Author: Avi Babian
   Date: 19/04/2022
"""

LENGTH_FIELD_SIZE = 2
PORT = 8820


def check_cmd(data):
    """Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)"""
    return (data == "TIME" or data == "NAME" or data == "RAND" or data == "EXIT")


def create_msg(data):
    """Create a valid protocol message, with length field"""
    length = str(len(data))
    zfill_length = length.zfill(2)
    message = zfill_length + data
    return message


def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    length = my_socket.recv(2).decode()
    if not length.isnumeric():
        return False, "Error"
    return True, my_socket.recv(int(length)).decode()
