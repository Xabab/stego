from PIL import Image, ImageChops
im1 = Image.open("./l.bmp")
im2 = Image.open("./stego.bmp")

difference = ImageChops.difference(im1, im2)
difference.save("diff.png")