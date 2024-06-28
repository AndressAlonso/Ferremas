document.addEventListener("DOMContentLoaded",function(){
const boton = document.querySelector('#btnCompras');
const contCompras = document.querySelector('#verCompras');

boton.addEventListener('click', () => {
    if(contCompras.classList.contains('cerrado')){
        contCompras.classList.remove('cerrado');
        contCompras.classList.add('abierto');
    }else{
        contCompras.classList.remove('abierto');
        contCompras.classList.add('cerrado');
    }
});
});