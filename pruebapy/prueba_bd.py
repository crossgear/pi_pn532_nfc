import pymysql

db = pymysql.connect(host = "localhost", 
    port = "3306", 
    user = "pi", 
    passwd = "raspberry",
    db = "prueba",
    unix_socket="/var/run/mysqld/mysqld.sock")

try:
    with db.cursor() as cursor:
        sql = "SELECT id, uid, estado, saldo FROM tarjetas"

        cursor.execute(sql)
        for row in cursor:
            Id = row[0]
            Uid = row[1]
            Estado = row[2]
            Saldo = row[3]
            print("Id: ",Id,"UID: ",Uid, "Estado: ",Estado,"Saldo: ",Saldo)
except pymysql.err as e:
    print("Error %d: %s" % (e.args[0], e.args[1]))

finally:
    db.close()

    #