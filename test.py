from tkdnd_wrapper import TkDND
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Photoeditor import PhotoEditor

filename = "No-img.png"

def openPhotoEditor():
    PhotoEditor(filename, root)
    pass

def printPhoto():
    pass

def resetPhoto():
    pass

root = tk.Tk()
dnd = TkDND(root)
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
    render = ImageTk.PhotoImage(load)
except:
    load = Image.open("No-img.png")
    render = ImageTk.PhotoImage(load)

img = tk.Label(booksFrame, image=render, background='white')
img.image = render
img.pack(expand=True)

editPhoto = tk.Button(buttonsFrame, text='Редактировать Фото', font=30, wraplength=115, justify=tk.CENTER, bd=5, command=openPhotoEditor)
printPhoto = tk.Button(buttonsFrame, text='Печать', font=30, wraplength=115, justify=tk.CENTER, bd=5, command=printPhoto)
resetPhoto = tk.Button(buttonsFrame, text='Сброс', font=30, wraplength=80, justify=tk.CENTER, bd=5, command=resetPhoto)

editPhoto.pack(expand=True, fill='both')
printPhoto.pack(expand=True, fill='both')
resetPhoto.pack(expand=True, fill='both')

def handle(event):
    global filename
    filename = event.data[1:len(event.data)-1]
    load = Image.open(event.data[1:len(event.data)-1])
    render = ImageTk.PhotoImage(load)
    event.widget.configure(image=render)
    event.widget.image = render

dnd.bindtarget(img, handle, 'text/uri-list')

def on_closing():
    if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
