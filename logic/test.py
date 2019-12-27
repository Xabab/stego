import random
from itertools import repeat

from logic.Block import Block
from logic.Cross import Cross

if __name__ == "__main__":


    c = Cross()
    c.importImage("./l.bmp")
    c.seed = 1
    c.interval = 10
    c.energy = 0.1
    c.repeatCount = 10
    c.cross = 1
    c.setMessage("Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet.")

    c.generateStegoImage().save("cross.bmp")
    c.importImage("./cross.bmp")

    print(c.extractStegoMessage())


    '''
    b = Block()
    b.importImage('./l.bmp')
    b.blockSide = 4
    b.setMessage("Lorem ipsum dolor sit amet.")

    b.generateStegoImage().save("block.bmp")
    b.importImage("block.bmp")

    print(b.extractStegoMessage())
    '''

    # c = Cross()

    # print(c.encodePayload(c._eof))









