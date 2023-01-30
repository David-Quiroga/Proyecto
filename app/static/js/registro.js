const formulario = document.querySelector('#formulario')
window.addEventListener('DOMContentLoaded', async () => {
  const response = await fetch("/api/users");
  const data = await response.json()
  console.log(data)
});
// Tiene codigo asincrono
formulario.addEventListener('submit', async e => {
  e.preventDefault()
// Se decllaran las variables que se requieren
  const username  = formulario['nombre'].value
  const lastname  = formulario['apellido'].value
  const datebirth = formulario['fecha'].value
  const phone     = formulario['movil'].value
  const addres    = formulario['direccion'].value
  const email     = formulario['correo'].value
  const password  = formulario['clave'].value
// Se termina de declarar 
  const response = await fetch('/api/users', {
    method: 'POST',
// Los datos que se envian del server es un json
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ 
      username,
      lastname,
      datebirth,
      phone,
      addres,
      email,
      password
    })
  })

  const user = await response.json()
  console.log(user)

  formulario.reset();

});