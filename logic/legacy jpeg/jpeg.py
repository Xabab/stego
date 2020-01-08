import numpy as np
from imageio import imread
import tkinter as tk
from PIL import Image, ImageTk
from test import jpeg

'''
# creating a window
window = tk.Tk()

# displaying source image
tkImg1 = ImageTk.PhotoImage(Image.open(("./lena512.bmp")))
tk.Label(window, image=tkImg1).pack()
'''


# loading source image as an array of int values
image = imread("./lena512.bmp")
image = image.astype(int)


#N = [8, 8, 8, 8, 8 , 8 , 8 , 8 , 16, 16, 16, 32, 32, 32]
#K = [1, 2, 5, 7, 10, 15, 30, 50, 2 , 7 , 15, 2 , 7 , 15]

N = [32]
K = [1]


for i in range(0, len(N)):
    jpegimg = jpeg(image, N[i], K[i])
    jpegimg = Image.fromarray(np.uint8(jpegimg), "L")
    jpegimg.save("out/jpeg n {} K {}.bmp".format(N[i], K[i]))

    print('"jpeg n {} K {}.bmp" done!'.format(N[i], K[i]))



'''
canvas = tk.Canvas(window, width=jpegimg.width, height=jpegimg.height, bg="#000000")
canvas.pack(side=tk.LEFT)


tkImg2 = ImageTk.PhotoImage(jpegimg)
canvas.create_image((jpegimg.width/2, jpegimg.height/2), image=tkImg2, state="normal")


# starting window loop
window.mainloop()
'''
