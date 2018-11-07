import os, sys
import signal
import time
import RPi.GPIO as GPIO
from modules.py532lib.i2c import *
from tkinter import * 
from tkinter import ttk


class Aplicacion():

    def __init__(self, window):
         
        window.geometry('300x200')
        ttk.Button(window, text='Pago', 
                command=self.pago).pack(side=BOTTOM)
        ttk.Button(window, text='Salir', 
                command=window.destroy).pack(side=BOTTOM)        
        print(key)
        Label(window, text='{}').pack()
        
    
    def signal_handler(self,signal, frame):
        GPIO.cleanup()
        print('[*] Exiting...')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    print("Test NFC")
    global nfc
    nfc = Pn532_i2c()           # Inicializa i2c
    nfc.reset_i2c()             
    nfc.SAMconfigure()          # Le indicamos al lector que configure la SAM(Secure Access Module) para actuar como lector



    def pago(self):
        try:  
            while 1:
                print(" >>> Pasa una tarjeta o tag por el lector NFC <<< ")
                card_data = ""
                while card_data=="":
                    card_data = nfc.read_mifare().get_data()  # Activamos el lector para leer las tarjetas que se acerquen      
                global key
                key=''.join(["%0.2X" % x for x in card_data[7:14]])
                print(key)
                
                time.sleep(1)
            

        except (KeyboardInterrupt, SystemExit):
            print("Saliendo...")
    
    
    
if __name__ == '__main__':
    window = Tk()
    application = Aplicacion(window)
    window.mainloop()