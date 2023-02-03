const partnerForm = document.querySelector('#partnerForm');

let users = []
let editing = false
let userId = null

window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch('/api/partner');
    const data = await response.json()
    users = data
    renderUser(users)
});

partnerForm.addEventListener('submit', async e => {

    e.preventDefault()

    const company   = partnerForm['company'].value
    const descrip   = partnerForm['descrip'].value
    const locate    = partnerForm['locate'].value
    const phone     = partnerForm['phone'].value
    const email     = partnerForm['email'].value

    if (!editing){
        const response = await fetch('/api/partner', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                company,
                descrip,
                locate,
                phone,
                email,
            }),
        });
    
        const data = await response.json();
        users.unshift(data);
        console.log("hola mundo")
    } else{
        const response = await fetch(`/api/partner/${userId}`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                company,
                descrip,
                locate,
                phone,
                email,
            }),
        })
        const updatePartner = await response.json()
        users = users.map(user => user.id === updatePartner.id ? updatePartner : user)
        renderUser(users)
        
    }

    renderUser(users);

    partnerForm.reset();


});

function renderUser(users) {
    const userList = document.querySelector('#userList')
    userList.innerHTML = ''

    users.forEach(user => {
        const userItem = document.createElement('li')
        userItem.classList = 'list-group-item list-group-item-dark my-2'
        userItem.innerHTML = `
        <header class="d-flex justify-content-between aling-items-center">
            <h5>${user.company}</h5>
        <div>
            <button class=" btn-delete btn btn-danger btn-sm">Eliminar</button>
            <button class=" btn-edit btn btn-dark btn-sm">Editar</button>
        </div>        
        </header>
        <p>${user.descrip}</p>
        <p>${user.locate}</p>
        <p>${user.phone}</p>
        <p>${user.email}</p>

    `
        const btnDelete = userItem.querySelector('.btn-delete');
        btnDelete.addEventListener('click', async () => {
            const response = await fetch(`/api/partner/${user.id}`, {
                method: 'DELETE'
            })
            const data = await response.json();

            users = users.filter(user => user.id !== data.id);
            renderUser(users);

        })

        const btnEdit = userItem.querySelector('.btn-edit');

        btnEdit.addEventListener('click', async e => {

            const response = await fetch(`/api/partner/${user.id}`);
            const data = await response.json();

            partnerForm['company'].value       = data.company;
            partnerForm['descrip'].value       = data.descrip;
            partnerForm['locate'].value        = data.locate;
            partnerForm['phone'].value         = data.phone;
            partnerForm['email'].value         = data.email;   
            
            editing = true
            userId = data.id
        })

        userList.append(userItem);
    })
}

