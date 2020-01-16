import itertools

import numpy as np
from PIL import Image
from logic.JessicaFridrich import JessicaFridrich
from logic.util.dctEssentials import dct2

matrix = np.array(Image.open("./l.bmp").convert("RGB").getchannel("B"))



ijs = [*range(0, 8)]
ijs = list(itertools.product(ijs, ijs))
ijs = [t for t in ijs if (t[0] + t[1]) / 2 >= 6]

print(ijs)



