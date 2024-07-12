function MostrarMensaje(mensaje) {
    var ElementoMensaje = document.createElement('div');
    ElementoMensaje.id = 'mensaje';
    ElementoMensaje.className = 'rounded-2 text-white bg-dark ';
    ElementoMensaje.innerHTML = `
        <span class="px-2 my-3 text-white"></span>
    `;
    ElementoMensaje.querySelector('span').innerText = mensaje;
    document.body.appendChild(ElementoMensaje);
    setTimeout(function() {
        document.body.removeChild(ElementoMensaje);
    }, 2000);
}

window.onload = function() {
    var djangoMessages = document.querySelectorAll('#django-messages li');
    djangoMessages.forEach(function(item) {
        var message = item.getAttribute('data-message');
        var tags = item.getAttribute('data-tags');
        if (tags.includes('success')) {
            MostrarMensaje(message);
        }
    });

}