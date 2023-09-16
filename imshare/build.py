from .misc import mkdir, hash_image, cp_r, log_action, rm_r
from .template import fill_share_template, static_html_template

import glob
import markdown
import os
import subprocess


THUMB_BYTES = "300kb"
THUMB_SIZE = "300x300"

MAIN_BYTES = "8MB"


def build():
    build_statics()
    build_shares()
    return 0


def build_statics():
    mkdir("web")
    mkdir("web/images")

    rm_r("web/static")
    cp_r("static", "web/static")

    log_action("building static", "/index.html")
    with open("state/index.md", "r") as f:
        html = markdown.markdown(f.read())
    with open("web/index.html", "w") as f:
        f.write(static_html_template(html, "Image sharing"))

    if os.path.exists("state/404.md"):
        log_action("building static", "/404.html")
        with open("state/404.md", "r") as f:
            html = markdown.markdown(f.read())
        with open("web/404.html", "w") as f:
            f.write(static_html_template(html, "404 - Not Found!"))


def build_shares():
    for share in get_shares():
        build_share(share)


def get_shares() -> list[str]:
    return (f for f in glob.glob("state/*") if os.path.isdir(f))


def build_share(share: str):
    log_action("building share", share)
    img_ids = [
        process_image(os.path.join(share, img))
        for img in glob.iglob("*.jpg", root_dir=share)
    ]
    build_share_html(share, img_ids)


def build_share_html(share: str, img_ids: list[str]):
    share_id = os.path.basename(share)
    html = md_file_as_html(os.path.join(share, "index.md"))
    footer = md_file_as_html("state/footer.md")
    content = fill_share_template(share_id, html, img_ids, footer)
    mkdir("web/s/" + share_id)
    with open(f"web/s/{share_id}/index.html", "w") as f:
        log_action("create html", f"{share_id}/index.html")
        f.write(content)


def md_file_as_html(md_file: str):
    if not os.path.exists(md_file):
        return ""
    with open(md_file, "r") as f:
        return markdown.markdown(f.read())


def process_image(img_path: str):
    img_id = hash_image(img_path)
    out_path = "web/images/"
    thumb_path = out_path + img_id + "_t.jpg"
    res_path = out_path + img_id + ".jpg"
    if not os.path.exists(thumb_path):
        log_action("create thumbnail", f"{img_path} with id {img_id}")
        subprocess.check_call(
            [
                "convert",
                img_path,
                "-define",
                f"jpeg:extent={THUMB_BYTES}",
                "-resize",
                THUMB_SIZE,
                thumb_path,
            ]
        )
    if not os.path.exists(res_path):
        log_action("convert image", f"{img_path} with id {img_id}")
        subprocess.check_call(
            ["convert", img_path, "-define", f"jpeg:extent={MAIN_BYTES}", res_path]
        )
    return img_id
