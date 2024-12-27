import pathlib
import shutil
import hashlib
import glob
import zlib
from functools import cache


def log_action(action: str, msg: str):
    print(f"[ACTION] {action}: {msg}")


def mkdir(path):
    log_action("create folder", path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def cp_glob(glob_, dest):
    log_action("glob", glob_)
    for path in glob.iglob(glob_):
        log_action("copy", f'from "{path}" to "{dest}"')
        shutil.copy2(path, dest)


def cp_r(path, dest):
    log_action("recursive copy", f'from "{path}" to "{dest}"')
    shutil.copytree(path, dest)


def rm_r(path: str):
    assert path.startswith("web/")
    log_action("recursive delete", path)
    shutil.rmtree(path, ignore_errors=True)


@cache
def hash_image(path: str):
    with open(path, "rb") as img:
        hash = hashlib.sha1()
        while data := img.read(65536):
            hash.update(data)
        return hash.hexdigest()


@cache
def crc32(path: str):
    with open(path, "rb") as img:
        checksum = 0
        while data := img.read(1024 * 1024):
            checksum = zlib.crc32(data, checksum)
        return checksum & 0xFFFFFFFF
