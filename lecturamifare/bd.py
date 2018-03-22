import mysql.connector
from mysql.connector import errorcode
key = "a27a45f2"
pasaje = 2000
try:
  cnx = mysql.connector.connect(user='root', password='0961341242',
                                 host='127.0.0.1',
                                 database='prueba')
  cursor = cnx.cursor()
  
  #query = ("SELECT estado, saldo FROM tarjetas WHERE uid = %s", (id,))
  
  #id = "a27a45f2"
  
  cursor.execute ("SELECT uid, estado, saldo FROM tarjetas WHERE uid = %s", ("a27a45f2",))
  
  #cursor.execute(query,id)
  
  #consulta = cursor.fetchall()
  #print (consulta)
  #for row in cursor.fetchall():
  #   print (row)
  #data=cursor.fetchall()
  for uid, estado, saldo in cursor:
      
    #print ("UID: {}, Estado: {}, Saldo: {}".format(uid.upper(), estado, saldo))
    #print (uid.upper(), estado, saldo)
      if (saldo >= pasaje):
        print ("todo ok")
    #elif():
    #else:
  
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
finally:
    cnx.close()