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
from typing import List, Dict

from PIL import Image

from logic.Stego import Stego


class Quant(Stego):
    def __init__(self):
        super().__init__()
        self.seed = None
        self.key  = None


    def generateKey(self) -> Dict[str, List[int]]:
        if self.seed is None: raise TypeError
        random.seed(self.seed)

        key = {
            "difference": [],
            "value"     : []
        }

        for i in range(-255, 256):
            key["difference"].append(i)
            key["value"]     .append(random.randint(0, 1))

        self.key = key
        return key

    def getContainerVolume(self) -> int:
        return self.image.size[0] * self.image.size[1] - 1

    def generateStegoImage(self) -> Image:
        if self.key   is None: raise TypeError
        if self.image is None: raise TypeError
        if self.getContainerVolume() < len(self.payload):
            raise ValueError("Payload ({} bits) bigger than container volume ({} bits)".format(len(self.payload),
                                                                                               self.getContainerVolume()))
        tempImg = self.image.copy()

        indices = [[i for i, x in enumerate(self.key["value"]) if x == 0],
                   [i for i, x in enumerate(self.key["value"]) if x == 1]]

        for i in range(0, len(self.payload)):
            xy0 = ( i      % self.image.size[1],  i      // self.image.size[0])
            xy1 = ((i + 1) % self.image.size[1], (i + 1) // self.image.size[0])

            px0 = tempImg.getpixel(xy0)
            px1 = tempImg.getpixel(xy1)

            index = self.key["difference"].index(px1[2] - px0[2])
            closestValueIndex = min(indices[self.payload[i]], key=lambda x: abs(x - index))

            px1 = (px1[0], px1[1], px0[2] + self.key["difference"][closestValueIndex])

            tempImg.putpixel(xy1, px1)


        return tempImg


    def extractStegoMessage(self) -> str:
        if self.key   is None: raise TypeError
        if self.image is None: raise TypeError

        byteList = []

        for i in range(0, self.image.size[0] * self.image.size[1] - 1):
            xy0 = ( i      % self.image.size[1],  i      // self.image.size[0])
            xy1 = ((i + 1) % self.image.size[1], (i + 1) // self.image.size[0])

            px0 = self.image.getpixel(xy0)
            px1 = self.image.getpixel(xy1)

            byteList.append(self.key["value"][self.key["difference"].index(px1[2] - px0[2])])


        return self.decodePayload(byteList, self._eof)




