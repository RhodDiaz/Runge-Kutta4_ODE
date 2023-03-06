import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None)

class RungeKuttas(object):
    
    # Encabezados
    header=list(("x","y","k1","k2","k3","k4","k5","Error"))

    # Constructor
    def __init__(self, initialValue:list, point:float, h_value:float, error:float = 0.0, equation:str="0") -> None:
        self._initialValue = initialValue
        self.h_value = h_value
        self.error = error
        self.solTab = np.zeros((1,len(self.header)),dtype=float)
        self.point = point
        self.equation = equation

    # Lo que muestra al llamar la función print
    def __str__(self:any) -> str:
        self.rkmMethod()
        return "Objeto de tipo Método Runge-Kutta"
    
    #region Método de Runge-Kutta-4
    def rk4(self:any):
        self.firstRowOrder4()
        self.iterationsOrder4()
        return pd.DataFrame(self.solTab, columns=self.header)[['x','y','k1','k2','k3','k4','Error']]
    
    # Método para crear la primera iteración de RK4
    def firstRowOrder4(self:any) -> None:
        x,y = self._initialValue[0], self._initialValue[1]
        self.solTab[0,0] = x
        self.solTab[0,1] = y
        self.solTab[0,2] = self.k1(x,y)
        self.solTab[0,3] = self.k2(x,y,self.solTab[0,2])
        self.solTab[0,4] = self.k3(x,y,self.solTab[0,3])
        self.solTab[0,5] = self.k4(x,y,self.solTab[0,2],self.solTab[0,3],self.solTab[0,4])

    # Método para crear el resto de las iteraciones de RK4
    def iterationsOrder4(self:any) -> None:
        rango = int(np.abs((self._initialValue[0]-self.point)/self.h_value))
        for i in range(0,rango):
            yn = np.zeros(shape=(1,len(self.header)))
            x,y = self.solTab[i,0] + self.h_value,self.solTab[i,1]
            yn[0,0] = x
            yn[0,1] = self.get_y(y=y, k1=self.solTab[i,2], k2=self.solTab[i,3], k3=self.solTab[i,4], k4=self.solTab[i,5])
            y = yn[0,1]
            yn[0,2] = self.k1(x,y)
            yn[0,3] = self.k2(x,y,yn[0,2])
            yn[0,4] = self.k3(x,y,yn[0,3])
            yn[0,5] = self.k4(x,y,yn[0,2],yn[0,3],yn[0,4])
            self.solTab = np.append(self.solTab,yn, axis=0)
            del yn,x,y

    # Métodos para obtener las k del metodo de RK4
    def k1(self, x:float, y:float) -> float:
        return self.fdexy(x,y)

    def k2(self, x:float, y:float, k1:float) -> float:
        return self.fdexy(x + self.h_value/2, y + k1 * self.h_value /2)

    def k3(self, x:float, y:float, k2:float) -> float:
        return self.fdexy(x + self.h_value/2, y + k2 * self.h_value /2)

    def k4(self, x:float, y:float, k1:float, k2:float, k3:float) -> float:
        return self.fdexy(x + self.h_value, y + k3 * self.h_value )

    def get_y(self,y:float, k1:float, k2:float, k3:float, k4:float) -> float:
        """Return the next y with a global error of O(h^3)"""
        return y + (k1 + 2 * k2 + 2 * k3 + k4) * self.h_value/6
    #endregion

    #region Método de Runge-Kutta-Merson
    def rkmMethod(self:any) -> pd.DataFrame:
        self.firstRowMerson()
        self.iterationsMerson()
        return pd.DataFrame(self.solTab, columns=self.header)[['x','y','k1','k2','k3','k4','k5','Error']]

    # Método para crear la primera iteración de Merson
    def firstRowMerson(self:any) -> None:
        x,y = self._initialValue[0], self._initialValue[1]
        self.solTab[0,0] = x
        self.solTab[0,1] = y
        self.solTab[0,2] = self.mersonk1(x,y)
        self.solTab[0,3] = self.mersonk2(x,y,self.solTab[0,2])
        self.solTab[0,4] = self.mersonk3(x,y,self.solTab[0,2],self.solTab[0,3])
        self.solTab[0,5] = self.mersonk4(x,y,self.solTab[0,2],self.solTab[0,3],self.solTab[0,4])
        self.solTab[0,6] = self.mersonk5(x,y,self.solTab[0,2],self.solTab[0,3],self.solTab[0,4],self.solTab[0,5])

    # Método para crear el resto de las iteraciones de Merson
    def iterationsMerson(self) -> None:
        rango = int(np.abs((self._initialValue[0]-self.point)/self.h_value))
        for i in range(0,rango):
            yn = np.zeros(shape=(1,8))
            x,y = self.solTab[i,0] + self.h_value,self.solTab[i,1]
            yn[0,0] = x
            yn[0,1] = self.get_yMerson(y=y, k1=self.solTab[i,2], k3=self.solTab[i,4], k4=self.solTab[i,5], k5=self.solTab[i,6])
            y = yn[0,1]
            yn[0,2] = self.mersonk1(x,y)
            yn[0,3] = self.mersonk2(x,y,yn[0,2])
            yn[0,4] = self.mersonk3(x,y,yn[0,2],yn[0,3])
            yn[0,5] = self.mersonk4(x,y,yn[0,2],yn[0,3],yn[0,4])
            yn[0,6] = self.mersonk5(x,y,yn[0,2],yn[0,3],yn[0,4],yn[0,5])
            self.solTab = np.append(self.solTab,yn, axis=0)
            del yn,x,y

    # Esta función recibirá una cadena que representará la función, usaremos la función "eval"
    def fdexy(self,x:float, y:float) -> float:
        """This is the equation we want to get the numeric solution"""
        # Notita: las variables x, y si se ocupan ¡aunque no lo parezca!
        return eval(self.equation)

    # Métodos para obtener las k del metodo de Merson
    def mersonk1(self, x:float, y:float) -> float:
        return self.h_value * self.fdexy(x,y)

    def mersonk2(self, x:float, y:float, k1:float) -> float:
        return self.h_value * self.fdexy(x + self.h_value/3, y + k1/3)

    def mersonk3(self, x:float, y:float, k1:float, k2:float) -> float:
        return self.h_value * self.fdexy(x + self.h_value / 3, y + k1/6 + k2/6)

    def mersonk4(self, x:float, y:float, k1:float, k2:float, k3:float) -> float:
        return self.h_value * self.fdexy(x + self.h_value / 2, y + k1 / 8 + 3/8 * k3)

    def mersonk5(self,x:float,y:float, k1:float, k2:float, k3:float, k4:float) -> float:
        return self.h_value * self.fdexy(x + self.h_value, y + k1/2 - 3/2 * k3 + 2*k4)

    def mersonk6(self, x:float, y:float, k1:float, k2:float, k3:float, k4:float, k5:float) -> float:
        return self.h_value * self.fdexy(x + self.h_value/2, y - 8/27*k1 + 2*k2 - 3544/2565*k3 + 1859/4104*k4 - 11/40*k5)

    # Regresa la y de Merson
    def get_yMerson(self,y:float, k1:float, k3:float, k4:float, k5:float) -> float:
        """Return the next y with a global error of O(h^4)"""
        return y + (k1 + 4*k4 + k5)/6
    
    #endregion
