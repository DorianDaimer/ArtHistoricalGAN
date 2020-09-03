""" Creates batches of images to feed into the training network conditioned by genre, uses upsampling when creating batches to account for uneven distributuions """


import numpy as np
import imageio
import time
import random
import os
from pathlib import Path
from PIL import Image

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings

# Set the dimension of images you want to be passed in to the network
DIM = 128

# Set your own path to images
src_img_path = './Images/' # use this after unzipping in colab

# This dictionary should be updated to hold the absolute number of images associated with each genre used during training
styles = {
    "Impressionism": 12956,
    "Expressionism": 6736,
    "vincent_van_gogh": 1889,
    "paul_cezanne": 579,
    "paul_gauguin": 499,
}

styleNum = {
    "Impressionism": 0,
    "Expressionism": 1,
    "vincent_van_gogh": 2,
    "paul_cezanne": 3,
    "paul_gauguin": 4,
}

curPos = {
    "Impressionism": 0,
    "Expressionism": 0,
    "vincent_van_gogh": 0,
    "paul_cezanne": 0,
    "paul_gauguin": 0,
}

testNums = {}
trainNums = {}

# Generate test set of images made up of 1/20 of the images (per genre)
for k, v in styles.items():
    # put a twentieth of paintings in here
    nums = range(v)
    random.shuffle(list(nums))
    testNums[k] = nums[0 : v // 20]
    trainNums[k] = nums[v // 20 :]


def inf_gen(gen):
    while True:
        for (images, labels) in gen():
            yield images, labels


def make_generator(files, batch_size, n_classes):
    if batch_size % n_classes != 0:
        raise ValueError(
            "Batch size {} must be divisible by num classes {}".format(batch_size, n_classes)
        )

    class_batch = batch_size // n_classes

    generators = []

    def get_epoch():

        while True:
            images = np.zeros((batch_size, DIM, DIM, 3), dtype="int32")
            #labels = np.zeros((batch_size, n_classes))
            labels = np.zeros(batch_size, dtype="int32")
            n = 0
            for style in styles:
                styleLabel = styleNum[style]
                curr = curPos[style]
                for _ in range(class_batch):
                    if curr == styles[style]:
                        curr = 0
                        random.shuffle(list(files[style]))

                    img_path = Path(src_img_path, style, str(curr) + ".jpg")
                    image = Image.open(img_path).convert(mode="RGB")
                    image = np.asarray(image)

                    images[n % batch_size] = image
                    #labels[n % batch_size, int(styleLabel)] = 1
                    labels[n % batch_size] =  int(styleLabel)
                    n += 1
                    curr += 1
                curPos[style] = curr

            # randomize things but keep relationship between a conditioning vector and its associated image
            rng_state = np.random.get_state()
            np.random.shuffle(images)
            np.random.set_state(rng_state)
            np.random.shuffle(labels)
            yield (images, labels)

    return get_epoch


def load(batch_size):
    return (
        make_generator(trainNums, batch_size, len(styles)),
        make_generator(testNums, batch_size, len(styles)),
    )


# Testing code to validate that the logic in generating batches is working properly and quickly
if __name__ == "__main__":
    train_gen, valid_gen = load(100)
    t0 = time.time()
    for i, batch in enumerate(train_gen(), start=1):
        a, b = batch
        print("time ", str(time.time() - t0))
        if i == 1000:
            break
        t0 = time.time()
