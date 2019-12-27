from PIL import Image
from logic.Stego import Stego

class Block(Stego):

    def __init__(self):
        super().__init__()
        self.blockSide = None

    def getContainerVolume(self):
        if self.image     is None: raise TypeError
        if self.blockSide is None: raise TypeError

        return (self.image.size[0] // self.blockSide) * (self.image.size[1] // self.blockSide)

    def extractStegoMessage(self) -> str:
        if self.image     is None: raise TypeError
        if self.blockSide is None: raise TypeError

        byteList = []
        eof = self.encodePayload(self._eof)
        for y in range(0, self.image.size[1], self.blockSide):
            for x in range(0, self.image.size[0], self.blockSide):
                byteList.append(self.image.getpixel((x, y))[2] % 2)
                if byteList[-len(eof):] == eof: self.decodePayload(byteList, self._eof)

        return self.decodePayload(byteList, self._eof)

    def generateStegoImage(self) -> Image:
        if self.payload   is None: raise TypeError
        if self.image     is None: raise TypeError
        if self.blockSide is None: raise TypeError
        if self.getContainerVolume() < len(self.payload):
            raise ValueError("Payload ({} bits) bigger than container volume ({} bits)".format(len(self.payload),
                                                                                               self.getContainerVolume()))

        image = self.image.copy()
        i = 0
        for y in range(0, self.image.size[1], self.blockSide):
            for x in range(0, self.image.size[0], self.blockSide):
                if i < len(self.payload):
                    px = self.image.getpixel((x, y))
                    if self.payload[i] != px[2] % 2:  px = (px[0], px[1], px[2] ^ 1)
                    image.putpixel((x, y), px)
                    i = i + 1

        return image
