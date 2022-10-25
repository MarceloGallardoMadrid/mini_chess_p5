
from math import log
from math import sqrt


#Aca va el montecarlo search tree
time_limit =3.0
simulations_limit=100.0
cp = 1.0/2.0*sqrt(2.0)
class Action:
    def __init__(self,accion:tuple) -> None:
        self.accion=accion
        self.visited=False
    def visitar(self)->None:
        self.visited=True
class MCST_node:
    def __init__(self,board=None,action=None,parent=None) -> None:
        #No se aconseja guardar todo el tablero pero por ahora no se me ocurre nada
        self.board=board
        self.simulated_board=board
        #por ahora es una tupla
        self.prev_action=action
        self.parent=parent
        self.available_moves=[]
        self.visits=0
        self.points=0
        self.create_moves()
    def is_terminal(self)->bool:
        return len(self.available_moves)==0
    def is_terminal_win(self)->bool:
        inverse_board(self.board)
        moves=calcular_madelinette_moves(self.board)
        return len(moves)==0
    def create_moves(self)->None:
        moves=calcular_madelinette_moves(self.board)
        for m in moves:
            self.available_moves.append(Action(m))
    def full_expanded(self)->bool:
        for ac in self.available_moves:
            if(not ac.visited):
                return False
        return True
    def select_node(self)->tuple:
        #biased porque elijo el primero posible, esta mal 
        for ac  in self.available_moves:
            if(not ac.visited):
                ac.visitar()
                return ac
    def value_of_node(self,value)->float:
        exploit=1.0*self.points/self.visits
        explore=value*sqrt(2.0*log(2.0*self.parent.visits)/(1.0*self.visits))
        return exploit+explore
def terminal_win(board):
    inverse_board(board)
    moves=calcular_madelinette_moves(board)
    return len(moves)==0
def terminal_lose(board):
    moves=calcular_madelinette_moves(board)
    return len(moves)==0
def cambiar_tablero(tablero,movimiento)->list:
    m_o,m_f=movimiento
    m_xo,m_yo=m_o
    m_xf,m_yf=m_f
    tablero[m_xo*3+m_yo]=0
    tablero[m_xf*3+m_yf]=1   
    return tablero
# no va por aca
# lo debo hacer de vuelta
#no me gusta nada nada nada nada nada nada nada
def inverse_board(tablero):
    i=0
    for _ in tablero:
        if(tablero[i]==1):
            tablero[i]=-1
        elif(tablero[i]==-1):
            tablero[i]=1
        i+=1
#El board tiene que ser el board peladitos, un list
def monte_carlo_search(root,board)->tuple:
    simulations=0
    time=simulations_limit
    root=MCST_node(board)
    while(time>0 or simulations<simulations_limit):
        tiempo_actual=time()
        node=tree_policy(root)
        reward=default_policy(node.board)
        backup(node,reward)
        simulations=simulations+1
        time=time-(time()-tiempo_actual)
    return best_move(root)
def tree_policy(nodo : MCST_node)->MCST_node:
    #Debo encontrar la manera de revisar si es terminal win or terminal lose
    while not nodo.is_terminal():
        if not nodo.full_expanded():
            return expand(nodo)
        else:
            nodo=best_child(nodo,cp)
    return nodo
def default_policy(board)-> int:
    end=-1 if terminal_lose(board) else 0
    end=1 if terminal_win(board) and not end==-1 else 0
    while end==0:

        end=-1 if terminal_lose(board) else 0
        end=1 if terminal_win(board) and not end==-1 else 0
def expand(node : MCST_node)->MCST_node:

    pass
def best_child(nodo : MCST_node, valor)-> MCST_node:
    pass
def backup(nodo:MCST_node, reward)->None:
    pass
def best_move(board)->tuple:
    pass
def calcular_madelinette_moves(tablero)->list:
    available_moves=[]
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
