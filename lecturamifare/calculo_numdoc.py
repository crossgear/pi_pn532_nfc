import sqlite3

def calculate():
    try:
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        cursor.execute('SELECT cabecera, numero FROM numeros_documentos order by numero desc limit 1;')
        for k, j in cursor:
            data=[k,j]
        d = "".join(str(data[0]))+"".join(str(data[1]))
        
        result = j + 1
        
        cursor.execute("insert into numeros_documentos values(4001044,?);", [result])
        
        con.commit()
            
    except sqlite3.Error as err:
        print(err)
    
    return d