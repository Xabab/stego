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
import itertools
import random
from typing import List, Tuple

from PIL import Image

from logic.KochZhao import KochZhao
from logic.Stego import Stego
from logic.util.dctEssentials import *
import numpy as np

from logic.util.randomIndexes import rollLowFreqIndex


class JessicaFridrich(Stego):
    def __init__(self):
        super().__init__()

        self.alpha = None
        self.window = None
        self.seed = None

    def _getZeroExpectedValueImageSignal(self, matrix: np.ndarray) -> np.ndarray:  # G
        expectedValue = matrix.mean()
        standardDeviation = np.std(matrix)

        x, y = matrix.shape

        return (1024 / np.sqrt(x * y)) * ((matrix - expectedValue) / standardDeviation)

    def _thetaNext(self, alpha: float, thetaPrevious: float) -> float:  # T i+1
        return ((1 + alpha) / (1 - alpha)) * thetaPrevious

    def _thetaAppendNext(self, thetaList: List):
        thetaList.append(self._thetaNext(self.alpha, thetaList[-1:][0]))

    def _indexFunction(self, x: int, thetaList: List) -> Tuple[int, int]:  # ind(x)
        if len(thetaList) == 0: thetaList.append(1)

        try:
            index = (next(idx for idx, value in enumerate(thetaList) if value > abs(x)))
            return (-1) ** index, index - 1
        except StopIteration:
            while thetaList[-1:][0] < abs(x):
                self._thetaAppendNext(thetaList)
                print(thetaList)

            return (-1) ** (len(thetaList) - 1), (len(thetaList) - 1)

    def _getIj(self, tile: np.array, ij: List[Tuple[int, int]] = None):
        newIj = rollLowFreqIndex(self.window, ij)

        if tile.item(newIj) < 1: return self._getIj(tile, ij)
        return newIj

    def generateStegoImage(self) -> Image:

        r, g, b = self._image.split()

        tiles = devideToTiles(np.array(b), 8)

        random.seed(self.seed)

        payload = list(map(lambda l: l * 2 - 1, self._payload))

        thetaList = []

        ijmap = []

        raise NotImplementedError # todo

        for n in range(0, len(tiles)):
            for m in range(0, len(tiles[0])):
                # for i in range(0, self.embedCount):
                #     ijs.append(self._getIj(tiles[n][m], ijs))
                # self._embedToTile(tiles[b][m], ijs, payload[n*8 + m], thetaList)

                self._embedToTile(tiles[b][m], ijmap, payload[n * 8 + m], thetaList)

    def _embedToTile(self, tile, ijs: List[Tuple[int, int]], payload: int, thetaList: List[int]):
        for ij in ijs:
            indexFunc = self._indexFunction(tile.item(ij), thetaList)

            if payload == indexFunc[0]:
                if indexFunc[1] + 1 == len(thetaList):
                    self._thetaAppendNext(thetaList)

                tile.itemset(ij, np.mean(thetaList[indexFunc[1]],
                                         thetaList[indexFunc[1] + 1]) * np.sign(tile.item(ij)))

            else:
                if indexFunc[1] + 1 == len(thetaList):
                    self._thetaAppendNext(thetaList)
                    self._thetaAppendNext(thetaList)

                mean = [
                    np.mean(thetaList[indexFunc[1] - 1], thetaList[indexFunc[1]]) * np.sign(tiles[n][m].item(ij)),
                    np.mean(thetaList[indexFunc[1] + 1], thetaList[indexFunc[1] + 2]) * np.sign(tiles[n][m].item(ij))
                ]

                tile.itemset(ij, min(mean, key=lambda x: abs(x - tile.item(ij))))

    def extractStegoMessage(self) -> str:
        pass

    def getContainerVolume(self) -> int:
        return (self._image.size[0] // 8) * (self._image.size[1] // 8)
