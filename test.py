import random
from itertools import repeat

from diff import saveDiff
from logic.Quant import Quant
from logic.Block import Block
from logic.Cross import Cross

if __name__ == "__main__":
    message = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis sollicitudin augue ut augue pretium, a lacinia lacus posuere. 
    Mauris vel mauris lorem. Etiam varius tempus diam in sodales. Morbi ultricies nisi eu commodo dictum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi tempus tempus malesuada. 
    Donec gravida eget sapien et tincidunt. Pellentesque non bibendum dui. Quisque non sem sit amet tortor aliquam mollis ac in eros. 
    Sed molestie consectetur porta. Mauris egestas lacus libero, nec euismod erat molestie sed. Maecenas feugiat gravida turpis non sodales. Mauris at consectetur leo. 
    Mauris aliquet feugiat ligula a cursus. Duis in nibh justo. Quisque eleifend imperdiet sapien, vitae lobortis lectus ultricies eu. 
    Nullam non iaculis lacus. Vestibulum quis justo enim. Phasellus tristique tortor quis dui viverra mattis. Nunc gravida iaculis lorem, a tempus nisl accumsan in. 
    Morbi ullamcorper egestas leo, in egestas magna tempus sed. Donec vitae urna a nisi blandit porttitor vel dignissim massa. 
    Phasellus finibus risus quis nibh ultricies imperdiet. Proin tempor ex at sagittis elementum. Suspendisse potenti."""


    c = Cross()
    c.importImage("l.bmp")
    c.seed = 1
    c.interval = 5
    c.energy = 0.15
    c.repeatCount = 8
    c.cross = 1
    c.setMessage(message)
    c.generateStegoImage().save("cross.bmp")

    c.importImage("cross.bmp")
    print(c.extractStegoMessage())

    saveDiff("l.bmp", "cross.bmp", "diff cross.png")


    b = Block()
    b.importImage('l.bmp')
    b.blockSide = 5
    b.setMessage(message)
    b.generateStegoImage().save("block.bmp")

    b.importImage("block.bmp")
    print(b.extractStegoMessage())

    saveDiff("l.bmp", "block.bmp", "diff block.png")


    q = Quant()

    q.seed = 1
    q.generateKey()
    q.importImage("l.bmp")
    q.setMessage(message)
    q.generateStegoImage().save("quant.bmp")

    q.importImage("quant.bmp")
    print(q.extractStegoMessage())

    saveDiff("l.bmp", "quant.bmp", "diff quant.png")







