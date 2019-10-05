import socket
import sys
from multiprocessing import Process, Pipe

from constants import DETECTION_RETRIES_LIMIT, CONN_SETUP_TIMEOUT
from control_sender import ControlSender
from joystick_connector import JoystickConnector

sys.path.append("..")
from common import HANDSHAKE_MESSAGE, SERVER_LISTENING_PORT, CLIENT_LISTENING_PORT


broadcast_address = ('<broadcast>',SERVER_LISTENING_PORT)
conn_set = False
detection_retries = 0

poiboi_address = None

listening_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listening_socket.settimeout(CONN_SETUP_TIMEOUT)
listening_socket.bind(('', CLIENT_LISTENING_PORT))

sending_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_auth_id = None

while not conn_set and detection_retries < DETECTION_RETRIES_LIMIT:
    # Broadcasting preable to port PoiBoi server port of all adresses visible in the network
    print("Detecting PoiBoi...")
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_socket.sendto(HANDSHAKE_MESSAGE, broadcast_address)
    try:
        client_auth_id, address = listening_socket.recvfrom(1024)
    except socket.timeout:
        print("Could not detect PoiBoi, retrying...")
        broadcast_socket.close()
        detection_retries += 1
        continue
    poiboi_address = (address[0], SERVER_LISTENING_PORT)
    conn_set = True
if detection_retries >= DETECTION_RETRIES_LIMIT and not conn_set:
    print("Did not detect PoiBoi. Retries limit exceeded.")
else:
    print(client_auth_id)
    sending_socket.sendto(client_auth_id + b'ACK', poiboi_address)
    print("PoiBoi detected on address: {}.".format(poiboi_address))
    sender_connection, connector_connection = Pipe()
    connector = Process(target=JoystickConnector.run, args=(connector_connection, ))
    sender = Process(target=ControlSender.run, args=(sending_socket, poiboi_address, sender_connection, client_auth_id))
    connector.start()
    sender.start()
    connector.join()
    sender.join()

listening_socket.close()
sending_socket.close()

