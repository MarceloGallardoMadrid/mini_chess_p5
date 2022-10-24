class Cell{
    constructor(color,x1,y1,w,h,id){
        this.id=id
        this.color=color
        this.pieza=""
        this.img=undefined
        this.hasImage=false
        this.x1=x1
        this.y1=y1
        this.w=w
        this.h=h
    }
    show(){ 
        if(this.color=="blanco"){
            fill(255)
            
        }else{
            fill(0)
        }
        rect(this.x1,this.y1,this.w,this.h)
        if(this.img){
            image(this.img,this.x1+this.w/5,this.y1+this.h/5)
        }
    }
    setImg(img){
        this.img=img
        this.hasImage=true
    }
    setPiece(piece){
        this.pieza=piece
    }
    takePiece(){
        this.img=undefined
        this.pieza=""
        this.hasImage=false
    }
    isClicked(x,y){
        if(x>=this.x1 && x<=this.x1+this.w && y>=this.y1 && y<=this.y1+this.h){
            return this.id
        }
        else{
            return -1;
        }
    }
    onClick(x,y){
        
    }


}