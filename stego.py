from abc import ABC
from PIL import Image

class Stego(ABC):
    def __init__(self, image: Image):
        self.image = image
        self.payload = None
        self.volume = None
        self.message = None

    def menu(self):
        pass

    def setPayload(self):
        payloadSuccess = False

        while not payloadSuccess:
            userInput = input("Set the payload (string, utf-8): ")

            if userInput == "0":
                return

            if not all(ord(c) < 256 for c in userInput):
                print("Only utf-8 characters allowed\n")
                continue

            self.message = userInput
            byteArrayString = ''.join(format(i, 'b') for i in bytearray(userInput, encoding='utf-8'))
            byteArray = []

            for bit in byteArrayString:
                byteArray.append(int(bit))

            if len(byteArray) > self.volume:
                print("Payload ({} bites) bigger than container volume ({} bites).\n".format(len(byteArray), self.volume))
                continue

            self.payload = byteArray.append([1, 1, 1, 1, 1, 1, 1, 1])

            print("Payload set: {}\nas: {}\n\n".format(self.message, byteArrayString))
            payloadSuccess = True

    def printInfo(self):
            pass

    def getStegoImage(self):
        pass