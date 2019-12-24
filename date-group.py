import argparse
import logging
from pathlib import Path


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    return parser.parse_args()


def iter_files(root: Path):
    for item in root.iterdir():
        if item.is_file():
            yield item
        if item.is_dir():
            yield from iter_files(item)


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s \t %(message)s",
        datefmt="%H:%M:%S",
    )
    args = get_args()
    root = args.path.resolve()
    logging.info("Root: %s", root)
    logging.info("Discovering files...")
    files = list(iter_files(root))
    logging.info("Discovered %d files.", len(files))


if __name__ == "__main__":
    main()
