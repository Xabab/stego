import numpy as np
from PIL import Image
from logic.JessicaFridrich import JessicaFridrich
from logic.util.dctEssentials import dct2

matrix = np.array(Image.open("./l.bmp").convert("RGB").getchannel("B"))

matrix = JessicaFridrich._getZeroExpectedValueImageSignal(JessicaFridrich(), matrix)

print(max(np.max(tyle) for tyle in dct2(matrix)))




