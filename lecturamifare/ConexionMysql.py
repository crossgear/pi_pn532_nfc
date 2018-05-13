import mysql.connector
from mysql.connector import errorcode
key = "a27a45f2"
pasaje = 2000

try:
    cnx = mysql.connector.connect(user='pi', 
                              password='raspberry',
                              host='127.0.0.1',
                              database='prueba')

    cursor = cnx.cursor()

    cursor.execute("select * from tarjetas")

    """rows = cursor.fetchall()
    for row in rows:
        print (row)"""

    for id, uid, estado, saldo in cursor.fetchall():
      #print(id, uid.upper(), estado, saldo)
      print ("UID: {}, Estado: {}, Saldo: {}".format(uid.upper(), estado, saldo))
    
        
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
