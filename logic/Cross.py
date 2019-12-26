import random
from statistics import mean
from typing import List, Tuple

from PIL import Image

from logic.Stego import Stego


class Cross(Stego):
    def __init__(self):
        super().__init__()
        self.seed = None
        self.interval = None
        self.energy = None
        self.repeatCount = None

    def extractStegoMessage(self, cross: int) -> str:
        if self.image    is None: raise TypeError
        if self.seed     is None: raise TypeError
        if self.interval is None: raise TypeError

        byteList = []
        repeat = []

        iPx = 0

        random.seed(self.seed)

        while iPx < self.image.size[0] * self.image.size[1]:
            y = iPx // self.image.size[0]
            x = iPx % self.image.size[1]

            crossMean = 0

            for i in range(1, cross + 1):
                tempXY = [
                          (max(x - i, 0),                  y),
                          (min(x + i, self.image.size[1]), y),
                          (x,                              max(y - i, 0)),
                          (x,                              min(y + i, self.image.size[0]))
                         ]

                crossMean += mean(self.image[i][2] for i in tempXY)

            crossMean /= cross * 4

            if self.image.getpixel((x, y))[2] > crossMean:
                repeat.append(1)
            else:
                repeat.append(0)

            if len(repeat) == self.repeatCount:
                byteList.append(int(round(mean(repeat))))

                if byteList[-8:] == [0, 0, 0, 0, 0, 0, 0, 0] and len(byteList) % 8 == 0:
                    payloadBinaryString = ''.join(str(bit) for bit in byteList)
                    print(' '.join(payloadBinaryString[i:i + 8] for i in range(0, len(payloadBinaryString), 8)))

                    return self._decodePayload(byteList[:-8])

                repeat = []

            interval = random.randint(1, self.interval)
            iPx += interval
            random.seed(interval)

        return self._decodePayload(byteList)  # if not found EOF

    def generateStegoImage(self) -> Image:
        if self.payload     is None: raise TypeError
        if self.image       is None: raise TypeError
        if self.seed        is None: raise TypeError
        if self.interval    is None: raise TypeError
        if self.energy      is None: raise TypeError
        if self.repeatCount is None: raise TypeError

        i = 0
        iPx = 0

        random.seed(self.seed)

        while i < len(self.payload) and iPx < self.image.size[0] * self.image.size[1]:
            px = self.image.getpixel((iPx % self.image.size[1], (iPx // self.image.size[0])))
            if self.payload[i] == 0:
                tmp = int(px[2] - self.energy * self.getLuminosity(px))
            else:
                tmp = int(px[2] + self.energy * self.getLuminosity(px))

            tmp = (px[0], px[1], tmp)
            self.image.putpixel((iPx // self.image.size[0], iPx % self.image.size[1]), tmp)

            i += 1

            interval = random.randint(1, self.interval)
            iPx += interval
            random.seed(interval)

        return self.image

    @staticmethod
    def getLuminosity(px: Tuple[int, int, int]):
        return px[0] * .2989 + px[1] * .58662 + px[2] * .11448
