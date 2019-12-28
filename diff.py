from PIL import Image, ImageChops

def exadurate(image: Image, diff: Image) -> Image:
    if image.size != diff.size: raise ValueError("Images dimentions are not equal")

    for y in range(0, image.size[0]):
        for x in range(0, image.size[1]):
            if diff.getpixel((x, y)) != (0, 0, 0):
                image.putpixel((x, y), (0, 0, 0))

    return image

def saveDiff(image1path: str, image2path: str, diffName: str = "diff.bmp") -> None:
    im1 = Image.open(image1path)
    im2 = Image.open(image2path)

    difference = ImageChops.difference(im1, im2)
    difference = exadurate(im2, difference)

    difference.save(diffName)


if __name__ == "__main__":

    saveDiff("./l.bmp", "./block.bmp", "diff block.png")
    saveDiff("./l.bmp", "./cross.bmp", "diff cross.png")
    saveDiff("./l.bmp", "./quant.bmp", "diff quant.png")



