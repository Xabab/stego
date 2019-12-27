from abc import ABC, abstractmethod
from PIL import Image

from typing import List

class Stego(ABC):
    def __init__(self) -> None:
        self.image = None
        self.stegoImage = None
        self.payload = None
        self.message = None
        self._eof = '\00'

    def importImage(self, path: str):
        self.image = Image.open(path)

    def setMessage(self, message: str) -> None:
        self.message = message
        self.payload = self.encodePayload(message, self._eof)


    def encodePayload(self, string: str, eof: str = "") -> List[int]:
        byteListString = ''
        for i in bytearray(string + eof, encoding='utf-8'):
            byteListString += format(i, '#010b')[2:]

        byteArray = []
        for bit in byteListString:
            byteArray.append(int(bit))

        return byteArray


    def decodePayload(self, byteList: List[int], eof: str = "") -> str:
        string = ''

        for i in range(0, len(byteList), 8):
            char = chr(int(''.join(str(b) for b in byteList[i: i + 8]), 2))  # for heck's sake
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
