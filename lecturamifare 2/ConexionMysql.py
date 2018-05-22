import mysql.connector
from mysql.connector import errorcode
#key = "a27a45f2"
key = "DE626E9A"
pasaje = 2000

try:
    cnx = mysql.connector.connect(user='pi', 
                              password='raspberry',
                              host='127.0.0.1',
                              database='prueba')

    cursor = cnx.cursor()

    #cursor.execute("select * from tarjetas")

    cursor.execute("SELECT uid, estado, saldo FROM tarjetas WHERE uid = %s", (key,))

    # con esta configuracion la base de datos devuelve cero si no existe y 1 si existe
    data = cursor.fetchall()
    #print (len(data))
   
    if len(data) == 1:
    
        for uid, estado, saldo in data:

            if (key.upper() == uid.upper()) and (estado == 1):

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
                else:
                        #saldo menor al pasaje
                        print("Saldo Insuficiente")
                        
            else:
                    #si la tarjeta esta inactiva o es desconocida
                    print("Tarjeta Inactiva o desconocida")
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
