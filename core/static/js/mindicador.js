window.onload = () => {
  GetIndicador();
};

function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
function roundNumber(num) {
  return Math.round(num);
}

async function GetIndicador() {
  var precio = document.getElementById("precioClp");
  var precioOriginal = precio.getAttribute("precio");
  var ssindicador = document.querySelector("#ssindicador");

  ssindicador.addEventListener("change", function () {
    var divisaText = ssindicador.options[ssindicador.selectedIndex].text;
    fetch("https://mindicador.cl/api/" + divisaText)
      .then((response) => response.json())
      .then((datas) => {
        var valorx = datas.serie[0].valor;
        var precioConvertido = precioOriginal / valorx;
        let precio = document.getElementById("precioClp");
        let divisa = document.getElementById("divisa");
        

        if (datas.codigo === "dolar") {
          divisa.textContent = "USD";
       
        }
        else if (datas.codigo === "euro") {
          divisa.textContent = "EUR";
          
        }
        else {
          divisa.textContent = "BTC";
        
        }
        precio.textContent = numberWithCommas(roundNumber(precioConvertido))
      })
      .catch((error) => {
        console.error("Error al obtener los datos de la API:", error);
      });

  });


}
