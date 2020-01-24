import img_modifier.color_filter as filt
import cv2
from PIL import Image, ImageTk


path = "1.png"

img = Image.open(path) # create a new black image

def sepia(img):
    pix = img.load()
    for i in range(img.width):
        for j in range(img.height):
            s = sum(pix[i, j]) // 3
            k = 30
            pix[i, j] = (s + k * 2, s + k, s)


sepia(img)
img.show()


