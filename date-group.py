#!/usr/bin/env python3

import argparse
import datetime
import logging
import shutil
from pathlib import Path

import exifread
from dateutil.parser import parse as parse_datetime
from dateutil.parser._parser import ParserError
from tqdm import tqdm


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def iter_files(root: Path):
    for item in root.iterdir():
        if item.is_file():
            yield item
        if item.is_dir():
            yield from iter_files(item)


def get_exif_date(path: Path):
    with path.open(mode="rb") as f:
        exif_data = exifread.process_file(f)
    if not exif_data:
        return None
    for key in ["EXIF DateTimeOriginal", "Image DateTime"]:
        if key not in exif_data:
            continue
        return datetime.datetime.strptime(
            str(exif_data[key]), "%Y:%m:%d %H:%M:%S"
        ).date()


def get_date_for_file(path: Path):
    date = get_exif_date(path)
    if date:
        return date
    try:
        return parse_datetime(path.name, fuzzy=True).date()
    except ParserError:
        pass


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s \t %(message)s",
        datefmt="%H:%M:%S",
    )
    args = get_args()
    root = args.path.resolve()
    logging.info("Root: %s", root)
    logging.info("Discovering files...")
    files = list(iter_files(root))
    logging.info("Discovered %d files.", len(files))
    for path in tqdm(files):
        date = get_date_for_file(path)
        if not date:
            logging.warning("Failed to parse date from file %s", path.relative_to(root))
            continue
        date_subdir = path.parent.joinpath(date.strftime("%Y/%B"))
        dest = date_subdir.joinpath(path.name)
        if args.dry_run:
            logging.info("%s -> %s", path.relative_to(root), dest.relative_to(root))
        else:
            date_subdir.mkdir(parents=True, exist_ok=True)
            shutil.move(path, dest)


if __name__ == "__main__":
    main()
