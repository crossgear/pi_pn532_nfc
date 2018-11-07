from tkinter import *
from tkinter import ttk
import os, sys

class Aplicacion():
    def __init__(self):
        
        self.pantalla=Tk()
        #pantalla.geometry('300x200')
        self.pantalla.title('Aplicacion')
        
        #boton Pagos
        boton1 = ttk.Button(self.pantalla, text='Pagos', 
                   command=self.AbrirPago)
        boton1.grid(row=0,column=1, pady=20, padx=20)
        #boton Recarga
        boton2 = ttk.Button(self.pantalla, text='Recarga', 
                   command=self.pantalla.destroy)
        boton2.grid(row=1,column=1, pady=20, padx=50)
        #boton Consulta
        boton3 = ttk.Button(self.pantalla, text='Consulta', 
                   command=self.pantalla.destroy)
        boton3.grid(row=2,column=1, pady=20, padx=20)
        #boton salir
        boton4 = ttk.Button(self.pantalla, text='Salir', 
                   command=self.pantalla.destroy)
        boton4.grid(row=3,column=1, pady=20, padx=20)
        
        self.pantalla.mainloop()
   
    def AbrirPago(self):
        self.dialogo = Toplevel()
        def script():
            os.system('python3.6 lectura_nfc_def.py')
        #boton Realizar Pagos
        boton5 = ttk.Button(self.dialogo, text='Realizar Pagos', 
                   command=script)
        boton5.grid(row=0,column=1, pady=20, padx=20)
        #boton Devoluciones
        boton6 = ttk.Button(self.dialogo, text='Devoluciones', 
                   command=self.dialogo.destroy)
        boton6.grid(row=1,column=1, pady=20, padx=20)
        #boton Atras
        boton7 = ttk.Button(self.dialogo, text='<<Atras', 
                   command=self.dialogo.destroy)
        boton7.grid(row=2,column=1, pady=20, padx=20)
        
        
        self.dialogo.transient(master=self.pantalla)
        self.dialogo.grab_set()
        self.pantalla.wait_window(self.dialogo)

    def PagoPasaje(self):
        self.dialogo1 = Toplevel()
        
        Label(self.dialogo1, text="show something here").grid(row=0,column=1, pady=20, padx=20)
        
        #boton Realizar Pagos
        boton8 = ttk.Button(self.dialogo1, text='<<volver', 
                   command=self.dialogo1.destroy)
        boton8.grid(row=1,column=1, pady=20, padx=20)
        
        self.dialogo1.transient(master=self.pantalla)
        self.dialogo1.grab_set()
        self.pantalla.wait_window(self.dialogo1)
        
def main():
    mi_app = Aplicacion()
    return 0
        
if __name__=='__main__':
    main()