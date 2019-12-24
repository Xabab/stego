import numpy as np
from PIL import Image

from stego import Stego


class Block(Stego):
    def __init__(self, image: Image):
        super().__init__(image)
        self.blockSide = None

    def menu(self):
        while True:  # menu sequence
            print("Enter '0' at any time to return to main menu.\n")

            blockSizeSuccess = False

            while not blockSizeSuccess:
                userInput = input("Set block size (a power of two): ")

                if userInput == 0:
                    return

                try:
                    userInput = int(userInput)
                except:
                    print("Not an integer. Try again.\n")
                    continue

                if not isinstance(userInput, int) or not np.math.log(userInput, 2).is_integer():
                    print("Sorry, given input must be a power of two. Try again.\n")
                    continue

                if userInput > self.image.size[0]:
                    print("Sorry, given block size is bigger than an image. Try again.\n")
                    continue

                blockSizeSuccess = True

                self.blockSide = userInput

            self.volume = self.image.size[0]*self.image.size[1] // (self.blockSide * self.blockSide)

            self.setPayload()

            if self.payload is None: return

            exit = False

            while not exit:
                print('''    1) Print info
    2) Save image
    0) Return to main menu''')

                userInput = input("Enter a number: ")
                try:
                    userInput = int(userInput)
                except:
                    print("Not an integer. Try again.\n")
                    continue

                if userInput < 0 or userInput > 2:
                    print("No such option. Try again.\n")
                    continue

                if userInput == 0: return
                else:
                    if userInput == 1:
                        self.printInfo()
                    else:
                        self.getStegoImage().save(input("Save as:") + ".bmp")


    def printInfo(self):
        print(self.image)
        print("Container volume (blocks/bites): {}\n".format(self.volume))
        print("Payload: {}\n".format(len(self.message)))
        print("Payload (binary): {}\n".format(''.join(str(self.payload))))
        print("Payload volume (bites): {}\n".format(len(self.payload)))

    def getStegoImage(self):
        if self.payload is None: return None

        tempimg = self.image.copy()

        i = 0

        for x in range(0, self.image.size[0], self.blockSide):
            for y in range(0, self.image.size[1], self.blockSide):
                if i < len(self.payload):
                    px = tempimg.getpixel((x, y))
                    px = (px[0], px[1], px[2] ^ self.payload[i])
                    tempimg.putpixel((x, y), px)

        return tempimg

    @staticmethod
    def getStegoMessage(img: Image, blockSide: int):
        byte = []

        string = ''

        for x in range(0, img.size[0], blockSide):
            for y in range(0, img.size[1], blockSide):
                if len(byte) == 7:
                    if byte == [1, 1, 1, 1, 1, 1, 1, 1]:
                        return string
                    char = chr(int(''.join(str(b) for b in byte), 2))
                    print(char)
                    string = string + char
                    byte = []
                byte.append(img.getpixel((x, y))[2] % 2)
