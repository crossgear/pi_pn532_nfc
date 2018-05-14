#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import os, sys
import signal
import time
import RPi.GPIO as GPIO
#libreria para conexion a mysql
import mysql.connector
from mysql.connector import errorcode
#libreria a utilizar para lectura nfc
from modules.py532lib.i2c import *

#----------///////Control del led a traves del GPIO///////-------------

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
red = 17
green = 18
blue = 27

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
 
Freq = 200 #Hz

RED = GPIO.PWM(red, Freq)
RED.start(100)
GREEN = GPIO.PWM(green, Freq)
GREEN.start(100)
BLUE = GPIO.PWM(blue, Freq)
BLUE.start(100)

#una funcion simple para prender los leds
def color(R, G, B, on_time):
    
    RED.ChangeDutyCycle(R)
    GREEN.ChangeDutyCycle(G)
    BLUE.ChangeDutyCycle(B)
    time.sleep(on_time)
 
    RED.ChangeDutyCycle(100)
    GREEN.ChangeDutyCycle(100)
    BLUE.ChangeDutyCycle(100)

#-----------------///////Inicio de proceso de pago//////////------------------------

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
        #---Consulta BD----
        
        pasaje = 2000 #este es una variable el pasaje actual esta entre 2200 y 3400
       
        try:
            #nos conectamos a la base de datos
            cnx = mysql.connector.connect(user='pi', 
                              password='raspberry',
                              host='127.0.0.1',
                              database='prueba')  

            cursor = cnx.cursor()
            #verificamos si existe el id en la base de datos
            cursor.execute ("SELECT uid, estado, saldo FROM tarjetas WHERE uid = %s", (key,))
          
            data = cursor.fetchall()

            if len(data) == 1:
                
                for uid, estado, saldo in data:
          
                    if (key.upper() == uid.upper()) and (estado == 1):
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
                                color(100, 50, 100, 3)
                                time.sleep(0.5)
                        else:
                            #saldo menor al pasaje
                            print("Saldo Insuficiente")
                            color(0,0,100,3)
                            time.sleep(0.5)
                            
                    else:
                        #si la tarjeta esta inactiva o es desconocida
                            print("Tarjeta Inactiva")
                            color(0, 100, 100, 3)
                            time.sleep(0.5)

            else:
                
                print("Tarjeta Desconocida!!")

              
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        finally:
            cursor.close()
            cnx.close()
        
        #-------
        
except (KeyboardInterrupt, SystemExit):

    print ("Saliendo...")
    
finally:
    GPIO.cleanup()