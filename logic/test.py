import random

from logic.Block import Block

if __name__ == "__main__":

    b = Block()
    b.importImage("./l.bmp")
    b.setMessage("Hello world!")
    b.blockSide = 8
    b.generateStegoImage().save("s.bmp")

    b.importImage("./s.bmp")
    print(b.extractStegoMessage())
    print(b.payload)






