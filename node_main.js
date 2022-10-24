const NEGRO="negro"
const BLANCO="blanco"
const PAWN="pawn"
const BSHP="bishop"
const HORSE="horse"
const QUEEN="queen"
const KING="king"
const NADA="nada"
//Un movimiento es mover una pieza de p1 a p2
/**
 * {
            x1:0,
            y1:0,
            x2:0,
            y2:9
    }
 */
class RandomStrategy{
    
}
class Jugador{
    constructor(strategy,color){
        this.strategy=strategy
        this.color=color
        this.moves=[]
    }
    calcular_movimimientos(tablero){
        this.moves=[]
    }
    //Ojo que puede ser una conversion
    next_move(){
        return {
            x1:0,
            y1:0,
            x2:0,
            y2:0,
            new:QUEEN
        }
    }

}
class Pieza{
    constructor(nombre,color){
        this.nombre=nombre
        this.color=color
    }
    toString(){
        let s='0'
        if(this.nombre==NADA){
            return s
        }
        if(this.color==BLANCO){
            s="w_"
        }
        else{
            s="b_"
        }
        if(this.nombre==HORSE){s+="h"}
        else if(this.nombre==BSHP){s+="bshp"}
        else if(this.nombre==QUEEN){s+="q"}
        else  if(this.nombre==KING){s+="k"}
        else if(this.nombre==PAWN){s+="p"}
        return s

    }
}
class Celda{
    constructor(x,y,pieza){
        this.x=x
        this.y=y
        this.pieza=pieza
    }
    toString(){
        return this.pieza.toString()
    }
}
function offlimit(x,y){
    if(x<0 || x>5 || y<0 || y>5){
        return {
            x:-1,
            y:-1
        }
    }
    return {
        x,
        y
    }
}
//Quiero saltar la ejecucion si es checked
//Sino ejecuto
function estaChecked(checked,cb){
    if(!checked){
        return cb()
    }
    return checked
}
class Tablero{
    constructor(){
        this.celdas=[]
        this.white_king_cell={x:-1,y:-1}
        this.black_king_cell={x:-1,y:-1}
        for(let i=0;i<6;i++){
            this.celdas.push([])
            for(let j=0;j<6;j++){
                if(i>1 && i<4){
                    this.celdas[i].push(new Celda(i,j,new Pieza(NADA,NADA)))
                }
                if(i==0){
                    if(j==0 || j ==5){
                        this.celdas[i].push(new Celda(i,j,new Pieza(HORSE,NEGRO)))
                    }
                    if(j==1 || j==4){
                        this.celdas[i].push(new Celda(i,j,new Pieza(BSHP,NEGRO)))
                    }
                    if(j==2){
                        this.celdas[i].push(new Celda(i,j,new Pieza(QUEEN,NEGRO)))
                    }
                    if(j==3){
                        this.celdas[i].push(new Celda(i,j,new Pieza(KING,NEGRO)))
                        this.black_king_cell={x:i,y:j}

                    }
                }
                if(i==1){
                    this.celdas[i].push(new Celda(i,j,new Pieza(PAWN,NEGRO)))
                }
                if(i==4){
                    this.celdas[i].push(new Celda(i,j,new Pieza(PAWN,BLANCO)))
                }
                if(i==5){
                    if(j==0 || j ==5){
                        this.celdas[i].push(new Celda(i,j,new Pieza(HORSE,BLANCO)))
                    }
                    if(j==1 || j==4){
                        this.celdas[i].push(new Celda(i,j,new Pieza(BSHP,BLANCO)))
                    }
                    if(j==2){
                        this.celdas[i].push(new Celda(i,j,new Pieza(KING,BLANCO)))
                        this.white_king_cell={x:i,y:j}
                    }
                    if(j==3){
                        this.celdas[i].push(new Celda(i,j,new Pieza(QUEEN,BLANCO)))
                    }
                }
            }
        }
    }
    copy(){

    }
    //Que pasa si es una conversion de peon a queen
    cambiarTablero(move,color_active,print=false){
        if(print){
            console.log("Inicio")
            console.log(this.celdas[move.x1][move.y1])
            console.log(this.celdas[move.x1][move.y1].pieza)
            console.log("fin")
            console.log(this.celdas[move.x2][move.y2])
        }
        if(this.celdas[move.x1][move.y1].pieza===KING){
            if(color_active===KING){
                this.white_king_cell={x:move.x2,y:move.y2}
            }
            else{
                this.black_king_cell={x:move.x2,y:move.y2}
            }
        }
        this.celdas[move.x2][move.y2].pieza=this.celdas[move.x1][move.y1].pieza
        this.celdas[move.x1][move.y1].pieza=new Pieza(NADA,NADA)
    }
    //1 gana blanco,-1 gana negro,0 nada
    isEndGame(values){
        return this.isCheckMate(values.color_active)
    }
    isCheckMate(color_active){
        let es_blanco=color_active===BLANCO
        //El otro es el que sufre el checkmate
        let otro_color=es_blanco?NEGRO:BLANCO
        let enemies={}
        let allies={}
        for(let fila in this.celdas){
            for(let celda in fila){
                if(celda.pieza.color===otro_color){
                    if(enemies[celda.pieza.nombre]){
                        enemies[celda.pieza.nombre].push(celda)
                    }
                    else{
                        enemies[celda.pieza.nombre]=[celda]
                    }

                }
                else if(celda.pieza.color===color_active){
                    if(allies[celda.pieza.nombre]){
                        allies[celda.pieza.nombre].push(celda)
                    }
                    else{
                        allies[celda.pieza.nombre]=[celda]
                    }
                }
            }
        }
        
        let checked=false
        //checked pwans
        checked = estaChecked(checked,()=>{
            if(enemies[PAWN]){
                for(let p in enemies[PAWN]){
                    let hit=null
                    if(es_blanco){
                        hit=offlimit(p.x+1,p.y+1)
                        if(hit.x!=-1 && hit.x===this.black_king_cell.x && hit.y===this.black_king_cell.y){
                            return true

                        }
                        hit=offlimit(p.x-1,p.y+1)
                        if(hit.x!=-1 && hit.x===this.black_king_cell.x && hit.y===this.black_king_cell.y){
                            return true
                        }
                        
                    }
                    else{
                        hit=offlimit(p.x+1,p.y-1)
                        if(hit.x!=-1 && hit.x===this.black_king_cell.x && hit.y===this.black_king_cell.y){
                            return true
                        }
                        hit=offlimit(p.x-1,p.y-1)
                        if(hit.x!=-1 && hit.x===this.black_king_cell.x && hit.y===this.black_king_cell.y){
                            return true
                        }
                    }
                }
            }
            return false
        })        
        return 0
    }
    toString(){
        let s="[\n"
        for(let i=0;i<6;i++){
            s+="\t["
            for(let j=0;j<6;j++){
                s+=" "+this.celdas[i][j].toString()+" "
            }
            s+="]\n"
        }
        s+="]"
        return s
    }
}
class Juego{
    constructor(jugador_1,jugador_2){
        this.tablero=new Tablero()
        this.jugador_1=jugador_1
        this.jugador_2=jugador_2
        this.color_active=BLANCO
        this.turnos=0
    }

    jugarTurno(print=false){
        let move=undefined
        if(this.color_active==BLANCO){
            if(print){
                console.log("Jugador Blanco")
            }
            this.jugador_1.calcular_movimimientos(this.tablero)
            move=this.jugador_1.next_move()
        }
        else{
            if(print){
                console.log("Jugador Negro")
            }
            this.jugador_2.calcular_movimimientos(this.tablero)
            move=this.jugador_2.next_move()
        }

        if(move){
            this.tablero.cambiarTablero(move,this.color_active,print)
            let res = this.tablero.isEndGame({color_active:this.color_active})
            this.color_active=this.color_active===BLANCO?NEGRO:BLANCO
            return res
        }
        else{
            console.log("Che el movimiento esta vacio")
            return 10
        }
    }
    log(){
        console.log(this.tablero.toString())
    }
}
function main(){
    console.log("Empezando el juego")
    let juego =new Juego(new Jugador("nada","nada"),new Jugador("nada","nada"))
    juego.log()
    let game_res=0
    let iteraciones=0
    
    while(game_res===0 && iteraciones<2){
        game_res=juego.jugarTurno(true)
        iteraciones++
    }
   
    if(game_res==1){
        console.log("Gano el blanco")
    }
    else if(game_res==-1){
        console.log("Gano el negro")
    }
    else{
        console.log("Murio en madrid")
    }

}
main()