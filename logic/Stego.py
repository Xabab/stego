#  Copyright (c) 2019 Xabab
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

from abc import ABC, abstractmethod
from PIL import Image

from typing import List, Callable


class Stego(ABC):
    def __init__(self) -> None: # todo change signature for using kwargs
        self._image = None
        self._payload = None
        self.message = None
        self._eof = '\00'

    def importImage(self, path: str):
        self._image = Image.open(path).convert("RGB")

    def setMessage(self, message: str, encoder: Callable[[str, str], List[int]] = None) -> None:
        if encoder is None:
            encoder = self.encodePayload

        self.message = message
        self._payload = encoder(message, self._eof)

    @staticmethod
    def encodePayload(string: str, eof: str = "") -> List[int]:
        bitListString = ''
        for i in bytearray(string + eof, encoding='utf-8'):
            bitListString += format(i, '#010b')[2:]

        bitArray = []
        for bit in bitListString:
            bitArray.append(int(bit))

        return bitArray

    @staticmethod
    def decodePayload(bitList: List[int], eof: str = "") -> str:
        string = ''

        for i in range(0, len(bitList), 8):
            char = chr(int(''.join(str(b) for b in bitList[i: i + 8]), 2))  # for heck's sake
            string += char

            if string[-len(eof):] == eof:

                string = string[:-len(eof)]
                break

        return string

    @abstractmethod
    def generateStegoImage(self) -> Image:
        raise NotImplementedError("Stego.generateStegoImage() is abstract")

    @abstractmethod
    def extractStegoMessage(self) -> str:
        raise NotImplementedError("Stego.extractStegoMessage() is abstract")

    @abstractmethod
    def getContainerVolume(self) -> int:
        raise NotImplementedError("Stego.getContainerVolume() is abstract")
