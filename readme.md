# IA
## Exclusivo para 
Logs:{
    print message()
    abm logs()
    logs:[]
}
Juego:{
    tablero
    contexto
    jugadores:[]
    movimientosPosibles(estado_tablero)=moves
}
Tablero:{
    estado
    cambiar_tablero
    invertir_tablero //facilita algunas cosas
}
//Puede ser un traslado o una comida
Movimiento:{
    inicio:{x,y},
    fin{x,y},

}

Jugador:{
}

## Checkmates
https://stackoverflow.com/questions/30401046/check-of-checkmate-in-chess

https://softwareengineering.stackexchange.com/questions/378482/chess-efficiently-deciding-whether-a-check-mate-has-been-made

Resolucion facil
Soy negro, veo si alguna pieza del blanco puede matar mi rey
si la puede matar, hay alguna pieza negra que pueda comer o frenar a la blanca
Si no existe esa pieza, entonces si se puede mover el rey