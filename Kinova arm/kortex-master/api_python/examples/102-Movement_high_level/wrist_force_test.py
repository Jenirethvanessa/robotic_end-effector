import pygame
import serial
import pandas as pd
import time

import utilities
from utilities import DeviceConnection
from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from kortex_api.autogen.client_stubs.BaseCyclicClientRpc import BaseCyclicClient
from move_angular_and_cartesian import wrist_rotation


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


tool = input("Write the name of the tool: ")
open_close = input("Is the tool open or close: ")

file_suffix = f"tool_{tool}_{open_close}.csv"
wrist = open(f"wrist_{file_suffix}", "w")
angle_receive = ""
analog_value = ""

try:
    for i in range(36):
            
        with utilities.DeviceConnection.createTcpConnection(args) as router:
        # Create required services
            angle = 10
            base = BaseClient(router)
            base_cyclic = BaseCyclicClient(router)
            # Example core
            success, angle_receive = wrist_rotation(base, base_cyclic, angle)

        analog_value = arduino.readline().decode("latin")
        print(f"Analog value: {analog_value}")
        wrist.write(f"{angle_receive}, {analog_value} \n")
        wrist.flush()
       
except Exception as e:
    raise e
finally:

    wrist.close()





