from numpy import cos, sqrt, pi
import numpy as np
import copy


def c(i, j, N):
    if i == 0:
        return 1/sqrt(N)
    else:
        return sqrt(2/N) * cos((2*j + 1) * i * pi / (2 * N))


def getDCTmatrix(N):
    dctmatrix = np.ndarray((N, N), dtype=float)
    for i in range(0, N):
        for j in range(0, N):
            dctmatrix[i][j] = c(i, j, N)

    return dctmatrix


def _dct(arr):
    N = len(arr)

    dctmatrix = getDCTmatrix(N)

    nparr = np.array([np.array(row) for row in arr])

    out = np.dot(dctmatrix, nparr)
    out = np.dot(out, dctmatrix.transpose())
    out = out.astype(dtype=int)

    return out


def _dctinv(arr):
    N = len(arr)

    dctmatrix = np.linalg.inv(getDCTmatrix(N))

    nparr = np.array([np.array(row) for row in arr])

    out = np.dot(dctmatrix, nparr)
    out = np.dot(out, dctmatrix.transpose())
    out = out.astype(dtype=int)

    return out


def _qualitymatrix(K, N):
    matrix = np.ndarray((N, N), dtype=int)

    for y in range(0, N):
        for x in range(0, N):
            matrix[x][y] = 1 + (1 + x + y) * K

    return matrix


def _jpeg(arr, K):
    arr = np.array(arr)
    arr = arr.astype(int)

    out =_dct(arr)
    outq = np.divide          (out, _qualitymatrix(K, len(arr))).astype(int)
    outq = _dctinv(np.multiply(outq, _qualitymatrix(K, len(arr))))

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


if __name__ == "__main__":
    array = \
        [
            [12, 45, 75, 25, 85, 23, 12, 75],
            [45, 85, 23, 123, 23, 86, 25, 85],
            [12, 45, 75, 25, 85, 23, 12, 75],
            [1, 123, 23, 86, 75, 27, 126, 23],
            [12, 45, 75, 25, 85, 23, 12, 75],
            [1, 123, 23, 86, 75, 27, 126, 23],
            [12, 45, 85, 23, 12, 75, 45, 75],
            [25, 85, 25, 85, 45, 75, 25, 85]
        ]

    array = np.array(array)

    print(array - 128)




