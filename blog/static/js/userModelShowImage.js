window.onload = e => {
    if (!navigator.onLine) return
    let element = document.querySelector(".readonly>a")
    if (element != null) {
        let img = document.createElement('img')
        img.src = element.href
        img.atl = "Thumbnail Image"
        document.getElementById('content-main').prepend(img)
    }
}