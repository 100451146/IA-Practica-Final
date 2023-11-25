function mostrarImagen() {
    const circle = document.getElementById('circle');
    const inputImagen = document.querySelector('.circle input[name="imagen"]');
    const archivo = inputImagen.files[0];

    if (archivo) {
        const reader = new FileReader();

        reader.onload = function (e) {
            // Asigna la imagen como fondo del círculo
            circle.style.backgroundImage = `url(${e.target.result})`;
        };

        reader.readAsDataURL(archivo);
    }
}