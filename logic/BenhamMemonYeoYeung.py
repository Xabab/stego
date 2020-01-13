#  Copyright © 2020 Xabab
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
import os
import random
from collections import Counter
from typing import List, Tuple
from warnings import warn

import numpy as np
from PIL import Image

from logic.KochZhao import KochZhao


class BenhamMemonYeoYeung(KochZhao):
    def __init__(self):
        super().__init__()
        self.pDctHighLimit = None
        self.pDctLowWindow = None
        self.pDctLowCountLimit = None

    def generateStegoImage(self) -> Image:
        # todo check inputs
        # todo check if size mod 8 = 0

        r, g, b = self._image.split()

        tiles = self.devideToTiles(np.array(b), 8)

        random.seed(self.seed)

        i = 0

        for n in range(0, len(tiles)):
            for m in range(0, len(tiles[0])):
                if not self.tileIsAcceptable(tiles[n][m]):
                    continue

                try:
                    self._payload[i]
                except IndexError:
                    continue

                ij1 = self._rollIndex()
                ij2 = self._rollIndex([ij1])
                ij3 = self._rollIndex([ij1, ij2])


                tiles[n][m] = self.embedBitToTile(tiles[n][m], self._payload[i], ij1, ij2, ij3)

                if self.tileIsAcceptable(tiles[n][m]):  # for extracting
                    i += 1

        if i < len(self._payload):
            warn("Payload exceeds container volume, message will is fragmented.", stacklevel=2)

        if i == 0:
            warn("Unsatisfactory values. Payload wasn't writen.", stacklevel=2)

        tiles = np.around(tiles)
        tiles = np.clip(tiles, a_min = 0, a_max = 255)

        b = self.assembleFromTiles(tiles)

        return Image.merge("RGB", (r, g, Image.fromarray(b, mode="L")))

    def tileIsAcceptable(self, tile: np.ndarray):
        # return True

        dctTile = self.dct2(tile)

        isContrasty = np.max(abs(dctTile)) > self.pDctHighLimit

        # line below creates a boolean matrix map for elements satisfying that expression and sums it effectively
        # counting such elements because python boolean is in fact an 1/0 integer.
        # isclose is there for compensating int rounding after dct/idct

        isPlain = np.sum(abs(dctTile) < self.pDctLowWindow + np.isclose(dctTile, self.pDctLowWindow, atol=0.51)) \
                  > self.pDctLowCountLimit

        # if (isContrasty or isPlain): print(np.round(dctTile).astype('int'))
        return not (isContrasty or isPlain)



    def embedBitToTile(self, tile: np.ndarray, bit: str, ij1, ij2, ij3):
        np.set_printoptions(threshold=10, edgeitems=8, linewidth=150)

        dctTile = self.dct2(tile)


        dctItem1 = dctTile.item(ij1)
        dctItem2 = dctTile.item(ij2)
        dctItem3 = dctTile.item(ij3)

        if int(bit) == 0:
            if not abs(dctItem1) - abs(dctItem3) > self.dctEnergy:
                dctTile.itemset(ij1, (abs(dctItem3) + self.dctEnergy)*np.sign(dctItem1))

            if not abs(dctItem2) - abs(dctItem3) > self.dctEnergy:
                dctTile.itemset(ij2, (abs(dctItem3) + self.dctEnergy)*np.sign(dctItem2))

        else:  # if int(bit) == 1:
            if not abs(dctItem1) - abs(dctItem3) < -self.dctEnergy:
                dctTile.itemset(ij3, (abs(dctItem1) + self.dctEnergy)*np.sign(dctItem1))

            if not abs(dctItem2) - abs(dctItem3) < -self.dctEnergy:
                dctTile.itemset(ij3, (abs(dctItem2) + self.dctEnergy)*np.sign(dctItem2))

        tile = self.idct2(dctTile)

        return tile

    def extractBitFromTile(self, tile: np.ndarray, ij1, ij2, ij3):
        dctTile = self.dct2(tile)

        dctItem1 = dctTile.item(ij1)
        dctItem2 = dctTile.item(ij2)
        dctItem3 = dctTile.item(ij3)

        diff1 = abs(dctItem3) - max(abs(dctItem1), abs(dctItem2))
        diff2 = abs(dctItem3) - min(abs(dctItem1), abs(dctItem2))

        if diff1 < 0:
            return 0
        if diff2 > 0:
            return 1

        warn("Error while extracting bit, passing 0")
        return 0


    def extractStegoMessage(self) -> str:
        # todo check inputs
        # todo check if size mod 8 = 0

        r, g, b = self._image.split()

        tiles = self.devideToTiles(np.array(b), 8)

        random.seed(self.seed)

        payload = []

        for n in range(0, len(tiles)):
            for m in range(0, len(tiles[0])):
                if not self.tileIsAcceptable(tiles[n][m]):
                    continue

                ij1 = self._rollIndex()
                ij2 = self._rollIndex([ij1])
                ij3 = self._rollIndex([ij1, ij2])

                payload.append(self.extractBitFromTile(tiles[n][m], ij1, ij2, ij3))

        print("[Debug] Initial payload:")
        print(''.join([str(i) for i in self._payload]))
        print("[Debug] Extracted payload:")
        print(''.join([str(i) for i in payload]))
        print()

        return self.decodePayload(payload, self._eof)


    def getContainerVolume(self) -> int:
        # todo check inputs

        return (self._image.size[0] // 8) * (self._image.size[1] // 8)