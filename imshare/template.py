from .misc import log_action

def static_html_template(content: str, title: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link rel="stylesheet" href="/static/style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
    <main>
    {content}
</main>
<footer>&copy; 2023 Anton Lydike</footer>
</body>
"""

def fill_share_template(share_id: str, content: str, images: list[str]) -> str:
    log_action("template", f'share {share_id} with {images}')
    return f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link rel="stylesheet" href="/static/style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>image share</title>
</head>
<body>
    <main>
    
        <h1>Shared images:</h1>

        {content}

        <div class="image-container">
        {"".join(make_lightbox(image) for image in images)}
        </div>
    </main>
    <footer>&copy; 2023 Anton Lydike</footer>
    <div id="lightbox">
        <div class="lightbox-bg"></div>
        <div class="lightbox-fg">
            <img src=""/>
        </div>
    </div>

    </div>
    <script src="/static/main.js"></script>
</body>
</html>
    """

def make_lightbox(img_id: str) -> str:
    return f"""
    <div class="lightboxed image-item" data-lightbox-href="/images/{img_id}.jpg">
        <div class="image-item-bg" style="background-image: url('/images/{img_id}.jpg')"></div>
    </div>
    """

