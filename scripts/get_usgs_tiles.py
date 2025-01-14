from pathlib import Path

import argparse

import requests

from tqdm import tqdm

LINK_BASE = (
    "https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/TIFF/current"
)
THIS_DIR = Path(__file__).parent

parser = argparse.ArgumentParser(
    description="Download the 1/3 arc second elevation tiles from USGS"
)

parser.add_argument(
    "output_directory", help="Where should we write the tiles to?"
)


def build_link(tile: str) -> str:
    link = f"{LINK_BASE}/{tile}/USGS_13_{tile}.tif"
    return link


def download_file(url: str, destination: Path):
    if destination.is_file():
        print(f"{str(destination)} already exists, skipping")
        return

    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        destination.parent.mkdir(parents=True, exist_ok=True)

        # write to file in chunks
        with destination.open("wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def run():
    args = parser.parse_args()
    outdir = Path(args.output_directory)
    tile_data = THIS_DIR / "usgs_tiles.txt"
    with tile_data.open("r") as f:
        tiles = [l.strip() for l in f.readlines()]

    print("downloading tiles..")
    for tile in tqdm(tiles):
        link = build_link(tile)
        outfile = outdir / f"{tile}" / f"USGS_13_{tile}.tif"

        download_file(link, outfile)


if __name__ == "__main__":
    run()
