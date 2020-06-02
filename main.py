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

from logic import KochZhao, BenhamMemonYeoYeung, JessicaFridrich
from logic.Quant import Quant
from logic.Block import Block
from logic.Cross import Cross



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
Mauris vel mauris lorem. Etiam varius tempus diam in sodales. Morbi ultricies nisi eu commodo dictum. Lorem ipsum dolor sit amet."""
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
        print("{}.bmp {}".format(i, "channel 'B'"))
        print(np.array(Image.open("{}.bmp".format(i)).convert(mode="RGB").getchannel("B")))  # converting because original image is monochromatic (have single channel)
        print()

    '''


    message = """       Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis sollicitudin augue ut augue pretium, a lacinia lacus posuere. 
Mauris vel mauris lorem. Etiam varius tempus diam in sodales. Morbi ultricies nisi eu commodo dictum. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Donec gravida eget sapien et tincidunt. Pellentesque non bibendum dui. Quisque non sem sit amet tortor aliquam mollis ac in eros."""

    print("Initial message:\n")
    print(message)
    print()

    kj = KochZhao.KochZhao()
    kj.importImage('l.bmp')
    kj.dctEnergy = 50
    kj.seed = 1
    kj.window = 3
    kj.setMessage(message)
    kj.generateStegoImage().save("./out/KochZhao.bmp")

    kj.importImage("./out/KochZhao.bmp")
    print("Retrieved message from 'KochZhao.bmp':\n")
    print(kj.extractStegoMessage())
    print()

    difference(Image.open("./l.bmp"), Image.open("./out/KochZhao.bmp")).save("./out/diff KochZhao.png")

    crop = Image.open("./out/KochZhao.bmp")
    crop = crop.crop((0, 0, 16, 16))
    crop = crop.resize((516, 516), Image.NEAREST)
    crop.save("./out/crop KochZhao.bmp")



    bmyy = BenhamMemonYeoYeung.BenhamMemonYeoYeung()
    bmyy.importImage('l.bmp')
    bmyy.dctEnergy = 25
    bmyy.seed = 1
    bmyy.window = 0
    bmyy.pDctLowWindow = 1
    bmyy.pDctLowCountLimit = 40
    bmyy.pDctHighLimit = 1500
    bmyy.setMessage(message)
    bmyy.generateStegoImage().save("./out/BenhgamMemonEoYoung.bmp")

    bmyy.importImage("./out/BenhgamMemonEoYoung.bmp")
    print("Retrieved message from 'BenhgamMemonEoYoung.bmp':\n")
    print(bmyy.extractStegoMessage())
    print()

    difference(Image.open("./l.bmp"), Image.open("./out/BenhgamMemonEoYoung.bmp")).save("./out/diff BenhgamMemonEoYoung.png")

    crop = Image.open("./out/BenhgamMemonEoYoung.bmp")
    crop = crop.crop((0, 0, 16, 16))
    crop = crop.resize((516, 516), Image.NEAREST)
    crop.save("./out/crop BenhgamMemonEoYoung.bmp")

    '''
    jf = JessicaFridrich.JessicaFridrich()
    jf.importImage('l.bmp')
    jf.alpha = 0.25
    jf.seed = 1
    jf.window = 0
    jf.setMessage(message)
    jf.generateStegoImage().save("./out/JessicaFridrich.bmp")

    jf.importImage("./out/JessicaFridrich.bmp")
    print("Retrieved message from 'JessicaFridrich.bmp':\n")
    print(bmyy.extractStegoMessage())
    print()

    # difference(Image.open("./l.bmp"), Image.open("./out/JessicaFridrich.bmp")).save("./out/diff JessicaFridrich.png")
    '''
