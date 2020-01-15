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
from typing import List, Tuple


def rollSecondDiagonalIndex(window: int, ij: List[Tuple[int, int]] = None, matrixSideSize: int = 8) -> Tuple[int, int]:
    if ij is None:
        ij = []

    i = random.randint(0, matrixSideSize - 1)
    j = (matrixSideSize - 1 - i) + (random.randint(-window, window))
    newIj = (i, j)

    if newIj[1] < 0 or newIj[1] >= 8 or newIj in ij:
        return rollSecondDiagonalIndex(window, ij, matrixSideSize)

    return newIj

def rollLowFreqIndex(window: int, ij: List[Tuple[int, int]] = None, matrixSideSize: int = 8) -> Tuple[int, int]:
    if ij is None:
        ij = []

    i = random.randint(matrixSideSize - window - 1)
    j = random.randint(matrixSideSize - window - 1)

    newIj = (i, j)

    if newIj[1] < 0 or newIj[1] >= 8 or newIj in ij:
        return rollLowFreqIndex(window, ij, matrixSideSize)

    return newIj
