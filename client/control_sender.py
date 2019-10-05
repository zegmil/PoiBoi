class ControlSender:
    @staticmethod
    def run(sending_socket, poiboi_address, connection, client_auth_id):
        print("Initilizing Control Sender subprocess")
        while True:
            data = connection.recv()
            sending_socket.sendto(client_auth_id + data, poiboi_address)