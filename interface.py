#!/bin/python3

import datetime
import math
import threading
# Importing necessary modules for networking
import socket
import select
import time
# Importing Pyro4 for remote object communication
import Pyro4.core
import Pyro4.naming

import sys

# Importing Tkinter for GUI
from tkinter import *


import tkinter.ttk as ttk




def vp_start_gui():
    '''Starting point when module is the main routine.'''
  
    root = Tk()
    top = manitobagui(root)
    
    root.mainloop()





class manitobagui:
    def __init__(self, top=None):


        self.connect()
        
        self.flag=[False,False,False]
        self.temps=[0,0,0]
        self.etat=[0,1,0,0]
        self.tank=300






# Initializing GUI components

        
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])
# Setting up GUI window
        top.geometry("600x450+650+150")
        top.title("Manitoba Manager XD")
        top.configure(background="#d9d9d9")


   # Creating buttons and labels
        self.Button1 = Button(top)
        self.Button1.place(relx=0.17, rely=0.04, height=24, width=72)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Stop/Reset''')
        self.Button1.configure(command=self.stop)

        self.Button2 = Button(top)
        self.Button2.place(relx=0.3, rely=0.04, height=24, width=72)
        self.Button2.configure(activebackground="#d9d9d9")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''Add 2 min''')
        self.Button2.configure(command=self.server.ajoute2minutes())

        self.Button3 = Button(top)
        self.Button3.place(relx=0.03, rely=0.16, height=24, width=72)
        self.Button3.configure(activebackground="#d9d9d9")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="#d9d9d9")
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(text='''Etape 1''')
        self.Button3.configure(command=lambda: self.server.changeetat(0,1))

        self.Button4 = Button(top)
        self.Button4.place(relx=0.17, rely=0.16, height=24, width=72)
        self.Button4.configure(activebackground="#d9d9d9")
        self.Button4.configure(activeforeground="#000000")
        self.Button4.configure(background="#d9d9d9")
        self.Button4.configure(disabledforeground="#a3a3a3")
        self.Button4.configure(foreground="#000000")
        self.Button4.configure(highlightbackground="#d9d9d9")
        self.Button4.configure(highlightcolor="black")
        self.Button4.configure(pady="0")
        self.Button4.configure(text='''Etape 2''')
        self.Button4.configure(command=lambda: self.server.changeetat(1,1))

        self.Button5 = Button(top)
        self.Button5.place(relx=0.3, rely=0.16, height=24, width=72)
        self.Button5.configure(activebackground="#d9d9d9")
        self.Button5.configure(activeforeground="#000000")
        self.Button5.configure(background="#d9d9d9")
        self.Button5.configure(disabledforeground="#a3a3a3")
        self.Button5.configure(foreground="#000000")
        self.Button5.configure(highlightbackground="#d9d9d9")
        self.Button5.configure(highlightcolor="black")
        self.Button5.configure(pady="0")
        self.Button5.configure(text='''Etape 3''')
        self.Button5.configure(command=lambda: self.server.changeetat(2,1))

        self.TProgressbar1 = ttk.Progressbar(top)
        self.TProgressbar1.place(relx=0.52, rely=0.35, relwidth=0.42, relheight=0.0, height=22)
        self.TProgressbar1.configure(length="250")
        self.TProgressbar1.configure(maximum="300")
        self.TProgressbar1.configure(value="300")
        self.TProgressbar1.configure(variable=self.tank)
        

        self.TLabel1 = ttk.Label(top)
        self.TLabel1.place(relx=0.62, rely=0.29, height=19, width=98)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font="TkDefaultFont")
        self.TLabel1.configure(relief=FLAT)
        self.TLabel1.configure(text='''Niveau d'oxygène''')

        self.TLabel2 = ttk.Label(top)
        self.TLabel2.place(relx=0.03, rely=0.29, height=19, width=90)
        self.TLabel2.configure(background="#d9d9d9")
        self.TLabel2.configure(foreground="#000000")
        self.TLabel2.configure(font="TkDefaultFont")
        self.TLabel2.configure(relief=FLAT)
        self.TLabel2.configure(text='''Temps écoulé:''')

        self.TLabel3 = ttk.Label(top)
        self.TLabel3.place(relx=0.03, rely=0.36, height=19, width=90)
        self.TLabel3.configure(background="#d9d9d9")
        self.TLabel3.configure(foreground="#000000")
        self.TLabel3.configure(font="TkDefaultFont")
        self.TLabel3.configure(relief=FLAT)
        self.TLabel3.configure(text='''Temps total:''')

        self.TLabel4 = ttk.Label(top)
        self.TLabel4.place(relx=0.23, rely=0.29, height=19, width=90)
        self.TLabel4.configure(background="#d9d9d9")
        self.TLabel4.configure(foreground="#000000")
        self.TLabel4.configure(font="TkDefaultFont")
        self.TLabel4.configure(relief=FLAT)
        self.TLabel4.configure(text='''tempsecoulee''')

        self.TLabel5 = ttk.Label(top)
        self.TLabel5.place(relx=0.23, rely=0.36, height=19, width=90)
        self.TLabel5.configure(background="#d9d9d9")
        self.TLabel5.configure(foreground="#000000")
        self.TLabel5.configure(font="TkDefaultFont")
        self.TLabel5.configure(relief=FLAT)
        self.TLabel5.configure(text='''tempstotal''')

        self.TLabel6 = ttk.Label(top)
        self.TLabel6.place(relx=0.03, rely=0.42, height=19, width=90)
        self.TLabel6.configure(background="#d9d9d9")
        self.TLabel6.configure(foreground="#000000")
        self.TLabel6.configure(font="TkDefaultFont")
        self.TLabel6.configure(relief=FLAT)
        self.TLabel6.configure(text='''Etat partie:''')

        self.TLabel7 = ttk.Label(top)
        self.TLabel7.place(relx=0.23, rely=0.42, height=19, width=90)
        self.TLabel7.configure(background="#d9d9d9")
        self.TLabel7.configure(foreground="#000000")
        self.TLabel7.configure(font="TkDefaultFont")
        self.TLabel7.configure(relief=FLAT)
        self.TLabel7.configure(text='''state''')

        self.TLabel8 = ttk.Label(top)
        self.TLabel8.place(relx=0.03, rely=0.49, height=19, width=90)
        self.TLabel8.configure(background="#d9d9d9")
        self.TLabel8.configure(foreground="#000000")
        self.TLabel8.configure(font="TkDefaultFont")
        self.TLabel8.configure(relief=FLAT)
        self.TLabel8.configure(text='''Temps final:''')

        self.TLabel9 = ttk.Label(top)
        self.TLabel9.place(relx=0.23, rely=0.49, height=19, width=90)
        self.TLabel9.configure(background="#d9d9d9")
        self.TLabel9.configure(foreground="#000000")
        self.TLabel9.configure(font="TkDefaultFont")
        self.TLabel9.configure(relief=FLAT)
        self.TLabel9.configure(text='''tempsfinal''')

        self.TLabel10 = ttk.Label(top)
        self.TLabel10.place(relx=0.52, rely=0.9, height=19, width=240)
        self.TLabel10.configure(background="#d9d9d9")
        self.TLabel10.configure(foreground="#000000")
        self.TLabel10.configure(font="TkDefaultFont")
        self.TLabel10.configure(relief=FLAT)
        self.TLabel10.configure(text='''messageerreur''')

        self.menubar = Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)



        self.Button6 = Button(top)
        self.Button6.place(relx=0.03, rely=0.04, height=24, width=72)
        self.Button6.configure(activebackground="#d9d9d9")
        self.Button6.configure(activeforeground="#000000")
        self.Button6.configure(background="#d9d9d9")
        self.Button6.configure(disabledforeground="#a3a3a3")
        self.Button6.configure(foreground="#000000")
        self.Button6.configure(highlightbackground="#d9d9d9")
        self.Button6.configure(highlightcolor="black")
        self.Button6.configure(pady="0")
        self.Button6.configure(text='''Start''')
        self.Button6.configure(command=self.start)

        self.Button9 = Button(top)
        self.Button9.place(relx=0.43, rely=0.16, height=24, width=72)
        self.Button9.configure(activebackground="#d9d9d9")
        self.Button9.configure(activeforeground="#000000")
        self.Button9.configure(background="#d9d9d9")
        self.Button9.configure(disabledforeground="#a3a3a3")
        self.Button9.configure(foreground="#000000")
        self.Button9.configure(highlightbackground="#d9d9d9")
        self.Button9.configure(highlightcolor="black")
        self.Button9.configure(pady="0")
        self.Button9.configure(text='''Etape 4''')
        self.Button9.configure(command=lambda: self.server.changeetat(3,1))

        self.Entry1 = Entry(top)
        self.Entry1.place(relx=0.03, rely=0.69,height=20, relwidth=0.89)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")
        self.Entry1.configure(width=534)

        self.Label1 = Label(top)
        self.Label1.place(relx=0.03, rely=0.62, height=21, width=72)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Indice:''')

        self.Button7 = Button(top)
        self.Button7.place(relx=0.17, rely=0.62, height=24, width=80)
        self.Button7.configure(activebackground="#d9d9d9")
        self.Button7.configure(activeforeground="#000000")
        self.Button7.configure(background="#d9d9d9")
        self.Button7.configure(disabledforeground="#a3a3a3")
        self.Button7.configure(foreground="#000000")
        self.Button7.configure(highlightbackground="#d9d9d9")
        self.Button7.configure(highlightcolor="black")
        self.Button7.configure(pady="0")
        self.Button7.configure(text='''Envoyer''')
        self.Button7.configure(command=self.envoieindice)

        self.Button8 = Button(top)
        self.Button8.place(relx=0.33, rely=0.62, height=24, width=80)
        self.Button8.configure(activebackground="#d9d9d9")
        self.Button8.configure(activeforeground="#000000")
        self.Button8.configure(background="#d9d9d9")
        self.Button8.configure(disabledforeground="#a3a3a3")
        self.Button8.configure(foreground="#000000")
        self.Button8.configure(highlightbackground="#d9d9d9")
        self.Button8.configure(highlightcolor="black")
        self.Button8.configure(pady="0")
        self.Button8.configure(text='''Effacer''')
        self.Button8.configure(command=self.effaceindice)

        self.refresh()


    def connect(self):
          # Function to establish connection with the server
        connected=False
        while connected==False:
            try:
                self.ipserveur="192.168.233.1" #server IP
                

                self.nameserver=Pyro4.locateNS(host=self.ipserveur,port=9090)
                self.uri = self.nameserver.lookup("manitobaserver")
                self.server = Pyro4.Proxy(self.uri)
                connected=True
            except:# or possibly CommunicationError
                print("waiting for server")

            time.sleep(5)
    def refresh(self):  #refresh flags, state and temps from server each 500ms
        try:
            self.flag=self.server.getflag() #1: run #2 win #3 lost #4 reset #5 flash
            self.etat=self.server.getetat() #list of 5 int
            self.temps=self.server.gettemps() #1 time, #2 additionnal time
            self.tank=self.server.gettank()
        except:  # or possibly CommunicationError
            print("Connection lost. REBINDING...")
            print("(restart the server now)")
            self.server._pyroReconnect()
            time.sleep(5)
    # Updating GUI components based on game state
        #self.TProgressbar1["value"]=str(self.tank)
        self.TLabel4["text"]=time.strftime("%H:%M:%S",time.gmtime(self.temps[0])) #time
        self.TLabel5["text"]=time.strftime("%H:%M:%S",time.gmtime(self.temps[0]+self.temps[1])) #additionnal time
        self.TProgressbar1["value"]=self.tank
        if self.flag[0]==True:
            self.TLabel7["text"]="En cours"
        elif self.flag[1]==True:
            self.TLabel7["text"]="Gagnée!"
        elif self.flag[2]==True:
            self.TLabel7["text"]="Perdue :("
        else:
            self.TLabel7["text"]="Stoppée"
        if self.etat[0]==1:
            self.Button3["bg"]="green"
        else:
            self.Button3["bg"]="red"
        if self.etat[2]==1:
            self.Button5["bg"]="green"
        else:
            self.Button5["bg"]="red"

        if self.etat[3]==1:
            self.Button9["bg"]="green"
        else:
            self.Button9["bg"]="red"

        if self.etat[1]==1:
            self.Button4["bg"]="green"
        else:
            self.Button4["bg"]="red"


        if self.flag[1]==True or self.flag[2]==True:
            self.TLabel9["text"]=time.strftime("%H:%M:%S",time.gmtime(self.temps[2]))
        else:
            self.TLabel9["text"]="---"                               
            
            
            
            
        # Setting up periodic refresh
        threading.Timer(0.5, self.refresh).start()

    def start(self):
         # Function to start the game
        if self.flag[0]==False:
            self.server.start()

    def stop(self):
           # Function to stop/reset the game
        self.server.stop()
        self.Entry1.delete(0, END)

    def envoieindice(self):
         # Function to send an index
        self.server.setindice(self.Entry1.get())


    def effaceindice(self):
        # Function to clear the index entry field
        self.Entry1.delete(0, END)
        self.server.setindice(self.Entry1.get())
        

  

   


vp_start_gui()
