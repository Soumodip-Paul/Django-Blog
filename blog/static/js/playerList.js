window.onload = e => {
    let thumbnail = ''
    document.querySelectorAll('.readonly').forEach( (el , key, parent) => {
        if (validateUrl(el.innerText)) {
            let url = el.innerText;
            if (thumbnail === '' && url !== '' ) thumbnail = url
            el.innerHTML = `<a target="_blank" rel="noopener noreferrer"  href='${url}'>${url}</a>`
        }
    })
    if (!navigator.onLine) return
    let img = document.createElement('img')
    img.src = thumbnail
    img.atl = "Thumbnail Image"
    document.getElementById('content-main').prepend(img)
}

function validateUrl(value) {
    return /^(?:(?:(?:https?|ftp):)?\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:[/?#]\S*)?$/i.test(value);
  }