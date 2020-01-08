#  Copyright (c) 2019 Xabab
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import random
from itertools import repeat
from math import log

import numpy as np
import pprint
from PIL import Image, ImageChops

from logic.Quant import Quant
from logic.Block import Block
from logic.Cross import Cross
from logic.Spectral import Spectral


def exadurate(image: Image, diff: Image) -> Image:
    if image.size != diff.size: raise ValueError("Images dimensions are not equal")

    for y in range(0, image.size[0]):
        for x in range(0, image.size[1]):
            if diff.getpixel((x, y)) != (0, 0, 0):
                image.putpixel((x, y), (0, 0, 0))

    return image

def difference(image1: Image, image2: Image) -> Image:
    if image1.size != image2.size: raise ValueError("Images dimensions are not equal")

    diff = ImageChops.difference(image1, image2)
    return exadurate(image1, diff)

def imageGenerateDemo() -> None:
    message = """   Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis sollicitudin augue ut augue pretium, a lacinia lacus posuere. 
Mauris vel mauris lorem. Etiam varius tempus diam in sodales. Morbi ultricies nisi eu commodo dictum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi tempus tempus malesuada. 
Donec gravida eget sapien et tincidunt. Pellentesque non bibendum dui. Quisque non sem sit amet tortor aliquam mollis ac in eros. 
Sed molestie consectetur porta. Mauris egestas lacus libero, nec euismod erat molestie sed. Maecenas feugiat gravida turpis non sodales. Mauris at consectetur leo. 
Mauris aliquet feugiat ligula a cursus. Duis in nibh justo. Quisque eleifend imperdiet sapien, vitae lobortis lectus ultricies eu. 
Nullam non iaculis lacus. Vestibulum quis justo enim. Phasellus tristique tortor quis dui viverra mattis. Nunc gravida iaculis lorem, a tempus nisl accumsan in. 
Morbi ullamcorper egestas leo, in egestas magna tempus sed. Donec vitae urna a nisi blandit porttitor vel dignissim massa. 
Phasellus finibus risus quis nibh ultricies imperdiet. Proin tempor ex at sagittis elementum. Suspendisse potenti."""
    print("Initial message:\n")
    print(message)
    print()

    b = Block()
    b.importImage('l.bmp')
    b.blockSide = 5
    b.setMessage(message)
    b.generateStegoImage().save("./out/block.bmp")

    b.importImage("./out/block.bmp")
    print("Retrieved message from 'block.bmp':\n")
    print(b.extractStegoMessage())
    print()

    difference(Image.open("./l.bmp"), Image.open("./out/block.bmp")).save("./out/diff block.png")


    c = Cross()
    c.importImage("l.bmp")
    c.seed = 1
    c.interval = 5
    c.energy = 0.13
    c.repeatCount = 9
    c.cross = 3
    c.setMessage(message)
    c.generateStegoImage().save("./out/cross.bmp")

    c.importImage("./out/cross.bmp")
    print("Retrieved message from 'cross.bmp':\n")
    print(c.extractStegoMessage())  # message is fragmented due probabilistic bit recovery, container volume is actually enough to handle the message
    print()

    difference(Image.open("./l.bmp"), Image.open("./out/cross.bmp")).save("./out/diff cross.png")


    q = Quant()

    q.seed = 1
    q.generateKey()
    q.importImage("l.bmp")
    q.setMessage(message)
    q.generateStegoImage().save("./out/quant.bmp")

    q.importImage("./out/quant.bmp")
    print("Retrieved message from 'quant.bmp':\n")
    print(q.extractStegoMessage())
    print()

    difference(Image.open("./l.bmp"), Image.open("./out/quant.bmp")).save("./out/diff quant.png")


def showCopyrightClaim():
    copyrightMessage = """Copyright (C) 2019 Xabab
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions.\n\n\n"""
    print(copyrightMessage)


if __name__ == "__main__":
    '''
    showCopyrightClaim()  # "2019", lol, it's like 29th of December

    imageGenerateDemo()

    pp = pprint.PrettyPrinter(compact=True, indent=3)

    q = Quant()

    q.seed = 1
    q.generateKey()

    key = q.key

    np.set_printoptions(threshold=10, edgeitems=5, linewidth = 100)

    key["difference"] = np.array(key["difference"])
    key["value"] = np.array(key["value"])

    pp.pprint(key)

    paths = ["./lena512", "./out/cross", "./out/block", "./out/quant"]

    print()
    for i in paths:
        print("{}.bmp {}".format(i, "chanтel 'B'"))
        print(np.array(Image.open("{}.bmp".format(i)).convert(mode="RGB").getchannel("B")))  # converting because original image is monochromatic (have single channel)
        print()

    '''


    a = np.array([1, 0, 0, 1, 1, 0, 1, 0, 1]).tolist()

    print(type(a))