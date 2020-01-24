import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import filedialog
from Photoeditor import PhotoEditor
import os

filename = "No-img.png"

def openPhotoEditor():
    PhotoEditor(filename, root)
    pass

def printPhoto():
    pass

def resetPhoto():
    pass

def setPath():
    global filename
    filename = filedialog.askopenfilename(parent=root, initialdir="/", title="Открыть изображение",
                                               filetypes=(("Изображения", "*.jpg, *.png"), ("all files", "*.*")))


    if filename == "":
        filename = "No-img.png"
    else:
        filename = os.path.split(filename)[1]

    load = Image.open(filename)
    load = load.resize((650, 500))
    render = ImageTk.PhotoImage(load)

    img.configure(image=render)
    img.image = render

root = tk.Tk()
root.title('Фотопечать')
root.resizable(False, False)
root.geometry('800x500')

topFrame = tk.Frame(root, height=500, width=800, bg='gray')
topFrame.pack(side=tk.TOP, expand=True, fill='both')
buttonsFrame = tk.Frame(topFrame, height=500, width=200, bg='gray')
buttonsFrame.pack(side=tk.RIGHT, expand=True, fill='both')
booksFrame = tk.Frame(topFrame, height=500, width=600)
booksFrame.pack(side=tk.RIGHT, expand=True, fill='both')

try:
    load = Image.open(filename)
    load = load.resize((650, 500))
    render = ImageTk.PhotoImage(load)
except:
    load = Image.open("No-img.png")
    load = load.resize((650, 500))
    render = ImageTk.PhotoImage(load)

img = tk.Label(booksFrame, image=render, background='white')
img.image = render
img.pack(expand=True)

addPhoto = tk.Button(buttonsFrame, text='Загрузить фото', font=30, wraplength=80, justify=tk.CENTER, bd=5, command=setPath)
editPhoto = tk.Button(buttonsFrame, text='Редактировать Фото', font=30, wraplength=115, justify=tk.CENTER, bd=5, command=openPhotoEditor)
printPhoto = tk.Button(buttonsFrame, text='Печать', font=30, wraplength=115, justify=tk.CENTER, bd=5, command=printPhoto)
resetPhoto = tk.Button(buttonsFrame, text='Сброс', font=30, wraplength=80, justify=tk.CENTER, bd=5, command=resetPhoto)

addPhoto.pack(expand=True, fill='both')
editPhoto.pack(expand=True, fill='both')
printPhoto.pack(expand=True, fill='both')
resetPhoto.pack(expand=True, fill='both')


def on_closing():
    if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
