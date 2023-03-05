import tkinter as tk
from tkinter import ttk
import pandas as pd
from difer import *

class App:
    def __init__(self, master):
        self.master = master
        master.title("Interfaz gráfica")
        self.showKs=0

        # Crear los widgets para la entrada de datos
        tk.Label(master, text="Valor x").grid(row=0, column=0)
        self.float1_entry = tk.Entry(master,textvariable=tk.StringVar(value="0"))
        self.float1_entry.grid(row=0, column=1)
        tk.Label(master, text="Valor y").grid(row=1, column=0)
        self.float2_entry = tk.Entry(master,textvariable=tk.StringVar(value="1"))
        self.float2_entry.grid(row=1, column=1)
        tk.Label(master, text="Valor h").grid(row=2, column=0)
        self.float3_entry = tk.Entry(master,textvariable=tk.StringVar(value=".5"))
        self.float3_entry.grid(row=2, column=1)
        tk.Label(master, text="Punto Llegada").grid(row=3, column=0)
        self.float4_entry = tk.Entry(master,textvariable=tk.StringVar(value="10"))
        self.float4_entry.grid(row=3, column=1)
        tk.Label(master, text="Ecuación").grid(row=5, column=0)
        self.cadena_entry = tk.Entry(master,textvariable=tk.StringVar(value="-.06*y**(1/2)"))
        self.cadena_entry.grid(row=5, column=1)

        def pres():
            self.showKs += 1
            self.showKs %= 2
            print(self.showKs)

        kbuton = tk.Checkbutton(text="Mostrar k", command=pres)
        kbuton.grid(row=6, column=0)
        # Crear el botón para enviar los datos y mostrar el DataFrame
        self.button = tk.Button(master, text="Mostrar DataFrame", command=self.mostrar_dataframe)
        self.button.grid(row=6, column=1)


    def mostrar_dataframe(self):
        # Obtener los datos de las entradas
        x = float(self.float1_entry.get())
        y = float(self.float2_entry.get())
        h = float(self.float3_entry.get())
        point = float(self.float4_entry.get())
        equation = self.cadena_entry.get()
        if self.showKs == 0:
            order4 = RungeKuttas(initialValue=(x,y),h_value=h, point=point, equation=equation).rk4()[["x","y"]]
            merson = RungeKuttas(initialValue=(x,y),h_value=h, point=point, equation=equation).rkmMethod()[["y"]]
        else:
            order4 = RungeKuttas(initialValue=(x,y),h_value=h, point=point, equation=equation).rk4()
            merson = RungeKuttas(initialValue=(x,y),h_value=h, point=point, equation=equation).rkmMethod()
        print(order4)

        # Crear un diccionario con los datos
        # data = {"Float 1": [float1], "Float 2": [float2], "Float 3": [float3], "Float 4": [float4], "Float 5": [float5], "Cadena": [cadena]}

        # Crear un DataFrame a partir del diccionario y mostrarlo en una tabla
        # order4 = pd.DataFrame(data)
        window = tk.Toplevel(self.master)
        window.title("Tablas Runge-Kutta")
        left = tk.Frame(window)
        right = tk.Frame(window)
        tableorder4 = tk.Text(left)
        tableorder4.pack()
        tableMerson = tk.Text(right)
        tableMerson.pack()
        left.grid(column=0,row=0)
        right.grid(column=1,row=0)

        # Convertir DataFrame a cadena y mostrarlo en el widget Text
        tableorder4.insert('1.0', order4.to_string())
        tableMerson.insert('1.0', merson.to_string())


        # frame.pack(fill="both", expand=True)
        # table = ttk.Treeview(frame, columns=order4.columns, show="headings")
        # table.pack(side="left", fill="both", expand=True)
        # for col in order4.columns:
        #     table.heading(col, text=col)
        # for index, row in order4.iterrows():
        #     table.insert("", "end", values=[row[col] for col in order4.columns])

root = tk.Tk()
app = App(root)
root.mainloop()
