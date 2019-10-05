import socket
import traceback
import uuid
from multiprocessing import Pipe, Process

from arduino_connector import ArduinoConnector
from controll_listener import ControlListener

from common import HANDSHAKE_MESSAGE, SERVER_LISTENING_PORT, CLIENT_LISTENING_PORT

host = ''
port = SERVER_LISTENING_PORT
listening_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listening_socket.bind((host,port))

sending_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_connected = False
while True:
    try:
        message, address = listening_socket.recvfrom(1024)
        print("Got data from {}, Veryfing preable...".format(address))
        if message == HANDSHAKE_MESSAGE:
            connection_address = (address[0], CLIENT_LISTENING_PORT)
            print("Client verified, setting up connection with {} ...".format(connection_address))
            client_auth_id = uuid.uuid1()
            sending_socket.sendto(client_auth_id.bytes, connection_address)
            message, address = listening_socket.recvfrom(1024)
            if address[0] == connection_address[0] and client_auth_id.bytes == message[:16]:
                client_connected = True
                print("Connection set. Initilizing PoiBoi controls...")
                listener_connection, connector_connection = Pipe()
                listener = Process(target=ControlListener.run, args=[listening_socket, listener_connection,
                                                                     client_auth_id])
                connector = Process(target=ArduinoConnector.run, args=(connector_connection, ))
                listener.start()
                connector.start()

                listener.join()
                connector.join()
        else:
            print("Invalid preamble, refusing connection.")
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
listening_socket.close()
sending_socket.close()