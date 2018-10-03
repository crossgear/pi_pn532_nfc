import calculo_numdoc
import sqlite3
"""import mysql.connector

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

cnx = mysql.connector.connect(user='root', 
                              password='0961341242',
                              host='192.168.1.113',
                              database='xbus')  

cursor = cnx.cursor()

args = [timb, int(num), pasaje, lect]
print(args)
cursor.callproc('InsertarComprobante', args) """


"""con = sqlite3.connect('data.db')
cursor = con.cursor()
cursor.execute('SELECT numero FROM numeros_documentos;')
data = cursor.fetchall()
for d in data:
    numdoc = d[0]
print(numdoc)

result = numdoc + 1
    
print(result)

cursor.execute("insert into numeros_documentos values(4001044,?);", [result])
con.commit()


cursor.execute('SELECT cabecera, numero FROM numeros_documentos order by numero desc limit 1;')
for k, j in cursor:
    data=[k,j]
    d = "".join(str(data[0]))+"".join(str(data[1]))
    print(d)


con.close()"""
from calculo_numdoc import calculate
while 1:
    enter=""
    while enter=="":
        enter=input("continuar?")
        cal = calculate()
        print(cal)