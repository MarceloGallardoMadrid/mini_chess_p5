class Board{
    constructor(size,w,h){
        this.cells=[]
        this.size=size
        let color="blanco"
        let last_move=null
        for(let j=0;j<size;j++){
            for(let i=0;i<size;i++){
                this.cells.push(new Cell(color,i*w,j*h,w,h,j*size+i))
                if(color=="blanco"){
                    color="negro"
                }
                else{
                    color="blanco"
                }
            }
            if(color=="blanco"){
                color="negro"
            }
            else{
                color="blanco"
            }
        }
        this.img=undefined
        this.hasImage=false
        this.piece=""

        this.last_id=-1;
    }
    show(){
        
        for(let c of this.cells){
            
            c.show()
        }
    }
    setPiece(i,j,img,piece){
        this.cells[i*this.size+j].setImg(img)
        this.cells[i*this.size+j].setPiece(piece)
    }
    idClicked(x,y){
        let id=-1;
        for(let i=0;i<this.cells.length;i++){
            id=this.cells[i].isClicked(x,y)
            if(id!=-1){
                return id
            }
        }
        return id
    }
    onClick(x,y){
        let id=this.idClicked(x,y)
        
        if(id!=-1){
            
            if(this.cells[id].hasImage && !this.hasImage){
                this.img=this.cells[id].img
                this.piece=this.cells[id].pieza
                this.hasImage=true
                this.last_id=id
            }
            if(!this.cells[id].hasImage && this.hasImage){
                //Hay un movimento de la pieza last_id a la pieza id
                /**
                * this.cells[last_id].setImg(cells[id].img)
                * this.cells[last_id].setPiece(cells[id].pieza)
                * cells[id].takePiece()
                */
                if(this.last_move==null){
                    this.last_move=new Traslado(this.last_id,id)
                }
                else{
                    let traslado=new Traslado(this.last_id,id)
                    traslado.setAnterior(this.last_move)
                    this.last_move=traslado
                }
                this.cells[id].setImg(this.img)
                this.cells[id].setPiece(this.piece)
                this.cells[this.last_id].takePiece()
                this.hasImage=false
                this.piece=""
                this.last_id=-1
            }
            
        }
    }
    onR(){
        if(this.hasImage){
            if(this.last_move==null){
                this.last_move=new Eliminacion(this.last_id,this.piece,this.img)
            }else{
                let eliminacion=new Eliminacion(this.last_id,this.piece,this.img)
                eliminacion.setAnterior(this.last_move)
                this.last_move=eliminacion
            }
            this.cells[this.last_id].takePiece()
            this.last_id=-1
            this.hasImage=false
            this.piece=""
        }
    }
    reverse(){
        if(this.last_move){
            if(this.last_move && this.last_move.nombre=="traslado"){
                let img=this.cells[this.last_move.id_destino].img
                let piece=this.cells[this.last_move.id_destino].pieza
                this.cells[this.last_move.id_origen].setImg(img)
                this.cells[this.last_move.id_origen].setPiece(piece)
                this.cells[this.last_move.id_destino].takePiece()
                this.last_move=this.last_move.anterior
                
            }
            if(this.last_move && this.last_move.nombre=="eliminacion"){
                this.cells[this.last_move.id].setImg(this.last_move.img)
                this.cells[this.last_move.id].setPiece(this.last_move.pieza)
                this.last_move=this.last_move.anterior
                
            }
        }
    }
}