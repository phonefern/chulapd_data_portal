"""Derive web-ready brand assets from the institutional logo sources.

The sources in src/content/img/ are originals: the Thai Red Cross lockup is
4641 px square and 310 KB, far too large to ship, and both files carry wide
transparent margins that make them align badly at small sizes.

This script trims each to its opaque content, resizes, and writes the results to
public/brand/. Run it only when a source logo changes; the outputs are committed.

Both logos have an opaque near-white interior, so neither can sit directly on a
dark surface. The UI renders them on an explicit white plate in both themes.
That is also the correct treatment for the red cross emblem, which is protected
and must appear red-on-white without recolouring.

Requires Pillow. Pillow is a tool dependency for this script only — it is not
needed to build the site.

Usage:
    python scripts/build_brand_assets.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "src" / "content" / "img"
OUT = HERE.parent / "public" / "brand"

# Padding added back after trimming, as a fraction of the trimmed short side, so
# the mark does not sit flush against its container edge.
PAD_RATIO = 0.04


def trim(image: Image.Image) -> Image.Image:
    """Crop to the opaque content, ignoring the transparent margin."""
    bbox = image.getchannel("A").getbbox()
    return image.crop(bbox) if bbox else image


def pad_to_square(image: Image.Image, ratio: float = PAD_RATIO) -> Image.Image:
    """Centre the mark on a transparent square with a small even margin."""
    pad = int(min(image.size) * ratio)
    side = max(image.size) + pad * 2
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(image, ((side - image.width) // 2, (side - image.height) // 2), image)
    return canvas


def save(image: Image.Image, name: str, width: int) -> None:
    height = round(image.height * width / image.width)
    resized = image.resize((width, height), Image.LANCZOS)
    path = OUT / name
    resized.save(path, "PNG", optimize=True)
    print(f"  {name:<28} {width}x{height}  {path.stat().st_size / 1024:6.1f} KB")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    # --- ChulaPD / Parkinson's Center mark -------------------------------
    # The source is only 60x60, so it must never be displayed above ~30 px CSS
    # pixels or it will visibly soften. Header use is 26 px.
    mark = trim(Image.open(SRC / "chulapd-mark.png").convert("RGBA"))
    print(f"chulapd mark   source trimmed to {mark.size}")
    save(mark, "chulapd-mark.png", mark.width)  # -> public/brand/, distinct from the source

    square = pad_to_square(mark)
    for size, name in ((32, "favicon-32.png"), (180, "apple-touch-icon.png")):
        # Favicons are composited onto white: the source interior is opaque
        # white already, and a transparent favicon renders unpredictably across
        # browser chrome.
        plate = Image.new("RGBA", square.size, (255, 255, 255, 255))
        plate.alpha_composite(square)
        save(plate, name, size)

    # --- Thai Red Cross Society lockup -----------------------------------
    # Stacked lockup: emblem above two lines of type. Illegible below roughly
    # 120 px wide, so it is a footer asset, never a header one.
    trc = trim(Image.open(SRC / "thai-red-cross.png").convert("RGBA"))
    print(f"trc lockup     source trimmed to {trc.size}")
    save(trc, "thai-red-cross.png", 512)


if __name__ == "__main__":
    main()
