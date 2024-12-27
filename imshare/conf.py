from dataclasses import dataclass


@dataclass
class Config:
    num_jobs: int | None = None

    # image downscaling info:
    thumb_bytes = "200kb"
    thumb_size = "600x600"
    image_bytes = "8MB"


CONF = Config()
