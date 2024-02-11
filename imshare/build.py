import re
from .misc import mkdir, hash_image, cp_r, log_action, rm_r
from .template import fill_share_template, static_html_template

import glob
import markdown
import os
import csv
import subprocess
from multiprocessing.pool import ThreadPool

from functools import cache

THUMB_BYTES = "200kb"
THUMB_SIZE = "600x600"

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

    if os.path.exists("state/favicon.ico"):
        cp_r("state/favicon.ico", "web/favicon.ico")

    footer = md_file_as_html("state/footer.md")

    log_action("building static", "/index.html")
    html = md_file_as_html("state/index.md")
    with open("web/index.html", "w") as f:
        f.write(static_html_template(html, "Image sharing", footer))

    log_action("building static", "/404.html")
    html = md_file_as_html("state/404.md")
    with open("web/404.html", "w") as f:
        f.write(static_html_template(html, "404 - Not Found!", footer))


def build_shares():
    for share in get_shares():
        build_share(share)


def get_shares() -> list[str]:
    return (f for f in glob.glob("state/*") if os.path.isdir(f))


def build_share(share: str):
    log_action("building share", share)
    images = get_share_images(share)
    with ThreadPool() as tp:
        img_ids = tp.map(process_image, images)
    build_share_html(share, img_ids)
    build_share_files_txt(share, zip(images, img_ids))

def discover_images_in_share(share: str) -> list[str]:
    """
    find all image files inside folder share
    """
    is_image_file = re.compile(r'.*\.(jpg|jpeg|png)', re.IGNORECASE)
    return [
        os.path.join(share, f)
        for f in os.listdir(share)
        if os.path.isfile(os.path.join(share, f)) and is_image_file.fullmatch(f)
    ]

def get_share_images(share: str):
    csv_data: str = subprocess.check_output(
        [
            "exiftool",
            "-csv",
            "-CreateDate",
            "-d",
            "%s",
        ]
        + discover_images_in_share(share),
        text=True,
        stderr=subprocess.DEVNULL,
    )
    lines = csv.reader(csv_data.splitlines()[1:], delimiter=",")
    return [l[0] for l in sorted(lines, key=lambda l: int(l[1]))]


def build_share_html(share: str, img_ids: list[str]):
    share_id = os.path.basename(share)
    html = md_file_as_html(os.path.join(share, "index.md"))
    footer = md_file_as_html("state/footer.md")
    share_info = md_file_as_html("state/share_info.md")
    content = fill_share_template(share_id, html, img_ids, share_info, footer)
    mkdir("web/s/" + share_id)
    with open(f"web/s/{share_id}/index.html", "w") as f:
        log_action("create html", f"{share_id}/index.html")
        f.write(content)


def build_share_files_txt(share: str, images: list[tuple[str, str]]):
    """
    builds a files.txt file containing:

    - <size> /images/<hash>.jpg <name>

    for each image in the share
    """
    share_id = os.path.basename(share)
    with open(f"web/s/{share_id}/files.txt", "w") as f:
        log_action("create files.txt", f"{share_id}/files.txt")
        for name, id in images:
            f.write("- {} /images/{}.jpg {}\n".format(
                os.path.getsize(f'web/images/{id}.jpg'),
                id,
                os.path.basename(name)
            ))


@cache
def md_file_as_html(md_file: str):
    if not os.path.exists(md_file):
        return ""
    log_action("convert markdown", md_file)
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
                "-gravity",
                "Center",
                "-extent",
                "1:1",
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
            [
                "convert",
                img_path,
                "-define",
                f"jpeg:extent={MAIN_BYTES}",
                res_path,
            ]
        )
    return img_id
