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
import random
from math import sqrt, cos, pi
from typing import Tuple

import numpy as np
from PIL import Image

from logic.Stego import Stego

def c(i, j, N):
    if i == 0:
        return 1/sqrt(N)
    else:
        return sqrt(2/N) * cos((2*j + 1) * i * pi / (2 * N))


def getDctMatrix(N):
    dctmatrix = np.ndarray((N, N), dtype=float)
    for i in range(0, N):
        for j in range(0, N):
            dctmatrix[i][j] = c(i, j, N)

    return dctmatrix


def applyDct(matrix):
    N = len(matrix)

    dctmatrix = getDctMatrix(N)

    nparr = np.array([np.array(row) for row in matrix])

    out = np.dot(dctmatrix, nparr)
    out = np.dot(out, dctmatrix.transpose())
    out = out.astype(dtype=int)

    return out


def applyInverseDct(matrix):
    N = len(matrix)

    dctmatrix = np.linalg.inv(getDctMatrix(N))

    nparr = np.array([np.array(row) for row in matrix])

    out = np.dot(dctmatrix, nparr)
    out = np.dot(out, dctmatrix.transpose())
    out = out.astype(dtype=int)

    return out


def generateQualityMatrix(K, N):
    matrix = np.ndarray((N, N), dtype=int)

    for y in range(0, N):
        for x in range(0, N):
            matrix[x][y] = 1 + (1 + x + y) * K

    return matrix


def _jpeg(arr, K):
    arr = np.array(arr)
    arr = arr.astype(int)

    out = applyDct(arr)
    outq = np.divide(out, generateQualityMatrix(K, len(arr))).astype(int)
    outq = applyInverseDct(np.multiply(outq, generateQualityMatrix(K, len(arr))))

    return outq


def devideToTiles(arr, N):
    outNxNtile = []
    outNxNrow = []
    outNxNarray = []

    for y in range(0, len(arr), N):
        for x in range(0, len(arr), N):
            for subrow in arr[y: y+N]:
                outNxNtile.append(subrow[x:x+N])
            outNxNrow.append(outNxNtile)
            outNxNtile = []
        outNxNarray.append(outNxNrow)
        outNxNrow = []

    outNxNarray = np.array(outNxNarray)

    return outNxNarray


def assembleFromTiles(tiles):
    return np.concatenate(np.concatenate(tiles, axis=1), axis=1)


def jpeg(imageAsArray, N, K):

    image = copy.deepcopy(imageAsArray)

    image -= 128

    image = devideToTiles(image, N)

    for tileRowI in range(0, len(image)):
        for tileI in range(0, len(image[tileRowI])):
            image[tileRowI][tileI] = _jpeg(image[tileRowI][tileI], K)

    image = assembleFromTiles(image)

    image += 128

    return image

class KochJao(Stego):
    def __init__(self):
        super().__init__()
        self.dctEnergy = None
        self.window = None     # as distance from the second diagonal
        self.seed = None

    def generateStegoImage(self) -> Image:
        # todo check inputs
        # todo check if size mod 8 = 0

        r, g, b = self.image.split()

        tiles = devideToTiles(np.array(b), 8)


        random.seed(self.seed)


        for n in range(0, len(tiles)):
            for m in range(0, len(tiles[0])):
                ij1 = self._rollIndex()
                ij2 = self._rollIndex(ij1)


                try:
                    tiles[n][m] = self.embedBitToTile(tiles[n][m], self.payload[n*len(tiles[0]) + m], ij1, ij2)
                except IndexError:
                    b = assembleFromTiles(tiles)
                    return Image.merge("RGB", (r, g, Image.fromarray(b, mode="L")))

        b = assembleFromTiles(tiles)
        return Image.merge("RGB", (r, g, Image.fromarray(b, mode="L")))

    def _rollIndex(self, ij: Tuple[int, int] = (-1, -1)):
        i = random.randint(0, 7)
        _ij = (i, (7 - i) + (random.randint(-self.window, self.window)))

        if _ij[1] < 0 or _ij[1] >= 8 or _ij == ij:
            return self._rollIndex(ij)

        return _ij

    def embedBitToTile(self, tile: np.ndarray, bit: str, ij1, ij2):
        # np.set_printoptions(threshold=10, edgeitems=8, linewidth=100)

        dctTile = applyDct(tile)

        # print()

        # print((ij1, ij2))
        # print(dctTile)


        dct1 = dctTile.item(ij1)
        dct2 = dctTile.item(ij2)

        diff = abs(dct1) - abs(dct2)

        dbg = "Old ({}, {}), ".format(dct1, dct2)
        dbg += "abs diff {}, payload {}, ".format(diff, bit)

        if int(bit) == 1:
            if diff >= self.dctEnergy:
                pass
            else:
                dctTile.itemset(ij1, dct2 + self.dctEnergy)
        else:  # if int(bit) == 0:
            if diff <= -self.dctEnergy:
                pass
            else:
                dctTile.itemset(ij2, dct1 + self.dctEnergy)

        dbg += "new ({}, {})".format(dctTile.item(ij1), dctTile.item(ij2))

        # print(dctTile)
        tile = applyInverseDct(dctTile)

        # print(dbg)
        return tile

    def extractBitFromTile(self, tile: np.ndarray, ij1, ij2):
        dctTile = applyDct(tile)

        dct1 = dctTile.item(ij1)
        dct2 = dctTile.item(ij2)

        diff = abs(dct1) - abs(dct2)

        if diff >= 0: return 1
        else: return 0


    def extractStegoMessage(self) -> str:
        # todo check inputs
        # todo check if size mod 8 = 0
        # todo check window is odd

        r, g, b = self.image.split()

        tiles = devideToTiles(np.array(b), 8)

        random.seed(self.seed)

        payload = []


        for n in range(0, len(tiles)):
            for m in range(0, len(tiles[0])):
                ij1 = self._rollIndex()
                ij2 = self._rollIndex(ij1)

                payload.append(self.extractBitFromTile(tiles[n][m], ij1, ij2))


        return self.decodePayload(payload)


    def getContainerVolume(self) -> int:
        # todo check inputs

        return (self.image.size[0]//8) * (self.image.size[1]//8)