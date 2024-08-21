import os
from pathlib import Path


def get_photo_from_dir(directory: str) -> list:
    os.chdir(str(Path.home()))
    os.chdir("metaDesignBot/data/images/" + directory)
    return sorted(os.listdir())
