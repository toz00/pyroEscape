#!/bin/python3

import datetime
import math
import threading
import time
import random

import Pyro4  # Pyro4 library
import RPi.GPIO as GPIO  # Raspberry Pi GPIO library

time.sleep(2)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

# Server IP and port
my_ip = "192.168.233.1"
my_port = 6789

# Complete class exposition
@Pyro4.expose
# Only one unique class is created and shared between clients
@Pyro4.behavior(instance_mode="single")
class Server(object):
    # Server class

    def __init__(self):
        # Initialization of variables at server start
        # Load default values
        self.etat = [0, 1, 0, 0, 0, 0]
        self.started = False
        self.won = False
        self.lost = False
        self.temps = 0
        self.tempsadd = 0
        self.finaltime = 0
        self.tank = 0
        self.debut = time.time()
        self.rouge = GPIO.PWM(13, 50)
        self.rougeetat = 0
        self.blanc = GPIO.PWM(19, 50)
        self.blancetat = 0
        self.rouge.start(0)
        self.blanc.start(0)
        self.sens = True
        self.sensb = True
        self.alarme = False
        random.seed()
        self.texteaafficher = " "

    def ajoute2minutes(self):
        # Add two minutes to room time left
        if self.temps > 120 and self.started == True:
            self.tempsadd = self.tempsadd + 120

    # Getter for clients
    def gettemps(self):
        return [self.temps, self.tempsadd, self.finaltime]

    def getetat(self):
        return self.etat

    def getflag(self):
        return [self.started, self.won, self.lost]

    def gettank(self):
        return self.tank

    def getindice(self):
        return self.texteaafficher

    def changeetat(self, position, valeur):
        # Change one etat variable
        self.etat[int(position)] = int(valeur)

    def refresh(self):
        # Refresh function executed every 5 seconds for check and periodic stuff
        if self.started == True:
            self.temps = int(math.floor(time.time() - self.debut - self.tempsadd))
        self.checkwin()

        if self.tank < 120:
            self.alarme = True
        else:
            self.alarme = False

        threading.Timer(0.5, script.refresh).start()

    def checkwin(self):
        # Check if game is won or lost
        if self.started == True and self.won == False:
            if self.etat[0] == 1 and self.etat[2] == 1 and self.etat[1] == 1 and self.etat[3] == 1:
                self.started = False
                self.won = True
                self.finaltime = self.temps
                self.ending()

        if self.started == True and self.won == False:
            if self.temps == 1200:
                self.lost = True
                self.started = False
                self.finaltime = 1200
                self.ending()
        if self.etat[1] == 3 and self.started == True:
            self.started = False
            self.lost = True
            self.won = False
            self.finaltime = self.temps
            self.ending()

    def ending(self):
        # Executed when game lost
        print("Game over :(")

    # Set function for clients
    def settank(self, combien):
        self.tank = combien

    def setindice(self, texte):
        self.texteaafficher = texte

    def start(self):
        self.lost = False
        self.won = False
        self.started = True
        self.temps = 0
        self.tempsadd = 0
        self.etat = [0, 1, 0, 0, 0, 0]
        self.debut = time.time()
        print("Start")
        self.texteaafficher = ""

    def stop(self):
        self.lost = False
        self.won = False
        self.started = False
        self.etat = [0, 1, 0, 0, 0, 0]
        print("Stop")
        self.texteaafficher = ""
        self.finaltime = self.temps
        self.rouge.ChangeDutyCycle(100)
        self.blanc.ChangeDutyCycle(100)


myserver = Server()  # Class creation
myserver.refresh()  # Start periodic refresh

# Pyro server name IP and port
nameserver = Pyro4.locateNS(host="192.168.233.1", port=9090)
# Pyro deamon creation for this server
pyrodaemon = Pyro4.core.Daemon(host=my_ip, port=my_port)
# Join the myserver object to Pyro deamon
serveruri = pyrodaemon.register(myserver, "my name")
# Pyro name server register myserver (serveruri) with the name xxxx
nameserver.register("xxxx", serveruri)
# Pyro4 deamon start idle
pyrodaemon.requestLoop()
