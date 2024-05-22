window.onload = () => {
  GetIndicador();
};

async function GetIndicador() {
  var cont = 0;
  fetch("https://mindicador.cl/api")
    .then((response) => response.json())
    .then((datas) => {
      Object.keys(datas).forEach((data) => {
        let selectindicador = document.getElementById("ssindicador");
        if (
          data === "version" ||
          data === "autor" ||
          data === "fecha" ||
          data === "ivp" ||
          data === "ipc" ||
          data === "imacec" ||
          data === "libra_cobre" ||
          data === "tasa_desempleo"
        ) {
          // No hacer nada, ya que estos datos no se deben incluir
        } else {
          cont++;
          let opc = document.createElement("option");
          opc.value = cont;
          opc.textContent = data;
          selectindicador.appendChild(opc);
        }
      });
      let precioOriginal = document
        .getElementById("precioClp")
        .textContent.replace("$", "")
        .replace(".", "");
      let selectindicador = document.getElementById("ssindicador");
      selectindicador.addEventListener("change", function () {
        var selectedindex = selectindicador.selectedIndex;
        var selectedText = selectindicador.options[selectedindex].text;
        if (selectedindex > 0) {
          fetch("https://mindicador.cl/api/" + selectedText)
            .then((response) => response.json())
            .then((datas) => {
              var valorx = datas.serie[0].valor;
              var precioConvertido = precioOriginal / valorx;
              let precio = document.getElementById("precioClp");
              let divisa = document.getElementById("divisa");
              divisa.textContent = datas.codigo;
              precio.textContent = precioConvertido;
            })
            .catch((error) => {
              console.error("Error al obtener los datos de la API:", error);
            });
        } else {
          let precio = document.getElementById("precioClp");
          let divisa = document.getElementById("divisa");
          precio.textContent = precioOriginal;
          divisa.textContent = "CLP";
        }
      });
    })
    .catch((error) => {
      console.error("Error al obtener los datos de la API:", error);
    });
}
