from abc import ABC
from PIL import Image

from typing import List
byteList = List[int]


class Stego(ABC):
    def __init__(self, image: Image):
        self.image = image
        self.payload = None
        self.volume = None
        self.message = None



    def menu(self) -> None:
        raise NotImplementedError("Must override menu()")

    def menuPostMain(self) -> None:
        while True:
            print('''    1) print info\n    2) save image\n    0) return\n''')

            userInput = input("Enter a number: ")
            print()

            from old.main import menuChoiceCheck

            if not menuChoiceCheck(userInput, [0, 1, 2]):
                continue
            userInput = int(userInput)

            if userInput == 0: return

            if userInput == 1:
                self.printInfo()
            else:
                self.returnStegoImage().save(input("Save as ({input}.bmp): ") + ".bmp")
                print()


    def setPayload(self) -> None:
        payloadSuccess = False

        while not payloadSuccess:
            userInput = input("Set the payload (string, utf-8): ")
            print()

            if userInput == "0":
                return None

            if not all(ord(c) < 256 for c in userInput):
                print("Only utf-8 characters allowed\n")
                continue



            self.message = userInput

            bitArray = self._encodePayload(userInput)


            if len(bitArray) > self.volume:
                print("Payload ({} bites) bigger than container volume ({} bites).\n".format(len(bitArray), self.volume))
                continue

            self.payload = bitArray


            payloadBinaryString = ''.join(str(bit) for bit in bitArray)
            payloadBinaryString = ' '.join(payloadBinaryString[i:i + 8] for i in range(0, len(payloadBinaryString), 8))

            print("Payload set: {}\nBinary representation  (where 00000000 is EOF):\n{}\n\n".format(self.message, payloadBinaryString))
            payloadSuccess = True

    @staticmethod
    def _retrievePayloadFromImage(img: Image) -> byteList:
        raise NotImplementedError("Must override _retrievePayloadFromImage()")

    @staticmethod
    def _encodePayload(string: str) -> byteList:
        byteListString = ''

        for i in bytearray(string, encoding='utf-8'):
            byteListString += format(i, '#010b')[2:]
            # print("ByteArrayString: " + str(byteListString))
        byteListString += "00000000"  # eof

        byteArray = []

        for bit in byteListString:
            byteArray.append(int(bit))

        return byteArray

    @staticmethod
    def _decodePayload(byteList: list) -> str:
        string = ''

        for i in range(0, len(byteList), 8):
            char = chr(int(''.join(str(b) for b in byteList[i : i + 8]), 2))  # for heck's sake

            if char == '\00': break  # double check

            string += char

        return string

    def printInfo(self) -> None:
            raise NotImplementedError("Must override printInfo()")

    def returnStegoImage(self) -> Image:
        raise NotImplementedError("Must override returnStegoImage()")

    @staticmethod
    def printStegoMessage(img: Image) -> None:
        raise NotImplementedError("Must override printStegoMessage() as 'print(Child.getStegoMessage(img))'")

    @staticmethod
    def getStegoMessage(img: Image) -> str:
        raise NotImplementedError("Must override getStegoMessage()")

