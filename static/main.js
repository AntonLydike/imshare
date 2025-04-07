(() => {
const lightbox = document.querySelector("#lightbox");
const lightbox_img = lightbox.querySelector('img');

// once the image has loaded, remove the state loading class and start
// preloading the next image.
lightbox_img.addEventListener('load', _ => {
    lightbox.classList.remove("state-loading")
    preload_image(url_with_offset(1))
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

// galery controls options:
// expand possibly relative urls to absolute ones
const lightbox_urls = (() => {
    const a = document.createElement("a")
    return Array.from(document.querySelectorAll('.lightboxed')).map(elem => {
        const url = elem.getAttribute('data-lightbox-href')
        if (url === null) {
            console.error("Malformed lightboxed image:", elem)
            return null;
        }
        a.href = url;
        return a.href
    }).filter(x => x !== null)
})()

// get image that is <offset> elements from the current one (or null)
function url_with_offset(offset) {
    const index = lightbox_urls.indexOf(lightbox_img.src)
    if (index < 0) return null
    return lightbox_urls[
        mod((index + offset), lightbox_urls.length)
    ]
}
// display the <offset> image
function move_galery(offset) {
    const url = url_with_offset(offset)
    if (url === null) return
    lightbox.classList.add('state-loading')
    show(url)
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

document.body.classList.add("enable-galery");

document.addEventListener('keydown', evt => {
    if (evt.target != document.body) return
    if (actions.hasOwnProperty(evt.key)) {
        actions[evt.key]()
    }
})


// image preloading logic:
const preloaded_urls = []
let in_flight_preloads = 0
function preload_image(url) {
    if (in_flight_preloads > 1)
        return
    if (!url || preloaded_urls.indexOf(url) != -1)
        return

    in_flight_preloads++;
    img = document.createElement("img");
    img.addEventListener('load', _ => in_flight_preloads--);
    img.src = url;
    preloaded_urls.push(url)
}
})()