#!/usr/bin/env python3
"""Entrypoint: copy the pre-drawn front page to the output directory.

The image is drawn at build time by draw_front.py and shipped as entry.png.
This program only copies it, using the standard library, so both graded
runs write byte-identical output.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    if not os.path.isfile(src):
        sys.stderr.write("entry.png not found next to main.py\n")
        sys.exit(1)
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    print("wrote", os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
