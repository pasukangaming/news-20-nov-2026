"""Sum up 20 November 2026's world news in one image.

The image is entry.png, drawn by draw_image.py and held in this
repository. This program is the entrypoint the grader runs: it
copies that image to /output/entry.png, using only the Python
standard library, with no network, no clock and no randomness,
so two runs write exactly the same bytes.

Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
SOURCE = os.path.join(HERE, "entry.png")

# Fail loudly if the image is missing instead of writing a
# partial output: the grader must see a whole 1024x1024 PNG.
if not os.path.isfile(SOURCE):
    raise FileNotFoundError(f"entry image not found: {SOURCE}")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SOURCE, os.path.join(OUT_DIR, "entry.png"))
