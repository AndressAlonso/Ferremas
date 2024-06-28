document.addEventListener("DOMContentLoaded",function(){
const boton = document.querySelector('#btnCompras');
const contCompras = document.querySelector('#verCompras');
var svgabajo = document.getElementById('#flechaAbajo');
var svgarriba = document.getElementById('#flechaArriba');
boton.addEventListener('click', () => {
    if(contCompras.classList.contains('cerrado')){
        contCompras.classList.remove('cerrado');
        contCompras.classList.add('abierto');
        
    }else{
       contCompras.classList.remove('abierto');
        contCompras.classList.add('cerrado');
        svgarriba.classList.remove('d-none');
    }
});
});