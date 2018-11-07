import os, sys
import signal
import time
import RPi.GPIO as GPIO
from modules.py532lib.i2c import *

def signal_handler(signal, frame):
    GPIO.cleanup()
    print('[*] Exiting...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print("Test NFC")
nfc = Pn532_i2c()           # Inicializa i2c
nfc.reset_i2c()             
nfc.SAMconfigure()          # Le indicamos al lector que configure la SAM(Secure Access Module) para actuar como lector

def proceso():
        try:  
            while 1:
                print(" >>> Pasa una tarjeta o tag por el lector NFC <<< ")  
                card_data = ""
                while card_data=="":
                    card_data = nfc.read_mifare().get_data()  # Activamos el lector para leer las tarjetas que se acerquen
                key=''.join(["%0.2X" % x for x in card_data[7:14]])
                print("NFC key: ", key)
                time.sleep(1)
                
        except (KeyboardInterrupt, SystemExit):
            print("Saliendo...")        
        return key
