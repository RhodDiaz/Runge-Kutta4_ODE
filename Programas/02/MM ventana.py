from tkinter import Tk,Frame,Label,Entry,StringVar,Button,ttk
from matplotlib.pyplot import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Multivar import *
from Multivar import RK4_HEADER,ABM_HEADER
from math import *
import plotly.express as px
import pandas as pd
import panel as pn


class MultivariableMethods:
    def __init__(self, window:Tk) -> None:
        self.window = window
        self.window.resizable(width=False, height=False)
        self.window.title("MM.MM para EE.DD.")

        # region Frames hijos
        self.top_left_frame = Frame(self.window)
        self.top_right_frame = Frame(self.window)
        self.bottom_left_frame = Frame(self.window)
        self.bottom_right_frame = Frame(self.window)
        self.top_left_frame.grid(row=0,column=0)
        self.top_right_frame.grid(row=0,column=1)
        self.bottom_left_frame.grid(row=1,column=0)
        self.bottom_right_frame.grid(row=1,column=1)
        # endregion

        self.showks = 0
        self.showGraph = 0

        # region Etiquetas para variables de entrada:
        Label(self.top_left_frame, text='t:').grid(row=0, column=0)
        Label(self.top_left_frame, text='x:').grid(row=1, column=0)
        Label(self.top_left_frame, text='y:').grid(row=2, column=0)
        Label(self.top_left_frame, text='tf:').grid(row=3, column=0)
        Label(self.top_left_frame, text='h:').grid(row=4, column=0)
        Label(self.top_left_frame, text='x\'(t):').grid(row=5, column=0)
        Label(self.top_left_frame, text='y\'(t):').grid(row=6, column=0)
        # endregion

        # region Recolectores de datos
        self.tEntry = Entry(self.top_left_frame,textvariable=StringVar(value='0'))
        self.xEntry = Entry(self.top_left_frame, textvariable=StringVar(value='0'))
        self.yEntry = Entry(self.top_left_frame, textvariable=StringVar(value='1'))
        self.tfEntry = Entry(self.top_left_frame, textvariable=StringVar(value='0.5'))
        self.hEntry = Entry(self.top_left_frame, textvariable=StringVar(value='0.05'))
        self.xtEntry = Entry(self.top_left_frame, textvariable=StringVar(value='x*y+t'))
        self.ytEntry = Entry(self.top_left_frame, textvariable=StringVar(value='x-t'))
        #endregion
        
        # region Empacadores de recolectores
        self.tEntry.grid(row=0, column=1)
        self.xEntry.grid(row=1, column=1)
        self.yEntry.grid(row=2, column=1)
        self.tfEntry.grid(row=3, column=1)
        self.hEntry.grid(row=4, column=1)
        self.xtEntry.grid(row=5, column=1)
        self.ytEntry.grid(row=6, column=1)
        #endregion

        # Botón que inicializa los objetos que calculan los métodos
        Button (
            self.top_left_frame,
            text="Resolver",
            command=self.ALL
        ).grid(row=7,column=1)

        self.rk4m = ttk.Treeview(self.bottom_left_frame)
        self.a_b_m_m = ttk.Treeview(self.bottom_left_frame)
        
        # region Configurar columnas y encabezados
        self.rk4m["columns"] = RK4_HEADER
        self.rk4m["show"] = "headings"
        self.a_b_m_m["columns"] = ABM_HEADER
        self.a_b_m_m["show"] = "headings"

        self.to_label(RK4_HEADER, self.rk4m)
        self.to_label(ABM_HEADER, self.a_b_m_m)
        # endregion

        # region Empacar objetos Treeview en el Frame
        self.rk4m.grid(row=0,column=0, padx=20, pady=20)
        self.a_b_m_m.grid(row=1,column=0, padx=20, pady=20)

        Label(self.top_right_frame,text='Punto final:',font=('Arial',20)).grid(row=0,column=0)
        # endregion

    def ALL(self):
        self.callMultiMethod()
        self.unpackData()
        self.graph(self.results)
        self.df_to_tv(self.results[0], self.rk4m)
        self.df_to_tv(self.results[1], self.a_b_m_m)
        self.getLastPoint()
        self.printLastPoint()

    def printLastPoint(self):
        puntos = self.getLastPoint()
        Label (
            self.top_right_frame,
            text=f't: {puntos[0]:.6f}\nx(t): {puntos[1]:.6f}\ny(t): {puntos[2]:.6f}',
            font=('Arial',15)
        ).grid(row=1, column=0)

    def getLastPoint(self):
        puntoFinal = self.results[1].tail(2)
        return puntoFinal['t'].unique()[0],puntoFinal['x/y Corr'][:2].to_list()[0], puntoFinal['x/y Corr'][:2].to_list()[1]


    def callMultiMethod(self):
        t = float(self.tEntry.get())
        x = float(self.xEntry.get())
        y = float(self.yEntry.get())
        h = float(self.hEntry.get())
        tf = float(self.tfEntry.get())
        xt = self.xtEntry.get()
        yt = self.ytEntry.get()
        self.results = AdBaMo (
            initialValue=(t,x,y),
            point=tf,
            h_value=h,
            eqx=xt,
            eqy=yt
        ).rk4()

    def unpackData(self):
        self.rk4m.grid_forget()
        self.a_b_m_m.grid_forget()


    def to_label(self,header, treeview):
        for column in header:
            treeview.heading(column, text=column)
            treeview.column(column, width=100)

    def df_to_tv(self, df, treeview):
        df = df.applymap(lambda x: round(x, 6))
        treeview["columns"] = list(df.columns)
        treeview["show"] = "headings"

        self.to_label(df.columns,treeview)

        for _, row in df.iterrows():
            treeview.insert("", "end", values=list(row))

        # Borrar datos existentes y agregar nuevos datos al objeto Treeview
        treeview.delete(*treeview.get_children())
        for _, row in df.iterrows():
            treeview.insert("", "end", values=list(row))
        
        self.rk4m.grid(row=0,column=0, padx=20, pady=20)
        self.a_b_m_m.grid(row=1,column=0, padx=20, pady=20)

    def graph(self,results):
        df = pd.DataFrame()
        df['t'] = results[1][results[1].index %2 == 0][['t']].reset_index(drop=True,inplace=False)
        df['x'] = results[1][results[1].index %2 == 0][['x/y Corr']].values
        df['y'] = results[1][results[1].index %2 == 1][['x/y Corr']].values
        print(df)
        fig = px.scatter_3d (df,
            x='x',
            y='y',
            z='t'
        )
        fig.show()

        for widget in self.bottom_right_frame.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.destroy()
        fig = Figure()
        canvas = FigureCanvasTkAgg(fig, master=self.bottom_right_frame)
        ax = fig.add_subplot(111)
        ax.scatter(results[0][results[0].index %2 == 0][['t']],results[0][results[0].index %2 == 0][['x/y']],c='red')
        ax.scatter(results[0][results[0].index %2 == 1][['t']],results[0][results[0].index %2 == 1][['x/y']],c='blue')
        ax.scatter(results[1][results[1].index %2 == 0][['t']],results[1][results[1].index %2 == 0][['x/y Corr']],c='red')
        ax.scatter(results[1][results[1].index %2 == 1][['t']],results[1][results[1].index %2 == 1][['x/y Corr']],c='blue')
        canvas.get_tk_widget().grid(row=0,column=0)

        # df = px.data.iris()

root = Tk()
app = MultivariableMethods(root)
root.mainloop()
