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
from math import sqrt, cos, pi, log
from typing import List

import numpy as np
from PIL import Image

from logic.Stego import Stego



class Spectral(Stego):
    def __init__(self):
        super().__init__()
        self.blockSide = None
        self.energy = None
        raise NotImplementedError

    @staticmethod
    def getOrthogonalMatrix(side: int) -> np.ndarray:
        if side < 2:
            raise ValueError("Side must be bigger or equal to 2")
        if not log(side, 2).is_integer():
            raise ValueError("Side have to be a power of two")

        iterations = int(log(side, 2))

        orthogonalMatrix = np.ndarray(shape=(2, 2), dtype=int, buffer=np.array([1, 1, 1, -1]))

        for i in range(1, iterations):
            ortRow1 = np.concatenate((orthogonalMatrix, orthogonalMatrix     ), axis=1)
            ortRow2 = np.concatenate((orthogonalMatrix, orthogonalMatrix * -1), axis=1)

            orthogonalMatrix = np.concatenate((ortRow1, ortRow2), axis=0)

        return orthogonalMatrix

    @staticmethod
    def _getPayloadBlocks(payload, side) -> List[np.ndarray]:
        if payload is None:
            raise TypeError()
        if side is None:
            raise TypeError() # todo fix check

        size = side ** 2

        listOfMatrices = []

        for block in range(0, int(np.ceil(len(payload)/size))):
            matrix = []
            for i in range(0, size):
                try:
                    matrix.append(int(payload[block*size + i]))
                except IndexError:
                    matrix.append(0)

            listOfMatrices.append(np.ndarray(shape=(side, side), dtype= int, buffer = np.array(matrix)))

        return listOfMatrices

    def getContainerVolume(self) -> int:
        raise NotImplementedError

    def generateStegoImage(self) -> Image:
        # todo check inputs

        payload = (np.array(self._payload) * 2 - 1).tolist()
        payload = Spectral._getPayloadBlocks(payload, self.blockSide)

        ortMatrix = Spectral.getOrthogonalMatrix(self.blockSide)

        raise NotImplementedError


    def extractStegoMessage(self) -> str:
        raise NotImplementedError



