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
	"ip": "192.168.1.12",
	"username": "admin",
	"password": "admin"
}

# Main program loop
running = True
controller = None
previous_hat = None
previous_trigger_value = ""
angle_receive = 0

person_id = input("Instrument: ")
experiment_num = input("open or close: ")

file_suffix = f"{person_id}_exp_{experiment_num}.csv"
test_csv = open(f"test_{file_suffix}", "w")

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

                if button == 1:
                    with utilities.DeviceConnection.createTcpConnection(args) as router:
                        # Create required services
                        angle = 10
                        base = BaseClient(router)
                        base_cyclic = BaseCyclicClient(router)
                        # Example core
                        success, angle_receive = wrist_rotation(base, base_cyclic, angle)
                        
        # Read the data from the serial port and decode it
        analog_value = arduino.readline().decode("latin")
        print(analog_value)
        test_csv.write(f"{angle_receive}, {analog_value}")  

        pygame.display.flip()
        #clock.tick(30)
        

except Exception as e:
    raise e
finally:

    test_csv.close()

    # Cleanup
    pygame.quit()
    #arduino.close()

