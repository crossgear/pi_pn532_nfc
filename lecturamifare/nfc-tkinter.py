from tkinter import *
import binascii
import socket
import sys
import os, sys
import signal
import time
import RPi.GPIO as GPIO
import threading
from modules.py532lib.i2c import *

root = Tk()
root.className = "TeamBadoy"
root.geometry("800x480")
welcome = Label(root,text="Bienvenido al Sistema de Pago")
welcome.pack()
welcome.config(font=("Gothic", 18))
back = Frame(width=800, height=480)
back.pack()

"""instruction = Label(master=back, text='Desliza Tu Tarjeta Aqui!')
instruction.pack()
instruction.config(font=("Gothic", 30))
instruction.grid(row=0, column=1, padx=0, pady=150)"""

#def signal_handler(signal, frame):
#    GPIO.cleanup()
#    print('[*] Exiting...')
#    sys.exit(0)

#signal.signal(signal.SIGINT, signal_handler)
#print("Test NFC")
nfc = Pn532_i2c()
nfc.reset_i2c()             
nfc.SAMconfigure()

def proceso():
        try:  
            while 1:
                print(" >>> Pasa una tarjeta o tag por el lector NFC <<< ")  
                card_data = ""
                while card_data=="":
                    card_data = nfc.read_mifare().get_data()  # Activamos el lector para leer las tarjetas que se acerquen
                key=''.join(["%0.2X" % x for x in card_data[7:14]])
                #print("NFC key: ", key)
                ins = Label(master=back, text=key)
                #ins.pack()
                ins.config(font=("Gothic", 30))
                ins.grid(row=1, column=1, padx=0, pady=150)
                time.sleep(1)
                
        except (KeyboardInterrupt, SystemExit):
            print("Saliendo...")   

thread = threading.Thread(target=proceso)
#make test_loop terminate when the user exits the window
thread.daemon = True 
thread.start()


root.mainloop()