from .misc import log_action


def static_html_template(content: str, title: str, footer: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="/static/style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
    <main>
        {content}
    </main>
<footer>
    {footer}
</footer>
</body>
"""


def fill_share_template(
    share_id: str, content: str, images: list[str], additional_info: str, footer: str
) -> str:
    log_action("template", f"share {share_id} with {images}")
    preloads = "\n    ".join(preload_directive(f"/images/{id}.jpg") for id in images)
    return f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="/static/style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image share</title>
    <meta name="title" property="og:title" content="Image share"/>
    <meta name="description" property="og:description" content="An image share of {len(images)} images using the imshare platform on pikz.cc."/>
    <meta name="type" property="og:type" content="website"/>
    <meta name="image" property="og:image" content="https://pikz.cc/images/{images[0]}_t.jpg"/>
    <meta name="url" property="og:url" content="https://pikz.cc/s/{share_id}"/>

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="Image share">
    <meta name="twitter:description" content="An image share of {len(images)} images using the imshare platform on pikz.cc."/>
    <meta name="twitter:image" content="https://pikz.cc/images/{images[0]}_t.jpg"/>
</head>
<body>
    <main>
    
        <h1>Shared images:</h1>

        {content}

        <div class="image-container">
        {"".join(make_lightbox(image) for image in images)}
        </div>

        {additional_info}
    </main>
    <footer>
        {footer}
    </footer>
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
        <div class="image-item-bg" style="background-image: url('/images/{img_id}_t.jpg')"></div>
    </div>
    """


def preload_directive(url: str, kind: str = "image") -> str:
    return f'<link rel="preload" href="{url}" as="{kind}"/>'
