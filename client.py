#!/bin/python3

#exemple de script client pyro4

import sys
import random
import time
import threading
import Pyro4.core
import RPi.GPIO as GPIO
import os

time.sleep(5)


class Client():
#classe Cable  

    def __init__(self):
	
        self.connect() #connecto to name server and distant server script
        self.flag=[False,False,False] 
        self.temps=[0,0,0]
        self.etat=[0,0,0,0]

    def connect(self):
        connected=False
        while connected==False:
            try:
                self.ipserveur="192.168.233.1" #pyro server ip
                

                self.nameserver=Pyro4.locateNS(host=self.ipserveur,port=9090)  #pyro4 nameserver localisation
                self.uri = self.nameserver.lookup("xxxx")   #lookpu the distant object xxxx on name server
                self.server = Pyro4.Proxy(self.uri)  #etablish connection to distant object
                connected=True #success
				
            except:# sleep 5 secondebefore trying reconnect
                print("waiting for server")

                time.sleep(5)

    def refresh(self):  #refresh flags, state and temps from server each 500ms
        try:
            self.flag=self.server.getflag() #1: run #2 win #3 lost #4 reset #5 flash
            self.etat=self.server.getetat() #list of 5 int
            self.temps=self.server.gettemps() #1 time, #2 additionnal time
            
        except:  #Automatic reconnexion if connexion lost 
            print("Connection lost. REBINDING...")
            print("(restart the server now)")
            self.server._pyroReconnect()
            time.sleep(5)
        threading.Timer(0.5, script.refresh).start()
        
script=Client()  #
script.refresh()

jack1=17
jack2=18
jack3=27
jack4=22

relay=21

GPIO.setup(jack1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(jack2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(jack3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(jack4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(relay, GPIO.OUT, initial=GPIO.LOW)



while True:
    
#infinite loop for game 
    try:



            if script.flag[0] == True:
                if GPIO.input(jack1) == False and GPIO.input(jack2) == False and GPIO.input(jack3) == False and GPIO.input(jack4) == False:
                    GPIO.output(relay,GPIO.HIGH)
                    script.server.changeetat(0,1)
                else:
                    
                    GPIO.output(relay,GPIO.LOW)
            elif script.flag[1]==False and script.flag[2]==False:
                    script.server.changeetat(0,0)
                    GPIO.output(relay,GPIO.LOW)
            
            time.sleep(0.3)
    except KeyboardInterrupt:
        GPIO.cleanup() 


