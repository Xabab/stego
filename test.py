import binascii

import numpy as np
from PIL import Image
from imageio import imread

from block import Block

if __name__ == "__main__":
    print(Block.getStegoMessage(Image.open("./stego.bmp"), 8))





