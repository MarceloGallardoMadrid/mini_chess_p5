from pickle import NONE
import time
from math import log
from math import sqrt
import random
def cambiar_tablero(tablero,movimiento,player=1)->list:
    board=tablero.copy()
    m_o,m_f=movimiento
    m_xo,m_yo=m_o
    m_xf,m_yf=m_f
    board[m_xo*3+m_yo]=0
    board[m_xf*3+m_yf]=player   
    return board
def inverse_board(tablero)->list:
    board=tablero.copy()
    i=0
    for _ in board:
        if(board[i]==1):
            board[i]=-1
        elif(board[i]==-1):
            board[i]=1
        i+=1
    return board
def calcular_madelinette_moves(tablero,player=1)->list:
    available_moves=[]
    #Esta basado en las reglas, capaz sea mejor refactorizar pero por ahora
    #remitirse al modelo
    for i in range(len(tablero)):
        fila=i//3
        columna=i%3
        #tengo una pieza en ese lugar
        if(tablero[i]==player):
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
                                if  caminos_existentes(fila,columna,nueva_fila,nueva_col):
                                    nueva_celda=tablero[nueva_fila*3+nueva_col]
                                    #si esta vacia
                                    if(nueva_celda==0):
                                        available_moves.append(((fila,columna),(nueva_fila,nueva_col)))
    return available_moves
def caminos_existentes(fila,columna,nueva_fila,nueva_columna)->bool:
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
def win_board(board):
    return len(calcular_madelinette_moves(board,-1))==0

def lose_board(board):
    return len(calcular_madelinette_moves(board,1))==0

class Nodo:
    def __init__(self,board,parent =None,cp=2/sqrt(2)) -> None:
        self.board=board
        self.parent=parent
        self.available_accion=[]
        self.hijos={}
        self.puntos=0*1.0
        self.visitas=0*1.0
        self.cp=cp
        self.crear_acciones()
    def sumar_visita(self):
        self.visitas+=1
    def sumar_puntos(self,reward):
        self.puntos+=reward
    def crear_acciones(self):
        self.available_accion=calcular_madelinette_moves(self.board)

    def is_terminal(self)->bool:
        return len(calcular_madelinette_moves(self.board))==0 and len(calcular_madelinette_moves(self.board,-1))==0
    def is_expanded(self)->bool:
        return len(self.available_accion)==0
    def expand(self):
        accion=random.choice(self.available_accion)
        self.available_accion.remove(accion)
        hijo=Nodo(cambiar_tablero(self.board,accion),self,self.cp)
        self.hijos[accion]=hijo
        return hijo
    def puntaje(self):
        return (self.puntos/self.visitas)+self.cp*(sqrt(2*self.parent.visitas/self.visitas))
    def mejor_par_accion_hijo(self):
        pass
    def mejor_accion(self)->tuple:
        mejor_puntaje=0
        mejor_accion=None
        if(len(self.hijos)!=0):
            for key in self.hijos:
                value=self.hijos[key]
                if (value.puntaje()>=mejor_puntaje):
                    mejor_puntaje=value.puntaje()
                    mejor_accion=key
        return mejor_accion
    def mejor_hijo(self):
        mejor_puntaje=0
        mejor_hijo=None
        mejor_accion=None
        if(len(self.hijos)==0):
            print("sin hijos")
            print("terminal" if self.is_terminal() else "no terminal")
        ultimo_hijo=None
        if(len(self.hijos)!=0):
            iter_hijos=0
            for key in self.hijos:
                value=self.hijos[key]
                if (value.puntaje()>=mejor_puntaje):
                    mejor_puntaje=value.puntaje()
                    
                    mejor_hijo=value
                    
                iter_hijos+=1

        return mejor_hijo
    def to_string(self):
        print("hijos")
        print(self.hijos)
        print("acciones")
        print(self.available_accion)
def uct_search(board,cp=2/sqrt(2),max_sim=50,max_time=5)->tuple:

    root=Nodo(board,None,cp)

    tiempo=0
    simulations=0
    while(tiempo<max_time and simulations<max_sim):
        t=time.time()
        vl=TREE_POLICY(root)
        reward=DEFAULT_POLICY(vl.board)
        BACKUP(vl,reward)
        tiempo=tiempo+(time.time()-t)
        simulations+=1
    
    return root.mejor_accion()
def TREE_POLICY(nodo : Nodo)->Nodo:
    vl=nodo
    iter=0
    while not vl.is_terminal():
        #print("iteraciones tree policy: "+str(iter))
        #print_not_expanded(vl)
        if not vl.is_expanded():
            #print_not_expanded(vl)
            return vl.expand()
        else:
            #print_expanded(vl)
            if(not vl.is_terminal()):
                vl=vl.mejor_hijo()
            #vl.to_string()
        iter+=1
    return vl
def print_expanded(cosa):
    print("expanded")
    print(cosa)
def print_not_expanded(cosa):
    print("not expanded")
    print(cosa)
def print_is_terminal(cosa):
    print("is_terminal")
    print(cosa)
def DEFAULT_POLICY(board):
    tablero=board.copy()
    player=1
    while not win_board(tablero) and not lose_board(tablero):
        accion=random.choice(calcular_madelinette_moves(tablero,player))
        tablero=cambiar_tablero(tablero,accion,player)
        player=-1*player
    if(win_board(tablero)):
        return 3
    else:
        return 0
def BACKUP(nodo,reward):
    while not nodo.parent == None:
        nodo.sumar_visita()
        nodo.sumar_puntos(reward)
        nodo=nodo.parent

