import pandas as pd
from numpy import zeros, empty, append
pd.set_option('display.max_rows', None)

RK4_HEADER=list(("t","x/y","k1","k2","k3","k4"))
ABM_HEADER=list(("t","x/y Pred", "f(x,y) Pred","x/y Corr", "f(x,y) Corr"))


class AdBaMo(object):

    # Encabezados
    RK4_HEADER=list(("t","x/y","k1","k2","k3","k4"))
    ABM_HEADER=list(("t","x/y Pred", "f(x,y) Pred","x/y Corr", "f(x,y) Corr"))
    # header=list(("x","y","k1","k2","k3","k4","Error",""))

    # Constructor
    def __init__(self, initialValue:list, point:float, h_value:float, eqx:str="0", eqy="0") -> None:
        self._initialValue = initialValue
        self.h_value = h_value
        self.solTab = zeros((2,6),dtype=float)
        self.solTabABM = empty((2,5), dtype=float)
        self.point = point
        self.eqx = eqx
        self.eqy = eqy

    # Lo que muestra al llamar la función print
    def __str__(self) -> str:
        self.rkmMethod()
        return "Objeto de tipo Método Runge-Kutta"

    # Método de Runge-Kutta-4
    def rk4(self):
        self.firstRowOrder4()
        self.iterationsOrder4()
        self.adBaMo()
        #return pd.DataFrame(self.solTab, columns=self.headerRK4)
        return [
            pd.DataFrame(self.solTab, columns=self.RK4_HEADER),
            pd.DataFrame(self.solTabABM, columns=self.ABM_HEADER).drop([0,1])
        ]

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
        for i in range(0,3):
            un = zeros(shape=(2,6))
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
            self.solTab = append(self.solTab,un, axis=0)
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
    def fx(self, t:float, x:float, y:float)->float:
        """This is the equation we want to get the numeric solution"""
        # Notita: las variables x, y si se ocupan ¡aunque no lo parezca!
        return eval(self.eqx)

    def fy(self, t:float, x:float, y:float)->float:
        return eval(self.eqy)

    #--------------------------------------------
    #Iteraciones Adams-Bashforth-Moulton
    def adBaMo(self)->None:
        t=self.solTab[7,0]+self.h_value
        xCor=self.solTab[6,1]
        yCor=self.solTab[7,1]
        fxAnteriores=[self.solTab[0,2],self.solTab[2,2],self.solTab[4,2],self.solTab[6,2]]
        fyAnteriores=[self.solTab[1,2],self.solTab[3,2],self.solTab[5,2],self.solTab[7,2]]
        while(t<=self.point):
            xPred = self.u_pred(xCor,fxAnteriores)
            yPred = self.u_pred(yCor,fyAnteriores)
            fxPred = self.fx(t,xPred,yPred)
            fyPred = self.fy(t,xPred,yPred)
            xCor = self.u_cor(xCor, fxPred, fxAnteriores)
            yCor = self.u_cor(yCor, fyPred, fyAnteriores)
            fxCor = self.fx(t,xCor,yCor)
            fyCor = self.fy(t,xCor,yCor)
            #fila = zeros(shape=(2,5))
            fila = [[t,xPred,fxPred,xCor,fxCor],
                    [t,yPred,fyPred,yCor,fyCor]]
            self.solTabABM = append(self.solTabABM,fila,axis=0)
            fxAnteriores.pop(0)
            fxAnteriores.append(fxCor)
            fyAnteriores.pop(0)
            fyAnteriores.append(fyCor)
            t=t+self.h_value
    
    def u_pred(self, u:float, fAnt:list):
        return u + self.h_value/24 * (55*fAnt[3]-59*fAnt[2]+37*fAnt[1]-9*fAnt[0])

    def u_cor(self, u:float, fPred:float, fAnt:list):
        return u + self.h_value/24 * (9*fPred+19*fAnt[3]-5*fAnt[2]+fAnt[1])

