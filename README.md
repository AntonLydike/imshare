# Imshare - an image sharing platform

## How it works:

Folder structure:

 - `state`: The folder structure holding the state of the platform
   - `<id>`: Each "share" has an ID, the shares data is stored here
     - `notes.md`: Notes regarding the share, not visible to the user
     - `index.md`: Message attached to the share
     - `*.jpg`: Images that are to be shared (will be copied over to a web-accesible location, thumbnails will be generated)
     - `state.json`: JSON searilized state information attached to the share such as last updated time, content hash, etc.
   - `index.md`: Content shown on the landing page
   - `404.md`: 404 Message for unknown shares
 - `static`: Static files that are copied to the web:
    - `*`: copied to a web-accessible location
 - `web`: Target for all staticly generated files
 - `imshare`: Python source files that contain the program


Static files are generated into /web/static/...



