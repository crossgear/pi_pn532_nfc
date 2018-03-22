#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys
import signal
import time
import RPi.GPIO as GPIO
import mysql.connector
from mysql.connector import errorcode

GPIO.setwarnings(False)

# Set GPIO to Broadcom system and set RGB Pin numbers
GPIO.setmode(GPIO.BCM)
red = 17
green = 18
blue = 27

# Set pins to output mode
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
 
Freq = 100 #Hz
 
# Setup all the LED colors with an initial
# duty cycle of 0 which is off
RED = GPIO.PWM(red, Freq)
RED.start(100)
GREEN = GPIO.PWM(green, Freq)
GREEN.start(100)
BLUE = GPIO.PWM(blue, Freq)
BLUE.start(100)

# Define a simple function to turn on the LED colors
def color(R, G, B, on_time):
    # Color brightness range is 0-100%
    RED.ChangeDutyCycle(R)
    GREEN.ChangeDutyCycle(G)
    BLUE.ChangeDutyCycle(B)
    time.sleep(on_time)
 
    # Turn all LEDs off after on_time seconds
    RED.ChangeDutyCycle(100)
    GREEN.ChangeDutyCycle(100)
    BLUE.ChangeDutyCycle(100)

#libreria a utilizar para lectura nfc
from modules.py532lib.i2c import *

print("PAGO DE PASAJE")
nfc = Pn532_i2c()           # Inicializa i2c
nfc.reset_i2c()
nfc.SAMconfigure()          # Le indicamos al lector que configure la SAM(Secure Access Module) para actuar como lector
try:
    while 1:
      print(" >>> Deslice su tarjeta porfavor <<< ")
      card_data = ""
      while card_data=="":
        card_data = nfc.read_mifare().get_data()  # Activamos el lector para leer las tarjetas que se acerquen
        key=''.join(["%0.2X" % x for x in card_data[7:11]])[0:(2*4)]
        print (key)
        time.sleep(1)
        #---Consulta BD
        #verificamos si existe el id en la base de datos
        pasaje = 2000
       
        try:
          cnx = mysql.connector.connect(user='root', password='0961341242',
                                 host='127.0.0.1',
                                 database='prueba')
          cursor = cnx.cursor()
          
          cursor.execute ("SELECT uid, estado, saldo FROM tarjetas WHERE uid = %s", ("a27a45f2",))
          
          for uid, estado, saldo in cursor:
          
              if (key == uid.upper()) and (estado == 1):
                  #---descontamos el monto del pasaje
                  if(saldo >= pasaje):
                      try:
                          cursor.execute ("UPDATE tarjetas "
                                          "SET saldo = saldo - %s "
                                          "WHERE uid = %s", (pasaje, uid))
                          
                          cnx.commit()
                          print("PAGADO")
                      except mysql.connector.Error as err:
                          print(err)
                      finally:
                          cnx.close()
                      color(100, 50, 100, 3)
                      time.sleep(0.5)
                    #--sin saldo
                  elif(saldo == 0):
                      print("Debe Cargar Saldo")
                      time.sleep(0.5)
                  else:
                      #saldo menor al pasaje
                      print("Saldo Insuficiente")
                      time.sleep(0.5)
                    
              else:
                    print("Tarjeta Inactiva o desconocida")
                    color(0, 100, 100, 3)
                    time.sleep(0.5)
              
        except mysql.connector.Error as err:
          if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
          elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
          else:
            print(err)
        finally:
            cnx.close()
            cursor.close()
        
        #-------
        
except KeyboardInterrupt:
    print ("Saliendo...")
    
finally:
    GPIO.cleanup()
