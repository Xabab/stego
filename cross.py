import numpy as np
from PIL import Image

from stego import Stego
from typing import List
byteList = List[int]

class Cross(Stego):
    def __init__(self, image: Image):
        super().__init__(image)
        self.crossSize = None

    @staticmethod
    def _crossSizeInputCheck(input: str, maxSize: int) -> bool:
        try:
            userInput = int(input)
        except ValueError:
            print("Not an integer. Try again.\n")
            return False

        if not np.math.log(userInput, 2).is_integer():
            print("Sorry, given input must be a power of two. Try again.\n")
            return False

        if userInput > maxSize:
            print("Sorry, given block size is bigger than an image. Try again.\n")
            return False

        return True


    def menu(self):
        done = False
        while not done:  # menu sequence
            blockSizeSetSuccess = False

            while not blockSizeSetSuccess:
                userInput = input("Set block size (a power of two): ")
                print()

                if userInput == 0:
                    return

                blockSizeSetSuccess = self._blockSizeInputCheck(userInput, self.image.size[0])
                if not blockSizeSetSuccess: continue

                self.blockSide = int(userInput)

            self.volume = self.image.size[0]*self.image.size[1] // (self.blockSide * self.blockSide)

            self.setPayload()

            if self.payload is None:
                print("dbg: payload  is None, returning")
                return

            done = True

            self.menuPostMain()


    def printInfo(self):
        print("Container image: {}".format(str(self.image)))
        print("Container volume (blocks/bites): {}".format(self.volume))
        print("Payload: {}".format(self.message))
        print("Payload (chars count): {}".format(len(self.message)))
        print("Payload (binary): {}".format(''.join(str(self.payload))))
        print("Payload volume (bites): {}".format(len(self.payload)))


    def returnStegoImage(self):
        if self.payload is None: return None

        tempimg = self.image.copy()

        i = 0

        # print(self.payload)

        for x in range(0, self.image.size[0], self.blockSide):
            for y in range(0, self.image.size[1], self.blockSide):
                if i < len(self.payload):
                    px = tempimg.getpixel((x, y))
                    # tempDbg = px[2]

                    if self.payload[i] != px[2] % 2:  px = (px[0], px[1], px[2] ^ 1)

                    tempimg.putpixel((x, y), px)

                    # print(("p: " + str(self.payload[i]), "px (x,y)" + str((x, y)), "px: " + str(tempDbg),
                    #        "p_px: " + str(px[2]), "r_p: " + str(tempimg.getpixel((x, y))[2] % 2)))

                    i = i + 1

        return tempimg


    @staticmethod
    def getStegoMessage(img: Image) -> str:

        blockSizeSetSuccess = False

        while not blockSizeSetSuccess:
            userInput = input("Set block size (a power of two) or '0' to exit: ")
            print()

            if userInput == 0:
                return ''

            blockSizeSetSuccess = Block._blockSizeInputCheck(userInput, img.size[0])
            if not blockSizeSetSuccess: continue

            blockSide = int(userInput)

        return Stego._decodePayload(Block._retrievePayloadFromImage(img, blockSide))


    @staticmethod
    def _retrievePayloadFromImage(img: Image, blockSide: int):
        byteList = []

        for x in range(0, img.size[0], blockSide):
            for y in range(0, img.size[1], blockSide):
                byteList.append(img.getpixel((x, y))[2] % 2)

                if byteList[-8:] == [0, 0, 0, 0, 0, 0, 0, 0]:
                    return byteList[:-8]

        return None  # if not found EOF

    @staticmethod
    def printStegoMessage(img: Image) -> None:
        print(Block.getStegoMessage(img))
