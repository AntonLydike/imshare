#from .misc import 
from .build import process_image, discover_images_in_share
import shutil
from typing import Iterable


def iter_compressed_and_raw_paths(share: str) -> Iterable[tuple[str,str]]:
    """
    Given a share, return the IDs and names of all images in the share
    """
    for path in discover_images_in_share(share):
        yield process_image(path), path


def copy_compressed_with_plain_names_to(share: str, dest: str):
    for id, img in iter_compressed_and_raw_paths(share):
        img = img.split("/")[-1]
        print(f"Copy web/images/{id}.jpg to {dest}/{img}")
        shutil.copy2(
            f'web/images/{id}.jpg',
            f"{dest}/{img}",
        )
