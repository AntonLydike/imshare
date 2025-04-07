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

    descr_text = f"Anton shared {len(images)} images with you!"

    return f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="/static/style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image share</title>

    <meta name="title" property="og:title" content="Image share"/>
    <meta name="description" property="og:description" content="{descr_text}"/>
    <meta name="type" property="og:type" content="website"/>
    <meta name="image" property="og:image" content="https://pikz.cc/images/{images[0]}_t.jpg"/>
    <meta name="url" property="og:url" content="https://pikz.cc/s/{share_id}"/>

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="Image share">
    <meta name="twitter:description" content="{descr_text}"/>
    <meta name="twitter:image" content="https://pikz.cc/images/{images[0]}_t.jpg"/>

    <script defer data-domain="pikz.cc" src="https://plausible.datenvorr.at/js/script.js"></script>
</head>
<body>
    <main>
    
        <h1>Shared images:</h1>

        {content}

        <div class="image-container">
        {"".join(make_lightbox(image) for image in images)}
        </div>
        <script>window.lightbox_urls = [{",".join(f"'/images/{img_id}.jpg'" for img_id in images)}];</script>

        <p>Download everything as a zip: <a href="/download/{share_id}.zip">{share_id}.zip</a></p>

        {additional_info}
    </main>
    <footer>
        {footer}
    </footer>
    <div id="lightbox">
        <div class="lightbox-bg"></div>
        <div class="lightbox-fg">
            <img fetchpriority="high" src=""/>
            <div class="license-info">Photo by Anton Lydike, licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="noopener noreferrer">CC BY-NC-SA 4.0</a></div>
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
