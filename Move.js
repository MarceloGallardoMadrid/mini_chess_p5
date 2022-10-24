//Puede ser un traslado o una eliminacion
class Traslado{
    constructor(id_origen,id_destino){
        this.id_origen=id_origen
        this.id_destino=id_destino
        this.anterior=null
        this.nombre="traslado"
    }
    setAnterior(accion){
        this.anterior=accion
    }
}
class Eliminacion{
    constructor(id,pieza,img){
        this.id=id
        this.pieza=pieza
        this.img=img
        this.anterior=null
        this.nombre="eliminacion"
    }
    setAnterior(accion){
        this.anterior=accion
    }

}