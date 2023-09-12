import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None)


class RK4(object):

    # Encabezados
    headerRK4=list(("x","y/y'","k1","k2","k3","k4"))
    # header=list(("x","y","k1","k2","k3","k4","Error",""))

    # Constructor
    def __init__(self, initialValue:list, point:float, h_value:float, eq="0") -> None:
        self._initialValue = initialValue
        self.h_value = h_value
        self.solTab = np.zeros((2,6),dtype=float)
        self.point = point
        self.eq = eq

    # Lo que muestra al llamar la función print
    def __str__(self) -> str:
        self.rkmMethod()
        return "Objeto de tipo Método Runge-Kutta"

    # Método de Runge-Kutta-4
    def rk4(self):
        self.firstRowOrder4()
        self.iterationsOrder4()
        #return pd.DataFrame(self.solTab, columns=self.headerRK4)
        return pd.DataFrame(self.solTab, columns=self.headerRK4)

    # Método para crear la primera iteración de RK4
    def firstRowOrder4(self)->None:
        t,x,y = self._initialValue[0], self._initialValue[1], self._initialValue[2]
        self.solTab[0,0] = t
        self.solTab[1,0] = t
        self.solTab[0,1] = x
        self.solTab[1,1] = y
        #k1
        self.solTab[0,2] = self.k1x(t,x,y)
        self.solTab[1,2] = self.k1y(t,x,y)
        #k2
        self.solTab[0,3] = self.k2x(t,x,y,self.solTab[0,2],self.solTab[1,2])
        self.solTab[1,3] = self.k2y(t,x,y,self.solTab[0,2],self.solTab[1,2])
        #k3
        self.solTab[0,4] = self.k3x(t,x,y,self.solTab[0,3],self.solTab[1,3])
        self.solTab[1,4] = self.k3y(t,x,y,self.solTab[0,3],self.solTab[1,3])
        #k4
        self.solTab[0,5] = self.k4x(t,x,y,self.solTab[0,4],self.solTab[1,4])
        self.solTab[1,5] = self.k4y(t,x,y,self.solTab[0,4],self.solTab[1,4])

    # Método para crear el resto de las iteraciones de RK4
    def iterationsOrder4(self:float):
        #rango = int(np.abs((self._initialValue[0]-self.point)/self.h_value))
        t,x,y=0,0,0
        fp = int(np.abs((self._initialValue[0]-self.point)/self.h_value))
        for i in range(0,fp):
            un = np.zeros(shape=(2,6))
            t = self.solTab[2*i,0] + self.h_value
            x = self.solTab[2*i,1]
            y = self.solTab[2*i+1, 1]
            #Relleno de siguiente iteracion
            un[0,0] = t
            un[1,0] = t
            un[0,1] = self.get_u(u=x, k1=self.solTab[2*i,2], k2=self.solTab[2*i,3], k3=self.solTab[2*i,4], k4=self.solTab[2*i,5])
            un[1,1] = self.get_u(u=y, k1=self.solTab[2*i+1,2], k2=self.solTab[2*i+1,3], k3=self.solTab[2*i+1,4], k4=self.solTab[2*i+1,5])
            x = un[0,1]
            y = un[1,1]
            #k1
            un[0,2] = self.k1x(t,x,y)
            un[1,2] = self.k1y(t,x,y)
            #k2
            un[0,3] = self.k2x(t,x,y,un[0,2],un[1,2])
            un[1,3] = self.k2y(t,x,y,un[0,2],un[1,2])
            #k3
            un[0,4] = self.k3x(t,x,y,un[0,3],un[1,3])
            un[1,4] = self.k3y(t,x,y,un[0,3],un[1,3])
            #k4
            un[0,5] = self.k4x(t,x,y,un[0,4],un[1,4])
            un[1,5] = self.k4y(t,x,y,un[0,4],un[1,4])
            self.solTab = np.append(self.solTab,un, axis=0)
            del un,t,x,y

    # Métodos para obtener las k de x
    def k1x(self, t:float, x:float, y:float) -> float:
        return self.fx(t,x,y)

    def k2x(self, t:float, x:float, y:float, k1x:float, k1y:float) -> float:
        return self.fx(t + self.h_value/2, x + k1x * self.h_value /2, y + k1y * self.h_value /2)

    def k3x(self, t:float, x:float, y:float, k2x:float, k2y:float)-> float:
        return self.fx(t + self.h_value/2, x + k2x * self.h_value /2, y + k2y * self.h_value /2)

    def k4x(self, t:float, x:float, y:float, k3x:float, k3y:float)-> float:
        return self.fx(t + self.h_value, x + k3x * self.h_value, y + k3y * self.h_value )

    #Métodos para obtener las k de y
    def k1y(self, t:float, x:float, y:float) -> float:
        return self.fy(t,x,y)

    def k2y(self, t:float, x:float, y:float, k1x:float, k1y:float) -> float:
        return self.fy(t + self.h_value/2, x + k1x * self.h_value /2, y + k1y * self.h_value /2)

    def k3y(self, t:float, x:float, y:float, k2x:float, k2y:float)-> float:
        return self.fy(t + self.h_value/2, x + k2x * self.h_value /2, y + k2y * self.h_value /2)

    def k4y(self, t:float, x:float, y:float, k3x:float, k3y:float)-> float:
        return self.fy(t + self.h_value, x + k3x * self.h_value, y + k3y * self.h_value )

    #Siguiente valor de x y de y
    def get_u(self,u:float, k1:float, k2:float, k3:float, k4:float)->float:
        """Return the next y with a global error of O(h^3)"""
        return u + (k1 + 2 * k2 + 2 * k3 + k4) * self.h_value/6


    # Esta función recibirá una cadena que representará la función, usaremos la función "eval"
    def fx(self, x:float, y:float, y1:float)->float:
        """This is the equation we want to get the numeric solution"""
        # Notita: las variables x, y si se ocupan ¡aunque no lo parezca!
        return y1

    def fy(self, x:float, y:float, y1:float)->float:
        return eval(self.eq)

class DisparoLineal(object):
    
    # Constructor
    # Recibe los datos en el siguiente orden
    # Valores de la frontera izquierda (xi, yi)
    # Valores de la frontera derecha (xf, yf)
    # Tamaño de paso (h)
    # Primer valor propuesto para y'(x0): dy1
    # Segundo valor propuesto para y'(x0): dy2
    def __init__(self, xi:float, yi:float, xf:float, yf:float, h:float, dy1:float, dy2:float, eq="0") -> None:
        self.eq = eq
        self.xi = xi
        self.yi = yi
        self.xf = xf
        self.yf = yf
        self.h = h
        self.dy1 = dy1
        self.dy2 = dy2
        #Arreglo para guardar las tablas de RK4
        self.tabs = []
        #Arreglo para guardar las filas del metodo
        self.solTab = np.zeros((1,2),dtype=float)
        self.header=list(("y' inicial", "y final"))

    # Lo que muestra al llamar la función print
    def __str__(self) -> str:
        self.disparoLineal()
        return "Objeto de tipo Método Runge-Kutta"

    # Método de disparo lineal
    def disparoLineal(self):
        #Realiza las primeras aproximaciones por RK4 usando las propuestas de y'(x0)
        dyi1 = self.dy1
        dyi2 = self.dy2
        t1 = RK4(initialValue=(self.xi,self.yi, dyi1), point=self.xf, h_value=self.h, eq=self.eq).rk4()
        t2 = RK4(initialValue=(self.xi,self.yi, dyi2), point=self.xf, h_value=self.h, eq=self.eq).rk4()
        #Agrega ambas aproximaciones al arreglo "Tabs"
        self.tabs.append(t1)
        self.tabs.append(t2)
        #Recupera los valores finales de cada aproximacion
        yf1 = t1["y/y'"].iloc[-2]
        yf2 = t2["y/y'"].iloc[-2]
        #Agrega las primeras propuestas de y'(x0) y las aproximaciones a un nuevo DataFrame
        self.solTab[0,0] = dyi1
        self.solTab[0,1] = yf1
        un = np.zeros(shape=(1,2))
        un[0,0] = dyi2
        un[0,1] = yf2
        self.solTab = np.append(self.solTab,un, axis=0)
        #Repetirá el procedimiento hasta que encuentre una aproximacion igual al valor deseado (con 6 cifras significativas)
        while (abs(yf2-self.yf)>=0.0000001):
            #crea una nueva fila del metodo
            un = np.zeros(shape=(1,2))
            #calcula la nueva propuesta de y'(x0) inicial con los valores de las iteraciones anteriores
            dyi2 = dyi1 + ((dyi2-dyi1)/(yf2-yf1))*(self.yf-yf1)
            #Recorre en un lugar la derivada y la aproximacion más antigua
            dyi1 = self.tabs[-1]["y/y'"][1]
            yf1 = self.tabs[-1]["y/y'"].iloc[-2]
            #Calcula la nueva aproximacion con RK4 y la agrega al arreglo de tablas
            ti = RK4(initialValue=(self.xi,self.yi, dyi2), point=self.xf, h_value=self.h, eq=self.eq).rk4()
            self.tabs.append(ti)
            #print(ti)
            #Recupera el valor de la nueva aproximacion usando la tabla RK4 mas reciente
            yf2 = self.tabs[-1]["y/y'"].iloc[-2]
            #Agrega los valores obtenidos a la nueva fila y añade la fila a los datos previos
            un[0,0] = dyi2
            un[0,1] = yf2
            self.solTab = np.append(self.solTab, un, axis=0)
            del ti
        #Regresa el arreglo de tablas RK4 y la tabla del metodo    
        return self.tabs, pd.DataFrame(self.solTab, columns=self.header)