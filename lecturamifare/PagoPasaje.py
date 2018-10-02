#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import os, sys
import signal
import time
import sqlite3
from datetime import datetime, date, timedelta
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
        key=''.join(["%0.2X" % x for x in card_data[7:11]])
        print (key)
        time.sleep(1)
        #--- Consulta BD Interna----

        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        cursor.execute('SELECT monto FROM pasaje')
        data = cursor.fetchall()
        for m in data:
            pasaje = m[0]#pasaje actual
            
        cursor.execute('SELECT id, num_doc_ini FROM timbrados;')
        data = cursor.fetchall()
        for n in data:
            timb = n[0]#id timbrado 
            num = n[1]#num_doc_ini

        cursor.execute('SELECT id FROM lectores;')
        data = cursor.fetchall()
        for i in data:
            lect = i[0]#id lector
        
        fecha = datetime.now().date()
        
        #--- Consulta BD Externa----       
        try:
            #nos conectamos a la base de datos
            cnx = mysql.connector.connect(user='root', 
                              password='0961341242',
                              host='192.168.1.113',
                              database='xbus')  

            cursor = cnx.cursor()
            
            #ejecutamos una consulta a la base de datos pidiendo los campos uid, fecha_vencimiento, estado, saldo_actual
            cursor.execute ("SELECT uid, estado, saldo_actual, fecha_vencimiento FROM tarjetas WHERE uid = %s", (key,))
            
            #obtenermos los datos y lo guardamos en una variable
            data = cursor.fetchall()

            if len(data) == 1:#si recibo algo continua el script
                #--------------------------------------------------------#
                for uid, estado, saldo_actual, fecha_vencimiento in data:
                
                    if estado == 1 :
                        
                        fecha = datetime.now().date()
                        fecha_dada = fecha_vencimiento
                    
                        if str(fecha_dada) > str(fecha):
            
                            if (key.upper() == uid.upper()):
                                #si el uid es igual al key que acabamos de capturar y el estado es 1 osea activo
                                #consultamos el monto del pasaje

                                if(saldo_actual >= pasaje):
                                    try:
                                        cursor.execute ("UPDATE tarjetas "
                                                            "SET saldo_actual = saldo_actual - %s "
                                                            "WHERE uid = %s", (pasaje, uid))
                                        
                                        args = [timb, int(num), lect]
                                        cursor.callproc('InsertarComprobante', args)    
                                        
                                        cnx.commit()
                                        print("-----PAGADO-----")#Verde
                                    except mysql.connector.Error as err:
                                        print(err)
                                    finally: 
                                        color(100, 50, 100, 3)
                                        time.sleep(0.5)
                                else:
                                    #si el saldo es menor al precio del pasaje
                                    print("Saldo Insuficiente")#Azul
                                    color(100, 100, 0, 3)
                                    time.sleep(0.5)

                        else:
                            #si la tarjeta esta vencida = Amarillo
                            print("Tarjeta Vencida")
                            color(0, 0, 100, 3)
                            time.sleep(0.5)


                    else:
                        #si la tarjeta esta inactiva - Rojo
                        print("Tarjeta Inactiva")
                        color(0, 100, 100, 3)
                        time.sleep(0.5)

            else:#caso contrario no existe la tarjeta en el sistema
                
               print("Tarjeta Desconocida")


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
