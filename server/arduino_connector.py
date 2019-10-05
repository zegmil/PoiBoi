import serial

class ArduinoConnector:

    @staticmethod
    def run(connection, device="/dev/ttyS0", baudrate=9600):
        print("Initilizing Arduino Connector subprocess")
        uart_interface = serial.Serial(device, baudrate)  # Open port with baud rate
        while True:
            data = connection.recv()
            print("ARDUINO_CONNECTOR: Received control data: {}".format(data))
            uart_interface.write(bytes(data))

