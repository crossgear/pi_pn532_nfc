#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim :set tabstop=4 expandtab shiftwidth=4 softtabstop=4

import os, sys
import signal
import time

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

try:  
    while 1:
      print(" >>> Pasa una tarjeta o tag por el lector NFC <<< ")  
      card_data = ""
      while card_data=="":
        card_data = nfc.read_mifare().get_data()  # Activamos el lector para leer las tarjetas que se acerquen
      key=''.join(["%0.2X" % x for x in card_data[7:11]])[0:(2*4)]
      print("NFC key: ", key)
      time.sleep(1)
      file = open('codigo.txt','a+')
      file.write(key + '\n')
      file.close
          

except (KeyboardInterrupt, SystemExit):
    print("Saliendo...")
