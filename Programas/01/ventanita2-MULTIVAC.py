import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from difer import *

class App:
    def __init__(self, master):
        self.master = master
        master.title("Interfaz gráfica")
        self.showKs=0
        self.showGraph=0

        # Crear los widgets para la entrada de datos
        tk.Label(master, text="Valor x").grid(row=0, column=0)
        # self.xEntry = tk.Entry(master,textvariable=tk.StringVar(value="0"),width=10)
        self.xEntry = tk.Entry(master,textvariable=tk.StringVar(value=""))
        self.xEntry.grid(row=0, column=1)

        tk.Label(master, text="Valor y").grid(row=1, column=0)
        # self.yEntry = tk.Entry(master,textvariable=tk.StringVar(value="1"),width=10)
        self.yEntry = tk.Entry(master,textvariable=tk.StringVar(value=""))
        self.yEntry.grid(row=1, column=1)

        tk.Label(master, text="Valor h").grid(row=2, column=0)
        # self.hEntry = tk.Entry(master,textvariable=tk.StringVar(value=".5"),width=10)
        self.hEntry = tk.Entry(master,textvariable=tk.StringVar(value=""))
        self.hEntry.grid(row=2, column=1)

        tk.Label(master, text="Punto").grid(row=3, column=0)
        # self.pointEntry = tk.Entry(master,textvariable=tk.StringVar(value="10"),width=10)
        self.pointEntry = tk.Entry(master,textvariable=tk.StringVar(value=""))
        self.pointEntry.grid(row=3, column=1)

        tk.Label(master, text="Ecuación").grid(row=4, column=0)
        # self.eqEntry = tk.Entry(master,textvariable=tk.StringVar(value="-.06*y**(1/2)"),width=15)
        self.eqEntry = tk.Entry(master,textvariable=tk.StringVar(value=""))
        self.eqEntry.grid(row=4,column=1)

        def checkShowK():
            self.showKs += 1
            self.showKs %= 2

        def checkShowGraph():
            self.showGraph += 1
            self.showGraph %= 2

        kbuton = tk.Checkbutton(text="Mostrar k", command=checkShowK)
        kbuton.grid(row=6, column=0)

        Graficar = tk.Checkbutton(text="Graficar ", command=checkShowGraph)
        Graficar.grid(row=7, column=0)
        
        # Crear el botón para enviar los datos y mostrar el DataFrame
        self.button = tk.Button(master, text="Ejecutar", command=self.mostrar_dataframe)
        self.button.grid(row=6, column=1)

    def mostrar_dataframe(self):
        # Obtener los datos de las entradas
        x = float(self.xEntry.get())
        y = float(self.yEntry.get())
        h = float(self.hEntry.get())
        point = float(self.pointEntry.get())
        equation = self.eqEntry.get()
        window = tk.Toplevel(self.master)
        window.title("Tablas Runge-Kutta")
        mainFrame = tk.Frame(window)
        kFrame1 = tk.Frame(window)
        # titleFrame = tk.Frame(window,height=1)

        if self.showKs == 1:
            order4k = RungeKuttas(initialValue=(x,y),h_value=h, point=point, equation=equation).rk4()[['k1','k2','k3','k4']]
            mersonk = RungeKuttas(initialValue=(x,y),h_value=h, point=point, equation=equation).rkmMethod()[['k1','k2','k3','k4','k5']]
            kTable1 = tk.Text(kFrame1)
            kTable2 = tk.Text(kFrame1)
            kTable1.grid(column=0,row=0)
            kTable2.grid(column=1,row=0)
            kFrame1.grid(column=0,row=2)
            kTable1.insert(tk.INSERT,"\tValores k R-K-4\n")
            kTable1.insert(tk.END,order4k.to_string())
            kTable2.insert(tk.INSERT,"\tValores k R-K-M\n")
            kTable2.insert(tk.INSERT,mersonk.to_string())
            # titleText1.insert('1.0',"R-K-4")
            # titleText2.insert('2',"R-K-M")
            
        # print(order4)
        compactFinalTab = tk.Text(mainFrame)

        compactFinalTab.grid(column=0,row=0)

        mainFrame.grid(column=0,row=0)


        order4 = RungeKuttas(initialValue=(x,y),h_value=h, point=point, equation=equation).rk4()[["x","y"]]
        merson = RungeKuttas(initialValue=(x,y),h_value=h, point=point, equation=equation).rkmMethod()[["y"]].rename(columns={'y': 'y merson'})
        error = ((RungeKuttas(initialValue=(x,y),h_value=h,point=point, equation=equation).rk4()[["y"]] )-(RungeKuttas(initialValue=(x,y),h_value=h, point=point, equation=equation).rkmMethod()[["y"]])).rename(columns={'y': 'Error'})
        
        final = pd.concat([order4,merson,error],axis=1)
        compactFinalTab.insert('1.0', final.to_string())

        if self.showGraph == 1:
            plt.scatter(order4[["x"]],order4[["y"]],color='red',label='R-K-4')
            plt.scatter(order4[["x"]],merson[["y merson"]], color='green', label='R-K-M')
            plt.legend()
            plt.show()

root = tk.Tk()
app = App(root)
root.mainloop()
