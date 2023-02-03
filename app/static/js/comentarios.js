const commentForm = document.querySelector('#commentForm');

let users = []
let editing = false
let userId = null

window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch('/api/comment');
    const data = await response.json()
    users = data
    renderUser(users)
});

commentForm.addEventListener('submit', async e => {

    e.preventDefault()

    const username = commentForm['username'].value
    const email = commentForm['email'].value
    const pregunta = commentForm['pregunta'].value

    if (!editing){
        const response = await fetch('/api/comment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                email,
                pregunta,
            }),
        });
    
        const data = await response.json();

        users.unshift(data);
        console.log("hola mundo")
    } else{
        const response = await fetch(`/api/comment/${userId}`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                email,
                pregunta,
            }),
        })
        const updateUser = await response.json()
        users = users.map(user => user.id === updateUser.id ? updateUser : user)
        renderUser(users)
    }

    renderUser(users);

    commentForm.reset();


});

function renderUser(users) {
    const userList = document.querySelector('#userList')
    userList.innerHTML = ''

    users.forEach(user => {
        const userItem = document.createElement('li')
        userItem.classList = 'list-group-item list-group-item-dark my-2'
        userItem.innerHTML = `
       <header class="d-flex justify-content-between aling-items-center">
          <h5>${user.username}</h5>
          <div>
            <button class=" btn-delete btn btn-danger btn-sm">Eliminar</button>
            <button class=" btn-edit btn btn-dark btn-sm">Editar</button>
          </div>        
       </header>
       <p>${user.email}</p>
       <p class="text-truncate">${user.pregunta}</p>
    `
        const btnDelete = userItem.querySelector('.btn-delete');
        btnDelete.addEventListener('click', async () => {
            const response = await fetch(`/api/comment/${user.id}`, {
                method: 'DELETE'
            })
            const data = await response.json();

            users = users.filter(user => user.id !== data.id);
            renderUser(users);

        })
        
        const btnEdit = userItem.querySelector('.btn-edit');

        btnEdit.addEventListener('click', async e => {

            const response = await fetch(`/api/comment/${user.id}`);
            const data = await response.json();

            commentForm["username"].value = data.username;
            commentForm["email"].value = data.email;
            commentForm["pregunta"].value = data.pregunta;

            editing = true
            userId = data.id
        })

        userList.append(userItem);


    })
}
