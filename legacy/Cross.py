import random
import time
from statistics import mean

import numpy as np
from PIL import Image

from legacy.stego import Stego
from typing import List, Tuple

byteList = List[int]
pixel = Tuple[int, int, int]


class Cross(Stego):
    def __init__(self, image: Image):
        super().__init__(image)
        self.seed = None
        self.interval = None
        self.energy = None
        self.repeatCount = None

    @staticmethod
    def _crossSizeInputCheck(userInput: str, maxSize: int) -> bool:
        try:
            userInput = int(userInput)
        except ValueError:
            print("Not an integer. Try again.\n")
            return False

        if not isinstance(userInput, int) or not np.math.log(userInput, 2).is_integer() or userInput < 1:
            print("Sorry, given input must be a power of two and bigger than zero. Try again.\n")
            return False
        if userInput > maxSize:
            print("Sorry, given cross size is bigger than an image. Try again.\n")
            return False

        return True

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

    @staticmethod
    def _intervalInputCheck(userInput) -> bool:
        try:
            userInput = int(userInput)
        except ValueError:
            print("Not an integer. Try again.\n")
            return False

        return True

    @staticmethod
    def _energyInputCheck(userInput) -> bool:
        try:
            userInput = float(userInput)
        except ValueError:
            print("Not a float. Try again.\n")
            return False

        if not isinstance(userInput, float) or userInput < 0. or userInput > 1.:
            print("Sorry, given input must be 0. < N < 1.\n")
            return False

        return True

    @staticmethod
    def _repeatCountInputCheck(userInput) -> bool:
        try:
            userInput = int(userInput)
        except ValueError:
            print("Not an integer. Try again.\n")
            return False

        if not isinstance(userInput, int) or userInput < 0 or userInput > 65536:
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

        intervalSetSuccess = False

        while not intervalSetSuccess:
            userInput = input("Set max interval: ")
            print()

            if userInput == "0":
                return

            intervalSetSuccess = self._intervalInputCheck(userInput)
            if not intervalSetSuccess: continue

            self.interval = int(userInput)

        energySetSuccess = False
        while not energySetSuccess:
            userInput = input("Set signal energy: ")
            print()

            if userInput == "0":
                return

            energySetSuccess = self._energyInputCheck(userInput)
            if not energySetSuccess: continue

            self.energy = float(userInput)

        repeatSetSuccess = False
        while not repeatSetSuccess:
            userInput = input("Set repeat count: ")
            print()

            if userInput == "0":
                return

            repeatSetSuccess = self._repeatCountInputCheck(userInput)
            if not repeatSetSuccess: continue

            self.repeatCount = int(userInput)



    def menu(self) -> None:
        done = False
        while not done:  # menu sequence
            self.inputData()

            self.volume = self.image.size[0] * self.image.size[1] // self.interval

            self.setPayload()

            if len(self.payload) > self.volume:
                print("Warning: payload volume ({}) bigger than guaranteed container volume ({})\n".format(len(self.payload), self.volume))

            if self.payload is None:
                return

            done = True

            self.menuPostMain()

    def setPayload(self):
        payloadSuccess = False

        while not payloadSuccess:
            userInput = input("Set the payload (string, utf-8): ")
            print()

            if userInput == "0":
                return None

            if not all(ord(c) < 256 for c in userInput):
                print("Only utf-8 characters allowed\n")
                continue

            self.message = userInput

            bitArray = self._encodePayload(userInput)

            if len(bitArray) > self.volume:
                print(
                    "Payload ({} bites) bigger than container volume ({} bites).\n".format(len(bitArray), self.volume))
                continue

            self.payload = bitArray

            payloadBinaryString = ''.join(str(bit) for bit in bitArray)
            payloadBinaryString = ' '.join(payloadBinaryString[i:i + 8] for i in range(0, len(payloadBinaryString), 8))

            print("Payload set: {}\nBinary representation  (where 00000000 is EOF):\n{}\n\n".format(self.message,
                                                                                                    payloadBinaryString))
            payloadSuccess = True


    def _encodePayload(self, string: str) -> byteList:
        byteListString = ''

        for i in bytearray(string, encoding='utf-8'):
            byteListString += format(i, '#010b')[2:]
            # print("ByteArrayString: " + str(byteListString))
        byteListString += "00000000"   # eof

        byteArray = []

        for bit in "".join([x * self.repeatCount for x in byteListString]):
            byteArray.append(int(bit))

        return byteArray

    def printInfo(self):
        print("Container image: {}".format(str(self.image)))
        print("Seed: {}".format(str(self.seed)))
        print("Max interval: {}".format(str(self.interval)))
        print("Container guaranteed volume (bites): {}".format(self.volume))
        print("Signal energy: {}".format(self.energy))
        print("Payload: {}".format(self.message))
        print("Payload (chars count): {}".format(len(self.message)))
        print("Payload (binary): {}".format(''.join(str(self.payload))))
        print("Payload volume (bits): {}".format(len(self.payload)))
        print("KEY: (seed: {}, interval: {})".format(self.seed, self.interval))
        print()

    def returnStegoImage(self):
        if self.payload is None: return None

        tempimg = self.image.copy()

        i = 0

        iPx = 0

        # print(self.payload)

        random.seed(self.seed)

        while i < len(self.payload) and iPx < tempimg.size[0] * tempimg.size[1]:
            px = tempimg.getpixel((iPx // tempimg.size[0], iPx % tempimg.size[1]))
            print((iPx // tempimg.size[0], iPx % tempimg.size[1]))
            if self.payload[i] == 0:
                tmp = int(px[2] - self.energy * Cross.getLuminocity(px))
            else:
                tmp = int(px[2] + self.energy * Cross.getLuminocity(px))

            tmp = (px[0], px[1], tmp)
            tempimg.putpixel((iPx // tempimg.size[0], iPx % tempimg.size[1]), tmp)

            i += 1

            interval = random.randint(1, self.interval)
            iPx += interval
            random.seed(interval)

        return tempimg

    @staticmethod
    def getStegoMessage(img: Image) -> str:

        key, interval, crossSize, repeatCount= None, None, None, None

        keySetSuccess = False
        while not keySetSuccess:
            userInput = input("Enter seed: ")
            print()

            if userInput == -1:
                print("Input must be bigger than zero. Try again.\n")
                continue

            if userInput == 0:
                return ""

            keySetSuccess = Cross._keyInputCheck(userInput)
            if not keySetSuccess: continue

            key = int(userInput)

        intervalSetSuccsess = False

        while not intervalSetSuccsess:
            userInput = input("Enter max interval: ")
            print()

            if userInput == 0:
                return ""

            intervalSetSuccsess = Cross._intervalInputCheck(userInput)
            if not intervalSetSuccsess: continue

            interval = int(userInput)

        crossSetSuccsess = False

        while not crossSetSuccsess:
            userInput = input("Enter cross size: ")
            print()

            if userInput == 0:
                return ""

            crossSetSuccsess = Cross._intervalInputCheck(userInput)
            if not crossSetSuccsess: continue

            crossSize = int(userInput)

        repeatSetSuccess = False
        while not repeatSetSuccess:
            userInput = input("Set repeat count: ")
            print()

            if userInput == "0":
                return ""

            repeatSetSuccess = Cross._repeatCountInputCheck(userInput)
            if not repeatSetSuccess: continue

            repeatCount = int(userInput)

        return Cross._decodePayload(Cross._retrievePayloadFromImage(img, key, interval, crossSize, repeatCount))

    @staticmethod
    def _retrievePayloadFromImage(img: Image, seed: int, maxInterval: int, crossSize: int, repeatCount: int):
        byteList = []
        repeat = []

        iPx = 0

        random.seed(seed)

        while iPx < img.size[0] * img.size[1]:
            x = iPx // img.size[0]
            y = iPx %  img.size[1]

            crossMean = 0

            for i in range(1, crossSize + 1):
                tmpXm = x - i
                tmpXp = x + i
                tmpYp = y + i
                tmpYm = y - i

                if tmpXp >= img.size[0]: tmpXp = img.size[0] - 1
                if tmpYp >= img.size[1]: tmpYp = img.size[1] - 1
                if tmpXm < 0:            tmpXm = 0
                if tmpYm < 0:            tmpYm = 0

                crossMean += img.getpixel((tmpXp, tmpYp))[2]
                crossMean += img.getpixel((tmpXm, tmpYm))[2]
                crossMean += img.getpixel((tmpXm, tmpYp))[2]
                crossMean += img.getpixel((tmpXp, tmpYm))[2]

            crossMean /= crossSize * 4

            if img.getpixel((x, y))[2] > crossMean: repeat.append(1)
            else:                                   repeat.append(0)

            if len(repeat) == repeatCount:
                byteList.append(int(round(mean(repeat))))
                print(repeat)

                if byteList[-8:] == [0, 0, 0, 0, 0, 0, 0, 0] and len(byteList) % 8 == 0:
                    payloadBinaryString = ''.join(str(bit) for bit in byteList)
                    print(' '.join(payloadBinaryString[i:i + 8] for i in range(0, len(payloadBinaryString), 8)))

                    return byteList[:-8]

                repeat = []




            interval = random.randint(1, maxInterval)
            iPx += interval
            random.seed(interval)



        return byteList  # if not found EOF

    @staticmethod
    def getLuminocity(px: pixel):
        return px[0] * .2989 + px[1] * .58662 + px[2] * .11448

    @staticmethod
    def printStegoMessage(img: Image) -> None:
        print(Cross.getStegoMessage(img))
