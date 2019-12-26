import binascii
import random

import numpy as np
from PIL import Image
from imageio import imread

from block import Block

if __name__ == "__main__":
    # print(Block.getStegoMessage(Image.open("./stego.bmp"), 2))

    random.seed(1)

    for i in range(-10, 11):
        print(random.randint(0, 1))





