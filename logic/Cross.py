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

import random
from _warnings import warn
from itertools import repeat
from statistics import mean
from typing import Tuple, List

from PIL import Image

from logic.Stego import Stego


class Cross(Stego):
    def __init__(self):
        super().__init__()
        self.seed        = None
        self.interval    = None
        self.energy      = None
        self.repeatCount = None
        self.cross       = None

    def getContainerVolume(self) -> int:
        if self.interval    is None: raise TypeError
        if self._image       is None: raise TypeError
        if self.repeatCount is None: raise TypeError

        return self._image.size[0] * self._image.size[1] // self.interval


    def encodePayload(self, string: str, eof: str = "") -> List[int]:
        bitList = super().encodePayload(string, eof)
        bitList = [x for item in bitList for x in repeat(item, self.repeatCount)]

        return bitList

    def decodePayload(self, bitList: List[int], eof: str = "") -> str:
        bitListClean = []

        for i in range(0, len(bitList), self.repeatCount):
            bitListClean.append(int(round(mean(bitList[i:i + self.repeatCount]))))

        return super().decodePayload(bitListClean, eof)

    def generateStegoImage(self) -> Image:
        if self._payload     is None: raise TypeError
        if self._image       is None: raise TypeError
        if self.seed        is None: raise TypeError
        if self.interval    is None: raise TypeError
        if self.energy      is None: raise TypeError
        if self.repeatCount is None: raise TypeError
        if self.getContainerVolume() < len(self._payload):
            warningMessage = "Payload ({} bits) bigger than guaranteed container volume ({} bits). Message might be fragmented.".format(len(self._payload), self.getContainerVolume())
            warn(warningMessage, stacklevel=2)  # stacklevel=2 because it's not generateStegoImage's fault that payload is bigger than volume

        image = self._image.copy()
        i = 0
        iPx = 0
        random.seed(self.seed)
        size = self._image.size
        while i < len(self._payload) and iPx < size[0] * size[1]:
            px = self._image.getpixel((iPx % size[1], (iPx // size[0])))
            if self._payload[i] == 0:
                pxB = max(0, int(px[2] - self.energy * self._getLuminosity(px)))
            else:
                pxB = min(255, int(px[2] + self.energy * self._getLuminosity(px)))

            tmp = (px[0], px[1], pxB)
            image.putpixel((iPx % image.size[1], iPx // image.size[0]), tmp)

            i += 1
            interval = random.randint(1, self.interval)
            iPx += interval

        return image

    def extractStegoMessage(self) -> str:
        if self._image    is None: raise TypeError
        if self.seed     is None: raise TypeError
        if self.interval is None: raise TypeError
        if self.cross    is None: raise TypeError

        byteList = []

        iPx = 0
        random.seed(self.seed)
        while iPx < self._image.size[0] * self._image.size[1]:
            y = iPx // self._image.size[0]
            x = iPx % self._image.size[1]

            crossMean = []

            for i in range(1, self.cross + 1):
                tempXY = [
                          (max(x - i, 0),                      y),
                          (min(x + i, self._image.size[1] - 1), y),
                          (x,                      max(y - i, 0)),
                          (x, min(y + i, self._image.size[0] - 1))]

                crossMean.extend([self._image.getpixel(i)[2] for i in tempXY])

            crossMean = mean(crossMean)

            if self._image.getpixel((x, y))[2] > crossMean:
                byteList.append(1)
            else:
                byteList.append(0)

            interval = random.randint(1, self.interval)
            iPx += interval

        return self.decodePayload(byteList, self._eof)


    @staticmethod
    def _getLuminosity(px: Tuple[int, int, int]):
        return px[0] * .2989 + px[1] * .58662 + px[2] * .11448
