import random
import time

import numpy as np
from PIL import Image

from stego import Stego
from typing import List


class Quant(Stego):
    def __init__(self, image: Image):
        super().__init__(image)
        self.seed = None
        self.key = None

    @staticmethod
    def _generateKey(seed: int):
        random.seed(seed)

        key = [[], []]

        for i in range (-255, 256):
            key[0].append(i)
            key[1].append(random.randint(0, 1))

        print(key)
        return key


    @staticmethod
    def _keyInputCheck(userInput) -> bool:
        try:
            userInput = int(userInput)
        except ValueError:
            print("Not an integer. Try again.\n")
            return False

        if userInput == -1:
            return True

        if not isinstance(userInput, int) or userInput < 1 or userInput > 65536:
            print("Sorry, given input must be 1 <= N <= 65536.\n")
            return False

        return True


    def inputData(self) -> None:
        seedSetSuccess = False
        while not seedSetSuccess:
            userInput = input("Set key (-1 to set randomly): ")
            print()

            if userInput == "0":
                return

            seedSetSuccess = self._keyInputCheck(userInput)
            if not seedSetSuccess: continue

            if int(userInput) == -1:
                random.seed(time.time())
                self.seed = random.randint(1, 65536)
                print("Random seed set: {}".format(self.seed))
                break

            self.seed = int(userInput)
            self.key = self._generateKey(self.seed)





    def menu(self) -> None:
        done = False
        while not done:  # menu sequence
            self.inputData()

            self.volume = (self.image.size[0] * self.image.size[1] - 1) // 2

            self.setPayload()

            if self.payload is None:
                return

            done = True

            self.menuPostMain()


    def printInfo(self):
        print("Container image: {}".format(str(self.image)))
        print("Key: {}".format(str(self.key)))
        print("Container volume (bits): {}".format(self.volume))
        print("Payload: {}".format(self.message))
        print("Payload (chars count): {}".format(len(self.message)))
        print("Payload (binary): {}".format(''.join(str(self.payload))))
        print("Payload volume (bits): {}".format(len(self.payload)))
        print("KEY: [(]seed: {}]".format(self.seed))
        print()

    def returnStegoImage(self):
        if self.payload is None: return None

        tempimg = self.image.copy()

        i = 0
        iPx = 0

        for x in range(0, self.image.size[0]):
            for y in range(0, self.image.size[1]):
                if i < len(self.payload) and iPx % 2 == 0:
                    if y + 1 >= self.image.size[1]:
                        xy1 = (x + 1, 0)
                    else: xy1 = (x, y + 1)

                    px0 = tempimg.getpixel((x, y))
                    px1 = tempimg.getpixel( xy1)


                    diff = px0[2] - px1[2]
                    pxB  = px0[2]

                    index = self.key[0].index(diff)
                    indexDeviation = 0

                    pxB = px0[2]

                    while True:
                        if index - indexDeviation >= 0               and self.payload[i] == self.key[1][index - indexDeviation]:
                            pxB += self.key[0][index - indexDeviation]
                            break

                        if index + indexDeviation < len(self.key[0]) and self.payload[i] == self.key[1][index + indexDeviation]:
                            pxB += self.key[0][index + indexDeviation]
                            break

                        if indexDeviation > 512: raise Exception()

                        indexDeviation += 1

                    px = (px0[0], px0[1], pxB)

                    print((px0[2], (x, y), px1[2], xy1, diff))

                    tempimg.putpixel((x, y), px)

                    i += 1
                iPx += 1

        return tempimg

    @staticmethod
    def getStegoMessage(img: Image) -> str:

        key = None

        keySetSuccess = False
        while not keySetSuccess:
            userInput = input("Enter seed: ")
            print()

            if userInput == -1:
                print("Input must be bigger than zero. Try again.\n")
                continue

            if userInput == 0:
                return ""

            keySetSuccess = Quant._keyInputCheck(userInput)
            if not keySetSuccess: continue

            key = int(userInput)


        dbg = Quant._decodePayload(Quant._retrievePayloadFromImage(img, key))
        return dbg

    @staticmethod
    def _retrievePayloadFromImage(img: Image, seed: int):
        byteList = []


        key = Quant._generateKey(seed)

        iPx = 0

        for x in range(0, img.size[0]):
            for y in range(0, img.size[1]):
                if iPx % 2 == 0:
                    px0 = img.getpixel((x, y))
                    if y + 1 >= img.size[1]:
                        xy1 = (x + 1, 0)
                    else:
                        xy1 = (x, y + 1)

                    px1 = img.getpixel(xy1)

                    byteList.append(key[1][px0[2] - px1[2]])

                    if byteList[-8:] == [0, 0, 0, 0, 0, 0, 0, 0] and len(byteList) % 8 == 0:
                        print(byteList)
                        return byteList[:-8]


        print("Empty")
        return None



    @staticmethod
    def printStegoMessage(img: Image) -> None:
        print(Quant.getStegoMessage(img))
