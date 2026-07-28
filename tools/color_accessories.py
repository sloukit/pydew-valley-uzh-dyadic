from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Any

from PIL import Image
import colorsys

from src.enums import Color

HAT_HOE_KEEP = Image.open("images/characters/rabbit/hat_hoe_keep.png").load()
HAT_WATER_KEEP = Image.open("images/characters/rabbit/hat_water_keep.png").load()

@dataclass
class Palette:
    name: Color
    dark: tuple[int, int, int, int]
    light: tuple[int, int, int, int]


BASE = Palette(Color.BASE, (154, 75, 152, 255), (233, 156, 177, 255))

PALETTES = [
    Palette(Color.GREEN, (26, 100, 0, 255), (34, 169, 0, 255)),
    Palette(Color.LIGHTBLUE, (50, 129, 255, 255), (71, 209, 255, 255)),
    Palette(Color.RED, (255, 0, 22, 255), (255, 66, 43, 255)),
    Palette(Color.YELLOW, (255, 209, 0, 255), (255, 230, 53, 255)),
    Palette(Color.PURPLE, (186, 0, 255, 255), (229, 52, 255, 255)),
    Palette(Color.BROWN, (75, 34, 0, 255), (117, 53, 0, 255)),
    Palette(Color.ORANGE, (214, 95, 0, 255), (255, 133, 0, 255)),
]

def is_base_image(path: Path):
    return path.stem.endswith("_base")

def color_distance(p1, p2):
    r1, g1, b1, _ = p1
    r2, g2, b2, _ = p2

    dr = r1-r2
    dg = g2-g1
    db = b2-b1

    return 0.299*dr*dr + 0.587*dg*dg + 0.114*db*db

def is_transparent(pixel):
    return pixel[3] == 0

def is_border(pixels, x, y):
    try:
        return any([is_transparent(pixel) for pixel in [
            pixels[x + 1, y],
            pixels[x, y + 1],
            pixels[x, y - 1],
            pixels[x - 1, y],
        ]])
    except IndexError:
        return True

def recolor(pixel, target):
    r, g, b, a = [x / 255 for x in pixel]

    tr, tg, tb, _ = [x / 255 for x in target]

    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    target_h, _, _ = colorsys.rgb_to_hsv(tr, tg, tb)

    nr, ng, nb = colorsys.hsv_to_rgb(target_h, s, v)

    return int(nr * 255), int(ng * 255), int(nb * 255), int(a * 255)

def recolor_hat(pixels, width, height, palette, mask):
    for y in range(height):
        for x in range(width):
            if mask is None or mask[x,y][0] != 0:
                distance_to_dark = color_distance(pixels[x, y], BASE.dark)
                distance_to_light = color_distance(pixels[x, y], BASE.light)

                if distance_to_dark < distance_to_light:
                    pixels[x, y] = recolor(pixels[x, y], palette.dark)
                else:
                    pixels[x, y] = recolor(pixels[x, y], palette.light)

def recolor_necklace(pixels, width, height, palette, _mask):
    for y in range(height):
        for x in range(width):
            pixels[x, y] = recolor(pixels[x, y], palette.light)

def add_colors(base: Path, palette: Palette, recolor: Callable[[Any, int, int, Palette, Any], None]):
    img = Image.open(base)
    pixels = img.load()
    width, height = img.size

    mask = None

    if "hoe" in base.stem:
        mask = HAT_HOE_KEEP
    if "water" in base.stem:
        mask = HAT_WATER_KEEP

    recolor(pixels, width, height, palette, mask)

    destination = base.parent / f"{base.stem.replace("_base", "")}_{palette.name}.png"
    img.save(destination)

def main():
    for file in Path("images/characters/rabbit").iterdir():
        if file.is_file() and not file.stem.endswith("_keep") and is_base_image(file):
            for palette in PALETTES:
                if file.stem.startswith("hat_"):
                    add_colors(file, palette, recolor_hat)
                elif file.stem.startswith("necklace_"):
                    add_colors(file, palette, recolor_necklace)

if __name__ == "__main__":
    main()