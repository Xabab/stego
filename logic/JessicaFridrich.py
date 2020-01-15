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
from PIL import Image

from logic.KochZhao import KochZhao
from logic.Stego import Stego
from logic.util.dctEssentials import *

class JessicaFridrich(Stego):
    def __init__(self):
        super().__init__()

        self.alpha = None

    def generateStegoImage(self) -> Image:
        pass

    def extractStegoMessage(self) -> str:
        pass

    def getContainerVolume(self) -> int:
        return (self._image.size[0] // 8) * (self._image.size[1] // 8)




