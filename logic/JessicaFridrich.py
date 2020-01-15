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
import random
from typing import List

from PIL import Image

from logic.KochZhao import KochZhao
from logic.Stego import Stego
from logic.util.dctEssentials import *
import numpy as np

class JessicaFridrich(Stego):
    def __init__(self):
        super().__init__()

        self.alpha = None
        self.window = None
        self.embedCount = None
        self.seed = None

    def _getZeroExpectedValueImageSignal(self, matrix: np.ndarray) -> np.ndarray:  # G
        expectedValue = matrix.mean()
        standardDeviation = np.std(matrix)

        x, y = matrix.shape

        return (1024 / np.sqrt(x * y)) * ((matrix - expectedValue) / standardDeviation)

    def _thetaNext(self, alpha: float, thetaPrevious: float) -> float:  # T i+1
        return ((1 + alpha) / (1 - alpha)) * thetaPrevious


    def _indexFunction(self, x: int, thetaList: List) -> int:  # ind(x)
        if len(thetaList) == 0: thetaList.append(1)

        try:
            return (-1) ** (next(idx for idx, value in enumerate(thetaList) if value > abs(x)))
        except StopIteration:
            while thetaList[-1:][0] < abs(x):
                thetaList.append(self._thetaNext(self.alpha, thetaList[-1:][0]))
                print(thetaList)

            return (-1) ** (len(thetaList) - 1)


    def generateStegoImage(self) -> Image:
        r, g, b = self._image.split()

        tiles = devideToTiles(np.array(b), 8)

        random.seed(self.seed)

        for n in range(0, len(tiles)):
            for m in range(0, len(tiles[0])):
                raise NotImplementedError

    def extractStegoMessage(self) -> str:
        pass

    def getContainerVolume(self) -> int:
        return (self._image.size[0] // 8) * (self._image.size[1] // 8)




