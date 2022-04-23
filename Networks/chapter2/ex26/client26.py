"""EX 2.6 client implementation
   Author: Avi Babian
   Date: 19/04/2022
"""

import socket
import protocol


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    while True:
        user_input = input("Enter command\n")
        # Check if user entered a valid command as defined in protocol
        valid_cmd = protocol.check_cmd(user_input)

        if valid_cmd:
            # If the command is valid:
            # 1. Add length field ("RAND" -> "04RAND") V
            # 2. Send it to the server V
            # 3. If command is EXIT, break from while loop V
            # 4. Get server's response
            # 5. If server's response is valid, print it

            user_input = "04" + user_input
            my_socket.send(user_input.encode())
            if user_input[2:] == "EXIT":
                break
            length = int(my_socket.recv(2).decode())
            response = my_socket.recv(length).decode()
            if response != "":
                print(response)
            else:
                print("Response not valid\n")
        else:
            print("Not a valid command")

    print("Closing\n")
    my_socket.close()


if __name__ == "__main__":
    main()
