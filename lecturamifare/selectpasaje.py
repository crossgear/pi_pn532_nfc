import sqlite3

con = sqlite3.connect('data.db')
cursor = con.cursor()
cursor.execute("select monto from pasaje")
data = cursor.fetchall()
for m in data:
    pasaje = m[0]
print(pasaje)