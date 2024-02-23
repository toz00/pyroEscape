#!/bin/python3

# Example of Pyro4 client script

import sys
import random
import time
import threading
import Pyro4.core
import RPi.GPIO as GPIO
import os

time.sleep(5)

class Client():
    # Cable class

    def __init__(self):
        self.connect()  # Connect to name server and distant server script
        self.flag = [False, False, False]  # Flags for game state
        self.temps = [0, 0, 0]  # Time variables
        self.etat = [0, 0, 0, 0]  # State variables

    def connect(self):
        connected = False
        while not connected:
            try:
                self.ipserveur = "192.168.233.1"  # Pyro server IP

                # Pyro4 name server localization
                self.nameserver = Pyro4.locateNS(host=self.ipserveur, port=9090)
                # Lookup the distant object 'xxxx' on name server
                self.uri = self.nameserver.lookup("xxxx")
                # Establish connection to distant object
                self.server = Pyro4.Proxy(self.uri)
                connected = True  # Connection success

            except:
                print("Waiting for server...")
                time.sleep(5)  # Sleep 5 seconds before trying to reconnect

    def refresh(self):
        # Refresh flags, state, and time from server every 500ms
        try:
            self.flag = self.server.getflag()  # 1: run, 2: win, 3: lost, 4: reset, 5: flash
            self.etat = self.server.getetat()  # List of 5 integers representing state
            self.temps = self.server.gettemps()  # 1: time, 2: additional time
            
        except:
            # Automatic reconnection if connection lost
            print("Connection lost. REBINDING...")
            print("(Restart the server now)")
            self.server._pyroReconnect()
            time.sleep(5)
            
        threading.Timer(0.5, script.refresh).start()

script = Client()  # Create client instance
script.refresh()

# Setup GPIO pins
jack1 = 17
jack2 = 18
jack3 = 27
jack4 = 22
relay = 21

GPIO.setup(jack1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(jack2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(jack3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(jack4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(relay, GPIO.OUT, initial=GPIO.LOW)

# Infinite loop for game
while True:
    try:
        if script.flag[0] == True:
            if GPIO.input(jack1) == False and GPIO.input(jack2) == False and GPIO.input(jack3) == False and GPIO.input(jack4) == False:
                GPIO.output(relay, GPIO.HIGH)
                script.server.changeetat(0, 1)
            else:
                GPIO.output(relay, GPIO.LOW)
        elif script.flag[1] == False and script.flag[2] == False:
            script.server.changeetat(0, 0)
            GPIO.output(relay, GPIO.LOW)

        time.sleep(0.3)
    except KeyboardInterrupt:
        GPIO.cleanup()
