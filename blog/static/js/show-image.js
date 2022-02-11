window.onload = e => {
    let a = document.querySelector('.file-upload a')
    const url = a.href
    a.innerHTML = `
    <img src='${url}' alt='${url}' style="width: 40vw; margin-bottom: 1rem;" />
    `
}