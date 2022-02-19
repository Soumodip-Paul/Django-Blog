async function submitLogin ( e ) {
    e.preventDefault()
    const formData = new FormData(e.target)
    try {
        const response = await fetch(e.target.action, {
            method: 'POST',
            body: formData
        })
        const data =  await response.clone().text()
        if (response.ok && response.redirected) {
            window.location.href = response.url
        }
        else if (response.status === 400) throw new Error("Failed to login! Invalid email or password.")
        else throw new Error(`${data}`)
    }
    catch ( error  ) {
        e.target.reset()
        showAlert(error.name,error.message)
    }
}

function showAlert(title,text) {
    const textElem = document.getElementById('alertModalText')
    const heading = document.getElementById('alertModalLabel')
    textElem.innerHTML = ''
    heading.innerHTML = ''
    var myModal = new bootstrap.Modal(document.getElementById('alertModal'), {
        keyboard: false
    })
    textElem.innerHTML = text
    heading.innerText = title
    myModal.toggle()
}
