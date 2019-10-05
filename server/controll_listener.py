import sys
sys.path.append("..")
from common import SERVER_FRAME_LENGTH, CLIENT_AUTH_ID_LENGTH


class ControlListener:

    @staticmethod
    def run(listening_socket, connection, client_auth_id):
        print("Initilizing Control Listener subprocess")
        while True:
            message, address = listening_socket.recvfrom(1024)
            if len(message) == SERVER_FRAME_LENGTH and client_auth_id.bytes == message[:CLIENT_AUTH_ID_LENGTH]:
                print("CONTROL_LISTENER: Received control data: {}".format(message))
                connection.send(message[CLIENT_AUTH_ID_LENGTH:])