
from math import sqrt
import random
import time
from MCST_madelinette import uct_search


#un movimiento es una tupla de tuplas ((xo,yo),(xf,yf))
class UCT_strategy:
    def next_move(self,movimientos,tablero)->tuple:
        mejor_accion=uct_search(tablero)
        return mejor_accion
class Random_strategy:
    def next_move(self,movimientos,tablero)->tuple:
        

        return random.choice(movimientos)
class Interactive_strategy:
    def next_move(self,movimientos,tablero)->tuple:
        print("tus movimientos posbiles")
        for j in range(len(movimientos)):
            print(movimientos[j])
        xo=int(input("escriba el x inicial: "))
        yo=int(input("escriba el y inicial: "))
        xf=int(input("escriba el x final: "))
        yf=int(input("escriba el y final: "))
        while not self.valido(xo,yo,xf,yf,movimientos):
            print("No es valida su eleccion")
            xo=int(input("escriba el x inicial: "))
            yo=int(input("escriba el y inicial: "))
            xf=int(input("escriba el x final: "))
            yf=int(input("escriba el y final: "))
        return ((xo,yo),(xf,yf))
    def valido(self,xo,yo,xf,yf,movimientos)-> bool:
        for t in movimientos:
            m_o,m_f=t
            m_xo,m_yo=m_o
            m_xf,m_yf=m_f
            if(xo==m_xo and yo==m_yo and xf==m_xf and yf==m_yf):
                return True
        return False
class Jugador:
    def __init__(self,stategy) -> None:
        self.available_moves=[]
        self.strategy=stategy
    def cantidad_movimientos(self) -> int:
        return len(self.available_moves)
#Leo el tablero y deduzco cuales movimientos puedo hacer
    def calcular_movimientos(self,tablero) -> None:
        self.available_moves=[]
        #Esta basado en las reglas, capaz sea mejor refactorizar pero por ahora
        #remitirse al modelo
        for i in range(len(tablero)):
            fila=i//3
            columna=i%3
            #tengo una pieza en ese lugar
            if(tablero[i]==1):
                for f in [-1,0,1]:
                    for c in [-1,0,1]:
                        #no tomar la misma celda medio al pedo porque esta ocupada
                        if not(c==0 and f==0):
                            nueva_fila=fila+f
                            nueva_col=columna+c
                            #celda inocupable                           
                            if not(nueva_fila==0 and nueva_col==1):
                                #margenes del tablero
                                if(nueva_fila>=0 and nueva_fila<=2 and nueva_col>=0 and nueva_col<=2):
                                    #no existe un camino entre estas celdas
                                    #el unico camino que existe es 2,0<->2,1 y 2,1<->2,2 
                                    if  self.caminos_existentes(fila,columna,nueva_fila,nueva_col):
                                        nueva_celda=tablero[nueva_fila*3+nueva_col]
                                        #si esta vacia
                                        if(nueva_celda==0):
                                            self.available_moves.append(((fila,columna),(nueva_fila,nueva_col)))
    def caminos_existentes(self,fila,columna,nueva_fila,nueva_columna)->bool:
        if(fila==2 and columna==1):
            if(nueva_fila==2 and nueva_columna==0) or (nueva_fila==2 and nueva_columna==2):
                return True
            else:
                return False
        elif(nueva_fila==2 and nueva_columna==1):
            if(fila==2 and columna==0) or( fila==2 and columna==2):
                return True
            else:
                return False
        else:
            return True
    def next_move(self,tablero)->tuple:
        return self.strategy.next_move(self.available_moves,tablero)
class Board:
    def __init__(self) -> None:
#lista de piezas, 3x3
        self.tablero=[1,"-",-1,1,0,-1,1,0,-1]
    def inverse_board(self):
        i=0
        for _ in self.tablero:
            if(self.tablero[i]==1):
                self.tablero[i]=-1
            elif(self.tablero[i]==-1):
                self.tablero[i]=1
            i+=1
    
    def cambiar_tablero(self,movimiento,no_print=False ):
        m_o,m_f=movimiento
        m_xo,m_yo=m_o
        m_xf,m_yf=m_f
        if(not no_print):
            print("inicio y fin")
            print(m_o)
            print(m_f)
        self.tablero[m_xo*3+m_yo]=0
        self.tablero[m_xf*3+m_yf]=1
    def print_tablero(self):
        print("tablero actual")
        for i in range(3):
            print("[ "+str(self.tablero[3*i+0])+" , "+str(self.tablero[3*i+1])+" , "+str(self.tablero[3*i+2])+"]")
class Game:
    def __init__(self,jugador_1_strategy,jugador_2_strategy) -> None:
        self.board=Board()
        self.jugador_1=Jugador(jugador_1_strategy)
        self.jugador_2=Jugador(jugador_2_strategy)
        self.jugador_activo=1
        self.turnos=0
    def jugar_turno(self,no_print=False)->int:
        if(self.jugador_activo==1):
            if(not no_print):
                print("jugador 1")
            self.jugador_1.calcular_movimientos(self.board.tablero)
            if(self.jugador_1.cantidad_movimientos()==0):
                return -1
            else:
                movimiento=self.jugador_1.next_move(self.board.tablero)
                self.board.cambiar_tablero(movimiento,no_print)
        else:
            if (not no_print):
                print("jugador 2")
            self.jugador_2.calcular_movimientos(self.board.tablero)
            if(self.jugador_2.cantidad_movimientos()==0):
                return 1
            else:
                movimiento=self.jugador_2.next_move(self.board.tablero)
                self.board.cambiar_tablero(movimiento,no_print)
        self.board.inverse_board()
        self.jugador_activo=-1*self.jugador_activo
        return 0
def main_not_diplay(juegos=100):
    ganados_1=0
    ganados_2=0
    tiempo_promedio=0.0
    for i in range(juegos):
        tiempo=time.time()
        game=Game(UCT_strategy(),Random_strategy())
        juego_terminado=False
        gana_1=False
        while(not juego_terminado):
            juego_terminado = game.jugar_turno(True)==1
            if(juego_terminado):
                gana_1=True
                break
            juego_terminado = game.jugar_turno(True)==-1
            if(juego_terminado):
                gana_1=False
                break
        if(gana_1):
            ganados_1+=1
        else:
            ganados_2+=1
        tiempo_final=time.time()-tiempo
        i=i+1
        # calculo de promedio iteratico (prom[i-1]*(i-1)+valor[i])/i
        tiempo_promedio=(tiempo_promedio*(i-1)+tiempo_final)/(i)
        print("tiempo en una iteracion: "+str(tiempo_final))
    print("juegos: "+str(juegos))
    print("juegos ganados por 1: "+str(ganados_1)+" , juegos ganados por 2: "+str(ganados_2))
    print("porcentaje de victorias 1: "+str(ganados_1*1.0/juegos))
    print("tiempo promedio de partida: "+str(tiempo_promedio)) 
def main():
    print("start game")
    game=Game(UCT_strategy(),Interactive_strategy())
    juego_terminado=False
    gana_1=False
    game.board.print_tablero()
    while(not juego_terminado):
        juego_terminado = game.jugar_turno()==1
        if(juego_terminado):
            gana_1=True
            break
        game.board.print_tablero()
        juego_terminado = game.jugar_turno()==-1
        if(juego_terminado):
            gana_1=False
            break
        game.board.print_tablero()
    if(gana_1):
        print("gano 1")
    else:
        print("gano 2")
if __name__ =="__main__":
    main()