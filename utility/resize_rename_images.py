"""
A script designed to:
1) resize all of the downloaded images to desired dimension (DEFAULT 64x64 pixels) and
2) rename images in folders from 1.jpg to n.jpg for ease of use in training
"""

import os
import random
# import PIL
from PIL import Image
from pathlib import Path

# define desired paths
ORIGINAL_IMAGES_PATH="./"
RESIZED_IMAGES_PATH="./""

def resize_image(base_path, dest_path):
    # """
    # Source: https://opensource.com/life/15/2/resize-images-python
    # """
    TARGET_BASEWIDTH = 128


    img = Image.open(base_path)

    img = img.resize((TARGET_BASEWIDTH, TARGET_BASEWIDTH))
    img.save(dest_path, "JPEG")


def resize_rename_data(org_img_dir, res_img_dir):
    for subdir, dirs, files in os.walk(str(org_img_dir)):
        if subdir == org_img_dir.name:
            continue
        if subdir == "wikiart":
            continue
        if subdir == "small_images":
            continue
        if subdir == res_img_dir.name:
            continue

        style = Path(subdir).name
        if len(style) < 1:
            continue

        name = style

        dest_dir = Path.joinpath(res_img_dir, name)

        dest_dir.mkdir(parents=True, exist_ok=True)

        style = Path(name)
        i = 0
        for f in files:
            source = Path.joinpath(org_img_dir, name, f)
            try:
                dest_path = Path.joinpath(dest_dir, str(i) + ".jpg")
                resize_image(source, dest_path)
                i += 1
            except Exception as e:
                print(e)
                print("missed it: " + str(source))


if __name__ == "__main__":
    original_images_dir = Path(ORIGINAL_IMAGES_PATH)
    resized_images_dir = Path(RESIZED_IMAGES_PATH)
    resize_rename_data(original_images_dir, resized_images_dir)
