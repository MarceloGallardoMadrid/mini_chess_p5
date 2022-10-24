let b;
const size=6
let b_ho_img;
let b_queen_img;
let w_queen_img;
let b_r_img;
let w_bshp_img;
let w_k_img;
let w_ho_img;
let w_pn_img;
let b_pn_img;
let w_q_img;
let w_r_img;
let b_k_img;
let b_bshp_img;

function preload(){
    b_bshp_img=loadImage('./chess/b_bshp.png')
    b_ho_img=loadImage('./chess/b_ho.png')
    b_k_img=loadImage('./chess/b_k.png')
    b_pn_img=loadImage('./chess/b_pn.png')
    b_queen_img=loadImage('./chess/b_queen.png')
    w_queen_img=loadImage('./chess/w_q.png')
    b_r_img=loadImage('./chess/b_r.png')
    w_k_img=loadImage('./chess/w_k.png')
    w_bshp_img=loadImage('./chess/w_bshp.png')
    w_ho_img=loadImage('./chess/w_ho.png')
    w_q_img=loadImage('./chess/w_q.png')
    w_pn_img=loadImage('./chess/w_pn.png')
    w_r_img=loadImage('./chess/w_r.png')
}
function initBoard(){
    b.setPiece(0,0,b_ho_img,"b_ho")
    b.setPiece(0,1,b_bshp_img,"b_bshp")
    b.setPiece(0,2,b_queen_img,"b_queen")
    b.setPiece(0,3,b_k_img,"b_k")
    b.setPiece(0,4,b_bshp_img,"b_bshp")
    b.setPiece(0,5,b_ho_img,"b_ho")
    b.setPiece(1,0,b_pn_img,"b_pn")
    b.setPiece(1,1,b_pn_img,"b_pn")
    b.setPiece(1,2,b_pn_img,"b_pn")
    b.setPiece(1,3,b_pn_img,"b_pn")
    b.setPiece(1,4,b_pn_img,"b_pn")
    b.setPiece(1,5,b_pn_img,"b_pn")
    b.setPiece(4,0,w_pn_img,"w_pn")
    b.setPiece(4,1,w_pn_img,"w_pn")
    b.setPiece(4,2,w_pn_img,"w_pn")
    b.setPiece(4,3,w_pn_img,"w_pn")
    b.setPiece(4,4,w_pn_img,"w_pn")
    b.setPiece(4,5,w_pn_img,"w_pn")
    b.setPiece(5,0,w_ho_img,"w_ho")
    b.setPiece(5,1,w_bshp_img,"w_bshp")
    b.setPiece(5,2,w_queen_img,"w_queen")
    b.setPiece(5,3,w_k_img,"w_k")
    b.setPiece(5,4,w_bshp_img,"w_bshp")
    b.setPiece(5,5,w_ho_img,"w_ho")
}
function setup(){
    createCanvas(400,400)
    b=new Board(size,width/size,height/size)
    initBoard()
    
}
function draw(){
    background(0)
    if(keyIsDown(82)){
        b.onR()
    }
    b.show()
}
function mouseClicked(){
    b.onClick(mouseX,mouseY)
}
function keyPressed(e) {
    // check if the event parameter (e) has Z (keycode 90) and ctrl or cmnd
    if (e.keyCode == 90 && (e.ctrlKey || e.metaKey)) {
      b.reverse()
    }
}