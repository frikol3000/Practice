from PIL import Image, ImageTk
import cv2
import numpy as np
import img_modifier.color_filter as filt
import tkinter as tk

filename = "No-img.png"

# # sepia = img.copy()
# # filt.sepia(sepia)
# # sepia = sepia.resize((100, 100))
# # sepia.show()
#
# dict ={'sepia' : None, 'black_white': None, 'negative': None}
#
# for i in dict:
#     dict[i] = img.copy()
#     filt.setFilter(i, dict[i])
#     dict[i] = dict[i].resize((200, 200))
#
# dict['sepia'].show()

root = tk.Tk()
root.title('Фотопечать')
root.resizable(False, False)
root.geometry('800x500')

load = Image.open("No-img.png").convert("RGB")
dict = {'sepia': None, 'black_white': None, 'negative': None}
for i in dict:
    dict[i] = load.copy()
    filt.setFilter(i, dict[i])
    dict[i] = dict[i].resize((160, 90))
sepia = ImageTk.PhotoImage(dict['sepia'])
# print(type(ImageTk.PhotoImage(sepia)))
sepia1 = tk.Button(root, image=sepia)
sepia1.pack(side=tk.LEFT)
# black_white1 = tk.Button(root, image=ImageTk.PhotoImage(image=dict['black_white']))
# black_white1.pack(side=tk.LEFT)
# negative1 = tk.Button(root, image=ImageTk.PhotoImage(image=dict['negative']))
# negative1.pack(side=tk.LEFT)

root.mainloop()