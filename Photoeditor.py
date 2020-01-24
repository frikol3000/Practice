import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import img_modifier.color_filter as filt
import cv2

class PhotoEditor(tk.Toplevel):
    def __init__(self, filename, master=None):
        tk.Toplevel.__init__(self, master)
        self.filename = filename
        self.master = master
        self.title('Редактор фото')
        self.resizable(False, False)
        self.geometry('500x600')
        self.load = Image.open(self.filename)
        self.load = self.load.resize((500, 380))
        self.render = ImageTk.PhotoImage(self.load)
        self._frame = None


        photoFrame = tk.Frame(self, height=250, width=600, bg='white')
        photoFrame.pack(side=tk.TOP, expand=True, fill='both')
        widgetsFrame = tk.Frame(self, height=250, width=600, bg='gray')
        widgetsFrame.pack(side=tk.TOP, expand=True, fill='both')
        buttonsFrame = tk.Frame(self, height=40, width=40, bg='gray')
        buttonsFrame.pack(side=tk.TOP, fill='x')

        self.notebook = ttk.Notebook(widgetsFrame)
        self.filterTab = Filters(self.notebook, self.filename)
        self.modificationTab = Modification(self.notebook, self.filename)
        self.adjustingTab = Adjusting(self.notebook, self.filename)
        self.rotationTab = Rotation(self.notebook, self.filename)
        self.notebook.add(self.filterTab, text="Фильтры")
        self.notebook.add(self.modificationTab, text="Модификация")
        self.notebook.add(self.adjustingTab, text="Регулировка")
        self.notebook.add(self.rotationTab, text="Поворот")
        self.notebook.pack(expand=True, fill='both')

        self.image = tk.Label(photoFrame, image=self.render)
        self.image.pack(expand=True, fill='both')

        saveButton = tk.Button(buttonsFrame, text="Сохранить", bd=3)
        resetButton = tk.Button(buttonsFrame, text="Отменить", bd=3)
        resetButton.pack(side=tk.RIGHT, padx=5, pady=5)
        saveButton.pack(side=tk.RIGHT, padx=5, pady=5)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def switch_tab1(self, frame_class):
        new_frame = frame_class(self.notebook)
        self.tab1.destroy()
        self.tab1 = new_frame

    def setNewImage(self, img):
        self.image.configure(image=img)

class Filters(ttk.Frame):
    def __init__(self, master, filename):
        ttk.Frame.__init__(self, master)
        self._frame = None
        self.master = master
        self.filename = filename
        self.photo_for_filters = cv2.imread(filename)
        self.photo_for_filters_resized = cv2.resize(self.photo_for_filters, (160, 90))
        self.sepia = ImageTk.PhotoImage(image=Image.fromarray(filt.sepia(self.photo_for_filters_resized)))
        sepia = tk.Button(self, image=self.sepia, command=self.setSepia)
        sepia.pack(side=tk.LEFT)
        self.black_white = ImageTk.PhotoImage(image=Image.fromarray(filt.black_white(self.photo_for_filters_resized)))
        black_white = tk.Button(self, image=self.black_white, command=self.setBlackWhite)
        black_white.pack(side=tk.LEFT)
        self.negative = ImageTk.PhotoImage(image=Image.fromarray(filt.negative(self.photo_for_filters_resized)))
        negative = tk.Button(self, image=self.negative, command=self.setNegative)
        negative.pack(side=tk.LEFT)

    def setSepia(self):
        self.img = cv2.resize(self.photo_for_filters, (500, 380))
        self.img = Image.fromarray(filt.sepia(self.img))
        self.img = ImageTk.PhotoImage(self.img)
        self.master.master.master.setNewImage(self.img)
        pass

    def setBlackWhite(self):
        pass

    def setNegative(self):
        pass

class Modification(ttk.Frame):
    def __init__(self, master, photo):
        ttk.Frame.__init__(self, master)
        self.photo = photo
        self.label = tk.Label(self, text="this is a test - two")
        self.label.pack()

class Adjusting(ttk.Frame):
    def __init__(self, master, photo):
        ttk.Frame.__init__(self, master)
        self.photo = photo
        self.label = tk.Label(self, text="this is a test - three")
        self.label.pack()

class Rotation(ttk.Frame):
    def __init__(self, master, photo):
        ttk.Frame.__init__(self, master)
        self.photo = photo
        self.label = tk.Label(self, text="this is a test - three")
        self.label.pack()



