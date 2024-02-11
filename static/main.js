(() => {
const lightbox = document.querySelector("#lightbox")
const lightbox_img = lightbox.querySelector('img')

lightbox_img.addEventListener('load', evt => {
    lightbox.classList.remove("state-loading")
})

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

const enable_galery = Array.isArray(window.lightbox_urls);
// expand possibly relative urls to absolute ones
const lightbox_urls = (() => {
    const a = document.createElement("a")
    return window.lightbox_urls.map(url => {
        a.href = url;
        return a.href
    })
})()

function move_galery(offset) {
    if (!enable_galery) return
    const index = lightbox_urls.indexOf(lightbox_img.src)
    if (index < 0) return
    lightbox.classList.add('state-loading')
    show(window.lightbox_urls[
        mod((index + offset), lightbox_urls.length)
    ]);
}
const next = () => move_galery(1)
const prev = () => move_galery(-1)

// because fuck you, javascript:
const mod = (n, m) => ((n % m) + m) % m

// map keys to actions
const actions = {
    // next on: space, arrows, enter
    " ": next,
    "ArrowRight": next,
    "ArrowDown": next,
    "Enter": next,
    // prev on: backspace, arrows
    "Backspace": prev,
    "ArrowLeft": prev,
    "ArrowUp": prev,
    // hide on escape
    "Escape": hide
}

if (enable_galery) {
    document.body.classList.add("enable-galery");

    document.addEventListener('keydown', evt => {
        if (evt.target != document.body) return
        if (actions.hasOwnProperty(evt.key)) {
            actions[evt.key]()
        }
    })
}
})()