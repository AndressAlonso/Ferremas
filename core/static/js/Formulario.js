function motivo() {
    let slctMotivo = document.getElementById('id_lista_motivo');
    let valuemotivo = slctMotivo.value;
    let slctClasificacion = document.getElementById('id_lista_clasificacion');

    slctClasificacion.innerHTML = '';

    if (valuemotivo === "2") {
        const optionsConsulta = [
            { value: "-1", text: "- Seleccione una Clasificacion" },
            { value: "1", text: "Stock/ Precios/ Promociones/ Direcciones/ Horarios" },
            { value: "2", text: "Estado de mi despacho / retiro" },
            { value: "3", text: "Como comprar / Garantía / Servicio Técnico" },
            { value: "4", text: "Otras consultas" },
            { value: "5", text: "Estado de mi compra / pago" }
        ];
        optionsConsulta.forEach(optionData => {
            let option = document.createElement("option");
            option.value = optionData.value;
            option.text = optionData.text;
            slctClasificacion.appendChild(option);
        });
    } else if (valuemotivo === "3") {
        const optionsConsulta = [
            { value: "-1", text: "- Seleccione una Clasificacion" },
            { value: "1", text: "Cotización RUT Persona"},
            { value: "2", text: "Mis boletas o facturas de compra" },
            { value: "3", text: "Mi cuenta web" },
            { value: "4", text: "Cotización RUT Empresa" },
            { value: "5", text: "Asesoría experta online en computación" },
            { value: "6", text: "Proveedores/ Propuestas" }
        ];
        optionsConsulta.forEach(optionData => {
            let option = document.createElement("option");
            option.value = optionData.value;
            option.text = optionData.text;
            slctClasificacion.appendChild(option);
        });
    } else if (valuemotivo === "4"){
        const optionsConsulta = [
            { value: "-1", text: "- Seleccione una Clasificacion" },
            { value: "1", text: "Despacho a domicilio / Retiro en tienda"},
            { value: "2", text: "Estado de mi reembolso / Problemas con el pago"},
            { value: "3", text: "Mi experiencia en pc Factory"},
            { value: "4", text: "Garantías / Servicio técnico / Productos digitales"}
        ];
        optionsConsulta.forEach(optionData => {
            let option = document.createElement("option");
            option.value = optionData.value;
            option.text = optionData.text;
            slctClasificacion.appendChild(option);
        });
    }
}

function obtenerSeleccion(select) {
    var selectedText = select.options[select.selectedIndex].text;
    console.log("Texto seleccionado:", selectedText);
  }
  

window.onload = () => {
    GetPaises();
    let slctMotivo = document.getElementById('id_lista_motivo');
    slctMotivo.addEventListener("change", motivo);
}

function ordenarData(data) {
    data.sort((a, b) => a.name.common.localeCompare(b.name.common));
    return data
  }
  
async function GetPaises(){
    var value = 0;
    fetch('https://restcountries.com/v3.1/all?fields=name,flags,idd')
  .then(response => response.json())
  .then(data => {
    ordenarData(data);
    data.forEach(country => {
        value++
        var pais = country.name.common;
        var root = country.idd.root
        var sufijo = country.idd.suffixes ? country.idd.suffixes[0] : ''
        let selectpaises = document.querySelector("#SSTelPaises");
        let opc = document.createElement("option");
        opc.value = value
        opc.textContent = root+sufijo + " " +  pais;
        selectpaises.appendChild(opc);
        if (value === 46){
            opc.selected = true;
        }
        if (getPaisSelected = opc.textConttent){
            opc.textContent = root+sufijo;
        }
        
        
    });
  })
  .catch(error => {
    console.error('Error al obtener los datos de la API:', error);
  });

}
