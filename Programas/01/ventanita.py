# import sys, tkinter
# def main():
#     root = tkinter.Tk()
#     root.title("Métodos Runge-Kuttas")
#     root.resizable(width=False,height=False)
#     def quit():
#         root.destroy()
#     bar = tkinter.Menu(root)
#     fileMenu=tkinter.Menu(bar,tearoff=0)
#     fileMenu.add_command(label="Salir",command=quit)
#     bar.add_cascade(label="Archivo", menu=fileMenu)
#     root.config(menu=bar)
#     tkinter.mainloop()

# main()

# import tkinter as tk

# root = tk.Tk()

# frame1 = tk.Frame(root)
# frame2 = tk.Frame(root)

# label1 = tk.Label(frame1, text="Este es el frame 1")
# label1.pack()

# label2 = tk.Label(frame2, text="Este es el frame 2")
# label2.pack()

# frame1.pack(side="left")
# frame2.pack(side="right")

# root.mainloop()

import tkinter as tk
import tkinter.font as tkfont
root = tk.Tk()
font = tkfont.Font(family="Consolas", size=10, weight="normal")
m_len = font.measure("m")
print(m_len)