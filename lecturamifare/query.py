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

con = sqlite3.connect('data.db')
cursor = con.cursor()

cursor.execute('SELECT numero FROM numero_documentos')
data = cursor.fetchall()
for d in data:
    numdoc = d[0]
print(numdoc)

result = numdoc + 1

print(result)

cursor.execute("insert into numero_documentos values(?);", [result])
con.commit()#####IMPORTANTE!!!!!!
cursor.execute('SELECT numero FROM numero_documentos')
data = cursor.fetchall()
for d in data:
    numdoc = d[0]
print(numdoc)

result = numdoc + 1

print(result)

cursor.execute("insert into numero_documentos values(?);", [result])

cursor.execute('SELECT numero FROM numero_documentos')
data = cursor.fetchall()
for d in data:
    numdoc = d[0]
print(numdoc)