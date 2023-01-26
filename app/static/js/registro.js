function validacion() {
    validarRedireccion()
}
function validarRedireccion() {
if (formulario.nombre.value != 0 && formulario.apellido.value != 0 && formulario.fecha.value != 0 && formulario.movil.value != 0 && formulario.direccion.value != 0 && formulario.correo.value != 0 && formulario.clave.value != 0 ) {
    window.location = "./dashboard.html";
}
    else{
        alert("Complete todos los campos en blanco")
    }
    
}