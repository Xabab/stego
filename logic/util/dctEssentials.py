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
import numpy as np
from scipy.fftpack import dct, idct


def dct2(matrix):
    return dct(dct(matrix.T, norm='ortho').T, norm='ortho')


def idct2(matrix):
    return idct(idct(matrix.T, norm='ortho').T, norm='ortho')


def devideToTiles(arr, N):
    outNxNtile = []
    outNxNrow = []
    outNxNarray = []

    for y in range(0, len(arr), N):
        for x in range(0, len(arr), N):
            for subrow in arr[y: y + N]:
                outNxNtile.append(subrow[x:x + N])
            outNxNrow.append(outNxNtile)
            outNxNtile = []
        outNxNarray.append(outNxNrow)
        outNxNrow = []

    outNxNarray = np.array(outNxNarray)

    return outNxNarray


def assembleFromTiles(tiles):
    return np.concatenate(np.concatenate(tiles, axis=1), axis=1)