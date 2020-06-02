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

import copy
import os
import random
from math import sqrt, cos, pi
from typing import Tuple, List

import numpy as np
from PIL import Image

from logic.Stego import Stego
from logic.util.dctEssentials import *
from logic.util.randomIndexes import *


class KochZhao(Stego):
    def __init__(self):
        super().__init__()
        self.dctEnergy = None
        self.window = None     # as distance from the second diagonal
        self.seed = None

    def generateStegoImage(self) -> Image:
        # todo check inputs
        # todo check if size mod 8 = 0

        r, g, b = self._image.split()

        tiles = devideToTiles(np.array(b), 8)

        random.seed(self.seed)

        # os.remove("write.txt")
        # f = open("write.txt", "w+")

        for n in range(0, len(tiles)):
            for m in range(0, len(tiles[0])):
                ij1 = rollSecondDiagonalIndex(self.window)
                ij2 = rollSecondDiagonalIndex(self.window, [ij1])

                # f.write(str((ij1, ij2)) + "\n")

                try:
                    tiles[n][m] = self.embedBitToTile(tiles[n][m], self._payload[n * len(tiles[0]) + m], ij1, ij2)
                except IndexError:
                    continue

        # f.close()

        b = assembleFromTiles(tiles)
        return Image.merge("RGB", (r, g, Image.fromarray(b, mode="L")))


    def embedBitToTile(self, tile: np.ndarray, bit: str, ij1, ij2):
        np.set_printoptions(threshold=10, edgeitems=8, linewidth=150)

        dctTile = dct2(tile)

        # print()

        # print((ij1, ij2))
        # print(dctTile)


        dctItem1 = dctTile.item(ij1)
        dctItem2 = dctTile.item(ij2)

        diff = abs(dctItem1) - abs(dctItem2)

        # dbg = "Old ({}, {}), ".format(dctItem1, dctItem2)
        # dbg += "abs diff {}, payload {}, ".format(diff, bit)

        if int(bit) == 0:
            if diff > self.dctEnergy:
                pass
            else:
                dctTile.itemset(ij1, (abs(dctItem2) + self.dctEnergy)*np.sign(dctItem1))
        else:  # if int(bit) == 1:
            if diff < -self.dctEnergy:
                pass
            else:
                dctTile.itemset(ij2, (abs(dctItem1) + self.dctEnergy)*np.sign(dctItem1))

        # dbg += "new ({}, {})".format(dctTile.item(ij1), dctTile.item(ij2))

        # print(dctTile)
        tile = idct2(dctTile)

        # print(dbg)
        return tile

    def extractBitFromTile(self, tile: np.ndarray, ij1, ij2):
        dctTile = dct2(tile)

        # print(dctTile.astype(int))

        dctItem1 = dctTile.item(ij1)
        dctItem2 = dctTile.item(ij2)

        diff = abs(dctItem1) - abs(dctItem2)

        if diff >= 0: return 0
        else: return 1


    def extractStegoMessage(self) -> str:
        # todo check inputs
        # todo check if size mod 8 = 0

        r, g, b = self._image.split()

        tiles = devideToTiles(np.array(b), 8)

        random.seed(self.seed)

        payload = []

        # os.remove("read.txt")
        # f = open("read.txt", "w+")

        for n in range(0, len(tiles)):
            for m in range(0, len(tiles[0])):
                ij1 = rollSecondDiagonalIndex(self.window)
                ij2 = rollSecondDiagonalIndex(self.window, [ij1])

                # f.write(str((ij1, ij2)) + "\n")

                payload.append(self.extractBitFromTile(tiles[n][m], ij1, ij2))

        # f.close()

        return self.decodePayload(payload, self._eof)


    def getContainerVolume(self) -> int:
        # todo check inputs

        return (self._image.size[0] // 8) * (self._image.size[1] // 8)
