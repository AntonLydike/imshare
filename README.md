# Imshare - an image sharing platform

## How it works:

Folder structure:

 - `state`: The folder structure holding the state of the platform
   - `<id>`: Each "share" has an ID, the shares data is stored here
     - `notes.md`: Notes regarding the share, not visible to the user. Reserved for future use (e.g. in an admin client)
     - `index.md`: Optional message attached to the share
     - `*.jpg`: Images that are to be shared (will be copied over to a web-accesible location, thumbnails will be generated)
     - `state.json`: JSON searilized state information attached to the share such as last updated time, content hash, etc. (not yet in use)
   - `index.md`: Content shown on the landing page
   - `404.md`: 404 Message for unknown shares
 - `static`: Static files that are copied to the web:
    - `*`: copied to a web-accessible location
 - `web`: Target for all staticly generated files
 - `imshare`: Python source files that contain the program

Static files are generated into /web/static/...

Images are processed and stored in a content-adressible manner in /web/mages

## Usage:

To build the static files, run `python -m imshare build`.

Requires imagemagic, exiftool installed and the `markdown` python package to run.

## Features:

- [X] Compress images for serving on the web (8MB file size)
- [X] Generate the right headers for link preview generators
- [X] Have small thumbnails
- [X] Cache images aggressively
- [X] Have visible license notice
- [X] Static hosting friendly
- [X] Responsive design, minimal style
- [X] Image preview in lightbox-style pop-up
- [X] Bulk download as zip (requires NGINX plugin)
- [X] Next/prev controls in lightbox
- [ ] Noscript friendly
- [ ] Add a way to zoom into the images when in lightbox mode
- [ ] Add license information to EXIF data