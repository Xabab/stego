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

from PIL import Image
from logic.Stego import Stego

class Block(Stego):  # basically LSB with intervals

    def __init__(self):
        super().__init__()
        self.blockSide = None

    def getContainerVolume(self):
        if self._image     is None: raise TypeError
        if self.blockSide is None: raise TypeError

        return (self._image.size[0] // self.blockSide) * (self._image.size[1] // self.blockSide)

    def extractStegoMessage(self) -> str:
        if self._image     is None: raise TypeError
        if self.blockSide is None: raise TypeError

        byteList = []
        eof = self.encodePayload(self._eof)
        for y in range(0, self._image.size[1], self.blockSide):
            for x in range(0, self._image.size[0], self.blockSide):
                byteList.append(self._image.getpixel((x, y))[2] % 2)
                if byteList[-len(eof):] == eof: self.decodePayload(byteList, self._eof)

        return self.decodePayload(byteList, self._eof)

    def generateStegoImage(self) -> Image:
        if self._payload   is None: raise TypeError
        if self._image     is None: raise TypeError
        if self.blockSide is None: raise TypeError
        if self.getContainerVolume() < len(self._payload):
            raise ValueError("Payload ({} bits) bigger than container volume ({} bits)".format(len(self._payload),
                                                                                               self.getContainerVolume()))

        image = self._image.copy()
        i = 0
        for y in range(0, self._image.size[1], self.blockSide):
            for x in range(0, self._image.size[0], self.blockSide):
                if i < len(self._payload):
                    px = self._image.getpixel((x, y))
                    if self._payload[i] != px[2] % 2:  px = (px[0], px[1], px[2] ^ 1)
                    image.putpixel((x, y), px)
                    i = i + 1

        return image
