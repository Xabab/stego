import numpy as np
from PIL import Image

from old.block import Block
from old.Cross import Cross
from old.crossTough import CrossTough
from old.quant import Quant


from typing import List
options = List[int]

def checkImageLocationInput(input: str) -> bool:
    if input == '0':
        return True

    try:
        Image.open(input)
    except:
        print("No such file. Try again.\n")
        return False

    return True

def loadImage():
    while True:
        userInput = input("Enter image location or '0' to return to previous menu: ")
        print()

        if not checkImageLocationInput(userInput):
            continue

        if userInput == '0':
            return None

        image = Image.open(userInput)

        height, width = image.size

        if height != width or not np.math.log(width, 2).is_integer():
            print("Sorry, given image must be square and n^2 pixels wide for the time being.\n")
            continue

        image = image.convert(mode="RGB")

        return image



def menuChoiceCheck(input: str, options: options) -> bool:
    try:
        input = int(input)
    except ValueError:
        print("Not an integer. Try again.\n")
        return False

    if input not in options:
        print("No such option. Try again.\n")
        return False

    return True


if __name__ == "__main__":
    # loading source image as an array of int values

    stegoMode = {
        1: Block,
        2: Quant,
        3: Cross,
        4: CrossTough
    }

    while True:  # menu sequence
        print('''    1) encode into image\n    2) decode from image\n    0) quit\n''')

        userInput = input("Enter a number: ")
        print()

        if not menuChoiceCheck(userInput, [0, 1, 2]): continue
        userInput = int(userInput)

        if userInput == 0:
            quit(0)

        if userInput == 1:
            while True:
                print('''    1) block embedding\n    2) quantization embedding\n    3) cross embedding\n    4) cross noiseimmunity embedding\n    0) return\n''')

                userInput = input("Enter a number: ")
                print()

                if not menuChoiceCheck(userInput, [0, 1, 2, 3, 4]): continue
                userInput = int(userInput)

                if userInput == 0:
                    break

                stego = stegoMode[userInput](loadImage())  # first time using "Strategy" pattern

                if stego.image is None:
                    break

                stego.menu()

        else:
            while True:
                print(
                    '''    1) block embedding\n    2) quantization embedding\n    3) cross embedding\n    4) cross noiseimmunity embedding\n    0) return\n''')

                userInput = input("Enter a number: ")
                print()

                if not menuChoiceCheck(userInput, [0, 1, 2, 3, 4]): continue
                userInput = int(userInput)

                if userInput == 0:
                    break

                decoder = stegoMode[userInput]

                image = loadImage()

                decoder.printStegoMessage(image)
                print()








