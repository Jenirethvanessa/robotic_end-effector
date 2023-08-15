import pygame
import serial
import pandas as pd
import time

import utilities
from twist_command import example_move_to_home_position
from twist_command import example_twist_command
from utilities import DeviceConnection
from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from move_angular_and_cartesian import example_cartesian_action_movement_down
from move_angular_and_cartesian import example_cartesian_action_movement_up
from move_angular_and_cartesian import example_cartesian_action_movement_right
from move_angular_and_cartesian import example_cartesian_action_movement_left
from kortex_api.autogen.client_stubs.BaseCyclicClientRpc import BaseCyclicClient
from move_angular_and_cartesian import example_move_to_retract_position
from move_angular_and_cartesian import example_move_to_initial_position
from move_angular_and_cartesian import wrist_rotation


# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Xbox Controller Input")
clock = pygame.time.Clock()

# Initialize the joystick module
pygame.joystick.init()

# Check if any joysticks/controllers are connected
if pygame.joystick.get_count() == 0:
    print("No joystick/controllers found.")
    pygame.quit()
    quit()

# Get the first joystick/controller
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Initialize serial communication with Arduino
arduino = serial.Serial('COM10', 9600)  

# Arguments for the robotic arm
args = {
	"ip": "192.168.1.10",
	"username": "admin",
	"password": "admin"
}

# Main program loop
running = True
controller = None
previous_hat = None
previous_trigger_value = ""

person_id = input("Enter person identification number: ")
experiment_num = input("Enter experiment number: ")
trial_num = input("Enter trial number: ")
vibration_feedback = input("Enter 'on' or 'off' to use haptic feedback:")
trigger_value = ""

file_suffix = f"person_{person_id}_exp_{experiment_num}_trial_{trial_num}.csv"
arduino_csv = open(f"arduino_{file_suffix}", "w")
time_csv = open(f"time_{file_suffix}", "w")

try:
    while running:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.JOYDEVICEADDED:
                    controller = pygame.joystick.Joystick(event.device_index)
                    print(f"Joystick {controller.get_instance_id()} connencted")

            # Check for button press event
            if event.type == pygame.JOYBUTTONDOWN:
                button = event.button

                if button == 0:  # A button
                    print("A button pressed")
                    arduino.write(b'r\n')
                
                elif button == 1:  # B button
                    print("B button pressed")
                    arduino.write(b'3\n')

                elif button == 2:  # X button
                    print("X button pressed")
                    arduino.write(b'1\n')  

                elif button == 3:  # Y button
                    print("Y button pressed")
                    arduino.write(b'2\n')
    
                elif button == 4:  # Left bumper
                    print("Left bumper pressed")
                    arduino.write(b'o\n')

                elif button == 5:  # Right bumper
                    print("Right bumper pressed")
                    time_csv.write(f"close,{time.time()}\n")
                    arduino.write(b'c\n')

                elif button ==6:
                    # with utilities.DeviceConnection.createTcpConnection(args) as router:
                    #     # Create required services
                    #     base = BaseClient(router)
                    #     # Example core
                    #     success = example_move_to_home_position(base)
                    arduino.write(b's\n')

                elif button ==7:
                    with utilities.DeviceConnection.createTcpConnection(args) as router:
                        # Create required services
                        base = BaseClient(router)
                        base_cyclic = BaseCyclicClient(router)
                        # Example core
                        success = example_move_to_initial_position(base, base_cyclic)
                        #success = example_move_to_retract_position(base)
                elif button == 9:
                    with utilities.DeviceConnection.createTcpConnection(args) as router:
                        # Create required services
                        angle = 10
                        base = BaseClient(router)
                        base_cyclic = BaseCyclicClient(router)
                        # Example core
                        success, angle_receive = wrist_rotation(base, base_cyclic, angle)

        # Read the data from the serial port and decode it
        analog_value = arduino.readline().decode("latin")
        arduino_csv.write(f"{trigger_value}, {analog_value}")  

        FSR_str = analog_value.split(',')
        if len(FSR_str) > 1:
            FSR = int(FSR_str[1])
        else:
            FSR = 0

        # if len(analog_value) == 8:
        # print(analog_value)
        # print(FSR)
        #     FSR = int(analog_value[-4:-1])
        #     print(FSR)
        # else: 
        #     FSR = 0

        if controller is not None:
            hat = joystick.get_hat(0)

            if previous_hat != hat:
                if hat == (0, 1):
                    print("Last button: UP")
                    with utilities.DeviceConnection.createTcpConnection(args) as router:
                        # Create required services
                        base = BaseClient(router)
                        base_cyclic = BaseCyclicClient(router)
                        # Example core
                        success = example_cartesian_action_movement_up(base, base_cyclic)
                        

                elif hat == (0, -1):
                    print("Last button: DOWN")
                    with utilities.DeviceConnection.createTcpConnection(args) as router:
                        # Create required services
                        base = BaseClient(router)
                        base_cyclic = BaseCyclicClient(router)
                        # Example core
                        success = example_cartesian_action_movement_down(base, base_cyclic)
                        time_csv.write(f"down,{time.time()}\n")
                elif hat == (1, 0):
                    print("Last button: RIGHT")
                    with utilities.DeviceConnection.createTcpConnection(args) as router:
                        # Create required services
                        base = BaseClient(router)
                        base_cyclic = BaseCyclicClient(router)
                        # Example core
                        success = example_cartesian_action_movement_right(base, base_cyclic)
                
                elif hat == (-1, 0):
                    print("Last button: DOWN")
                    with utilities.DeviceConnection.createTcpConnection(args) as router:
                        # Create required services
                        base = BaseClient(router)
                        base_cyclic = BaseCyclicClient(router)
                        # Example core
                        success = example_cartesian_action_movement_left(base, base_cyclic)
                        

                previous_hat = hat

            # if joystick.get_axis(4) != 0.0:
            #     left_trigger_value = joystick.get_axis(4)
            #     if left_trigger_value > -0.9:
            #         #print(f"Axis {left_trigger_value}")
            #         left_trigger_value = (1 - ((left_trigger_value + 1) / 2)) * 10
            #         left_trigger_value_str = f'L{str(left_trigger_value)[:2]}\n'
            #         if previous_trigger_value != left_trigger_value_str:
            #             arduino.write(left_trigger_value_str.encode())
            #             previous_trigger_value = left_trigger_value_str
            #         #print(left_trigger_value_str[0:4])
            #         #if left_trigger_value < 0.1:
            #             #joystick.rumble(0, 0.7, 500)

            if joystick.get_axis(5) != 0.0:
                trigger_value = joystick.get_axis(5)
                if trigger_value > -1.1:
                    trigger_value =  (1 - ((trigger_value + 1) / 2)) * 10
                    #print(trigger_value)
                    trigger_value = str(trigger_value)[:2]

                    if previous_trigger_value != trigger_value:
                        #print(previous_trigger_value)

                        if previous_trigger_value > trigger_value:
                            close_trigger_value_str = f'R{str(trigger_value)}\n'
                            arduino.write(close_trigger_value_str.encode())
                            previous_trigger_value = trigger_value
                        else:
                            trigger_value_open = abs(float(trigger_value) - 10)
                            open_trigger_value_str = f'L{str(trigger_value_open)}\n'
                            arduino.write(open_trigger_value_str.encode())
                            previous_trigger_value = trigger_value
                if vibration_feedback == 'on':
                    if FSR> 800 and FSR < 900:
                        joystick.rumble(0, 0.1, 10)
                    # elif FSR > 850 and FSR < 900:
                    #     joystick.rumble(0, 0.5, 10)
                    elif FSR > 900:
                        joystick.rumble(0, 0.8, 10)



        pygame.display.flip()
        #clock.tick(30)
        

except Exception as e:
    raise e
finally:

    arduino_csv.close()
    time_csv.close()

    # Cleanup
    pygame.quit()
    #arduino.close()

