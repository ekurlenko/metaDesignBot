import os
from pathlib import Path


def get_photo_from_dir(directory: str) -> list[str]:
    os.chdir(str(Path.home()))
    os.chdir("/metaDesignBot/data/images/" + directory)
    return sorted(os.listdir())


def get_photo_from_dir_for_portfolio(directory: str) -> list[str]:
    os.chdir(str(Path.home()))
    os.chdir("/metaDesignBot/data/" + directory)
    return sorted(os.listdir())


def get_photo_for_portfolio():
    cases = get_photo_from_dir_for_portfolio("portfolio")
    arr = []
    for case in cases:
        paths = []
        for file in get_photo_from_dir_for_portfolio("portfolio/" + case):
            paths.append(os.path.abspath(file))
        arr.append(paths)
    return arr
