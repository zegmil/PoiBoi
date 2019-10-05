import pygame
import time

from constants import CONTROL_FRAME_PREMABLE


class JoystickConnector:
    @staticmethod
    def run(connection):
        print("Initilizing Joystick Connector subprocess")
        pygame.init()
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        my_joystick = joysticks[0]
        my_joystick.init()
        print("Initilizing joystick {}".format(my_joystick.get_name()))
        #print(my_joystick.get_numaxes())
        while True:
                pygame.event.get()
                left_horizontal_axis = int(my_joystick.get_axis(0) * 100) + 100
                left_vertical_axis = int(my_joystick.get_axis(1) * 100) + 100
                right_horizontal_axis = int(my_joystick.get_axis(3) * 100) + 100
                right_vertical_axis = int(my_joystick.get_axis(4) * 100) + 100
                lt_axis = int(my_joystick.get_axis(2) * 100) + 100
                rt_axis = int(my_joystick.get_axis(5) * 100) + 100
                rt_activation = 1 if rt_axis > 100 else 0
                data = bytes([*CONTROL_FRAME_PREMABLE,
                              left_horizontal_axis, left_vertical_axis, lt_axis,
                              right_horizontal_axis, right_vertical_axis, rt_activation])
                connection.send(data)
                time.sleep(0.050)
