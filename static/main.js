(() => {
const lightbox = document.querySelector("#lightbox")
const lightbox_img = lightbox.querySelector('img')

document.querySelectorAll('.lightboxed').forEach(node => {
    node.addEventListener('click', event => {
        event.preventDefault()
        show(node.getAttribute('data-lightbox-href'))
    })
})

lightbox.querySelector('.lightbox-bg').addEventListener('click', evt => {
    hide()
})
lightbox.querySelector('.lightbox-fg').addEventListener('click', evt => {
    hide()
})
lightbox.querySelector('.lightbox-fg img').addEventListener('click', evt => {
    evt.preventDefault();
    evt.stopPropagation();
})

function show(img_path) {
    lightbox.classList.add('state-visible')
    lightbox_img.src = img_path
}

function hide() {
    lightbox_img.src = ""
    lightbox.classList.remove('state-visible')
}



})()