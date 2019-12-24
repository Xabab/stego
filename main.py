import numpy as np
from imageio import imread
from PIL import Image

from block import Block
from cross import Cross
from crossTough import CrossTough
from quant import Quant

def inputImage():
    while True:
        userInput = input("Enter image location or '0' to return to previous menu: ")

        if userInput == 0:
            return None

        try:
            image = Image.open("./lena512.bmp")
        except:
            print("Whops, something went wrong. Try again.\n")
            continue

        height, width = image.size

        if height != width or not np.math.log(width, 2).is_integer():
            print("Sorry, given image must be square and n^2 pixels wide for the time being.\n")
            continue

        image = image.convert(mode="RGB")

        return image

if __name__ == "__main__":
    # loading source image as an array of int values

    mode = {
        1: Block,
        2: Quant,
        3: Cross,
        4: CrossTough
    }

    while True: #menu sequence
        print('''
    1) block embedding
    2) quantization embedding
    3) cross embedding
    4) cross noiseimmunity embedding
    0) quit
    ''')

        userInput = input("Enter a number: ")

        try:
            userInput = int(userInput)
        except:
            print("Not an integer. Try again.\n")
            continue

        if userInput < 0 or userInput > 4:
            print("No such option. Try again.\n")
            continue

        if userInput == 0:
            quit(0)


        stego = mode[userInput](inputImage())

        if stego.image is None:
            continue

        stego.menu()




