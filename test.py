from tkdnd_wrapper import TkDND
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Photoeditor import PhotoEditor
from PrintImage import printImage
from os import remove

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.filename = "No-img.png"
        self.parent = parent
        self.dnd = TkDND(root)
        self.parent.title('Фотопечать')
        self.parent.resizable(False, False)
        self.parent.geometry('800x500')

        self.topFrame = tk.Frame(self.parent, height=500, width=800, bg='gray')
        self.topFrame.pack(side=tk.TOP, expand=True, fill='both')
        self.buttonsFrame = tk.Frame(self.topFrame, height=500, width=200, bg='gray')
        self.buttonsFrame.pack(side=tk.RIGHT, expand=False, fill='both')
        self.imageFrame = tk.Frame(self.topFrame, height=500, width=600)
        self.imageFrame.pack(side=tk.RIGHT, expand=True, fill='both')

        load = Image.open("No-img.png")
        render = ImageTk.PhotoImage(load)

        self.img = tk.Label(self.imageFrame, image=render, background='white')
        self.img.image = render
        self.img.pack(expand=True, fill="both")

        self.editPhoto = tk.Button(self.buttonsFrame, text='Редактировать Фото', font=30, wraplength=115, justify=tk.CENTER, bd=5,
                              command=self.openPhotoEditor)
        self.printPhoto = tk.Button(self.buttonsFrame, text='Печать', font=30, wraplength=115, justify=tk.CENTER, bd=5,
                               command=self.printPhoto)
        self.resetPhoto = tk.Button(self.buttonsFrame, text='Сброс', font=30, wraplength=80, justify=tk.CENTER, bd=5,
                               command=self.resetPhoto)

        self.editPhoto.pack(expand=True, fill='both')
        self.printPhoto.pack(expand=True, fill='both')
        self.resetPhoto.pack(expand=True, fill='both')

        self.dnd.bindtarget(self.img, self.handle, 'text/uri-list')

        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

    def handle(self, event):
            global filename
            filename = event.data[1:len(event.data) - 1]
            load = Image.open(event.data[1:len(event.data) - 1])
            load = load.resize((self.imageFrame.winfo_width(), self.imageFrame.winfo_height()))
            render = ImageTk.PhotoImage(load)
            event.widget.configure(image=render)
            event.widget.image = render

    def on_closing(self):
        if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
            try:
                remove('temp.png')
            except:
                pass
            self.parent.destroy()

    def printPhoto(self):
        printImage("temp.png")
        pass

    def openPhotoEditor(self):
        PhotoEditor(self.img, self.filename, self.parent)
        pass

    def resetPhoto(self):
        load = Image.open(filename)
        render = ImageTk.PhotoImage(load)
        self.img.configure(image=render)
        self.img.image = render
        pass

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

