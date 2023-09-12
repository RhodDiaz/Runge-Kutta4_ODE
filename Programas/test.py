import tkinter as tk

# Creamos la ventana
ventana = tk.Tk()

# Dividimos la ventana en dos columnas iguales
ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=1)

# Creamos los frames
frame1 = tk.Frame(ventana, bg="red")
frame2 = tk.Frame(ventana, bg="blue")

# Colocamos los frames en las columnas correspondientes
frame1.grid(row=0, column=0, sticky="nsew")
frame2.grid(row=0, column=1, sticky="nsew")

# Hacemos que los frames ocupen toda la fila
ventana.rowconfigure(0, weight=1)

# Mostramos la ventana
ventana.mainloop()
