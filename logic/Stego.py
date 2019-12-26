from abc import ABC
from PIL import Image

from typing import List

class Stego(ABC):
    def __init__(self) -> None:
        self.image = None
        self.stegoImage = None
        self.payload = None
        self.volume = None
        self.message = None

    def importImage(self, path:str):
        self.image = Image.open(path)

    def setMessage(self, message: str) -> None:
        self.message = message
        self.payload = self._encodePayload(message)

    @staticmethod
    def _encodePayload(string: str) -> List[int]:
        byteListString = ''

        for i in bytearray(string, encoding='utf-8'):
            byteListString += format(i, '#010b')[2:]
        byteListString += "00000000"  # eof

        byteArray = []

        for bit in byteListString:
            byteArray.append(int(bit))

        return byteArray

    @staticmethod
    def _decodePayload(byteList: List[int]) -> str:
        string = ''

        for i in range(0, len(byteList), 8):
            char = chr(int(''.join(str(b) for b in byteList[i : i + 8]), 2))  # for heck's sake

            if char == '\00': break  # double check

            string += char

        return string

    def generateStegoImage(self) -> Image:
        raise NotImplementedError("Stego.generateStegoImage()")

    def extractStegoMessage(self) -> str:
        raise NotImplementedError("Stego.extractStegoMessage()")

