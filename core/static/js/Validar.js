function validarInput(inputID) {
  let input = document.getElementById(inputID);
  if (input.id === "id_lista_motivo"){
    document.addEventListener("DOMContentLoaded", function () {
      if (input.selectedIndex === 0) {
        input.classList.add("incorrect");
        input.classList.remove("correct");
      }
    });
    input.addEventListener("change", function () {
      if (input.selectedIndex !== 0) {
        input.classList.remove("incorrect");
        input.classList.add("correct");
        console.log(input.selectedIndex);
      } else {
        let ssclasi = document.getElementById("id_lista_clasificacion");
        ssclasi.classList.add("incorrect")
        ssclasi.classList.remove("correct")
        input.classList.add("incorrect");
        input.classList.remove("correct");
      }
    });
  }
  if (input.id === "id_lista_clasificacion"){
    document.addEventListener("DOMContentLoaded", function () {
      if (input.selectedIndex === 0) {
        input.classList.add("incorrect");
        input.classList.remove("correct");
      }
    });
    input.addEventListener("change", function () {
        if (input.selectedIndex !== 0) {
        input.classList.remove("incorrect");
        input.classList.add("correct");
        console.log(input.selectedIndex);
      } else {
        input.classList.add("incorrect");
        input.classList.remove("correct");
      }
    });
  }

  
  
  if (input.value !== "") {
    input.classList.add("correct");
    input.classList.remove("incorrect");
  } else {
    input.classList.add("incorrect");
    input.classList.remove("correct");
  }

  input.addEventListener("keyup", function () {
    if (validarCampo(input)) {
      input.classList.add("correct");
      input.classList.remove("incorrect");
    } else {
      input.classList.add("incorrect");
      input.classList.remove("correct");
    }
  });
}
function validarCampo(input) {
  switch (input.id) {
    case "FormControlNombre":
    case "FormControlApellido":
      return input.value.length >= 3;
    case "FormControlRut":
      return validarRut(input.value);
    case "FormControlTelefono":
      return /^\d{9}$/.test(input.value);
    case "FormControlEmail":
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value);
      return input.value != "-1";
    case "FormControlBoleta":
      return input.value.length >= 6;
    default:
      return true;
  }
}

function validarRut(rut) {
  // Formato válido: 12345678-9
  if (!/^[0-9]+[-|‐]{1}[0-9kK]{1}$/.test(rut)) return false;

  let splitRut = rut.split("-");
  let numRut = splitRut[0];
  let digVerificador = splitRut[1].toLowerCase();

  let suma = 0;
  let multiplo = 2;

  for (let i = numRut.length - 1; i >= 0; i--) {
    suma += parseInt(numRut.charAt(i)) * multiplo;
    if (multiplo < 7) multiplo++;
    else multiplo = 2;
  }

  let resto = suma % 11;
  let dvEsperado = 11 - resto;

  if (dvEsperado === 10) {
    if (digVerificador === "k") return true;
  } else if (dvEsperado === 11 && digVerificador === "0") return true;
  else if (dvEsperado === parseInt(digVerificador)) return true;

  return false;
}
function validarFormulario() {
  const form = document.getElementById("formContacto");
  const erroresDiv = document.getElementById("errores");

  form.addEventListener("submit", function (event) {
    let mensajesError = [];
    let inputs = Array.from(document.querySelectorAll("input")).slice(3, -1);
    let selects = Array.from(document.querySelectorAll("select"));
 
    
   
    inputs.forEach((input) => {
     
      if (input.id !== "FormControlBoleta" && input.id !== "FormControlText") {
        if (input.value.trim() === "") {
          mensajesError.push("*"+`El campo ${input.name.slice(0,1).toLocaleUpperCase() + input.name.slice(1,input.name.length)} no puede estar vacío.`);
        } else if (input.classList.contains("incorrect")) {
          mensajesError.push(
            `El campo ${input.name.slice(0,1).toLocaleUpperCase() + input.name.slice(1,input.name.length)} es incorrecto, Revise el campo y vuelvalo a ingresar.`
          );
        } 
      }
    });
    selects.forEach(sltc => {
      if (sltc.classList.contains("incorrect")){
        mensajesError.push("*"+`El campo ${sltc.name.slice(0,1).toLocaleUpperCase() + sltc.name.slice(1,sltc.name.length)} tiene q ser seleccionado.`);
      }
  });
    if (mensajesError.length > 0) {
      event.preventDefault();
      erroresDiv.innerHTML = mensajesError.join("<br>");
    }
  });
}

  validarFormulario();
  validarInput("FormControlNombre");
  validarInput("FormControlApellido");
  validarInput("FormControlRut");
  validarInput("FormControlTelefono");
  validarInput("FormControlEmail");
  validarInput("id_lista_motivo");
  validarInput("FormControlBoleta");
  validarInput("id_lista_clasificacion");