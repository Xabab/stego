from typing import List

from PIL import Image

from logic.Stego import Stego


class Block(Stego):
    def __init__(self):
        super().__init__()
        self.blockSide = None

    def extractStegoMessage(self) -> str:
        if self.image     is None: raise TypeError
        if self.blockSide is None: raise TypeError

        byteList = []

        for y in range(0, self.image.size[1], self.blockSide):
            for x in range(0, self.image.size[0], self.blockSide):
                byteList.append(self.image.getpixel((x, y))[2] % 2)

                if byteList[-8:] == [0, 0, 0, 0, 0, 0, 0, 0]:
                    self.payload = byteList
                    self.message = self._decodePayload(byteList[:-8])
                    return self.message

        return None  # if not found EOF

    def generateStegoImage(self) -> Image:
        if self.payload   is None: raise TypeError
        if self.image     is None: raise TypeError
        if self.blockSide is None: raise TypeError
        if self.image.size[0] * self.image.size[1] // self.blockSide ** 2 < len(self.payload):
                                   raise ValueError

        i = 0
        for y in range(0, self.image.size[1], self.blockSide):
            for x in range(0, self.image.size[0], self.blockSide):
                if i < len(self.payload):
                    px = self.image.getpixel((x, y))
                    if self.payload[i] != px[2] % 2:  px = (px[0], px[1], px[2] ^ 1)
                    self.image.putpixel((x, y), px)
                    i = i + 1

        return self.image