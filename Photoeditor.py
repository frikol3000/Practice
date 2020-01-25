import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import img_modifier.color_filter as filt
import img_modifier.img_helper as img_transformation

THUMB_SIZE = 500
SLIDER_MIN_VAL = -100
SLIDER_MAX_VAL = 100
SLIDER_DEF_VAL = 0

def _get_ratio_height(width, height, r_width):
    return int(r_width/width*height)


def _get_ratio_width(width, height, r_height):
    return int(r_height/height*width)

def _get_converted_point(user_p1, user_p2, p1, p2, x):
    r = (x - user_p1) / (user_p2 - user_p1)
    return p1 + r * (p2 - p1)

class Operations():
    def __init__(self):
        self.angle = 0
        self.filter = ""
        self.contrast = 0
        self.brightness = 0
        self.sharpness = 0
        self.left_right = False
        self.upside_down = False

    def reset(self):
        self.angle = 0
        self.filter = ""
        self.contrast = 0
        self.brightness = 0
        self.sharpness = 0
        self.left_right = False
        self.upside_down = False

class PhotoEditor(tk.Toplevel):
    def __init__(self, filename, master=None):
        tk.Toplevel.__init__(self, master)
        self.filename = filename
        self.master = master
        self.title('Редактор фото')
        self.resizable(True, False)
        self.geometry('500x700')
        self._frame = None
        self.operations = Operations()


        photoFrame = tk.Frame(self, height=250, width=700, bg='white')
        photoFrame.pack(side=tk.TOP, expand=True, fill='both')
        widgetsFrame = tk.Frame(self, height=250, width=600, bg='gray')
        widgetsFrame.pack(side=tk.TOP, expand=False, fill='both')
        buttonsFrame = tk.Frame(self, height=40, width=40, bg='gray')
        buttonsFrame.pack(side=tk.TOP, fill='x')

        self.load = Image.open(filename).convert("RGB")
        self.render = ImageTk.PhotoImage(self.load)
        self.image = tk.Label(photoFrame, image=self.render)
        self.image.pack(expand=True, fill='both')

        self.notebook = ttk.Notebook(widgetsFrame)
        self.filterTab = Filters(self.notebook, self.filename)
        self.adjustingTab = Adjusting(self.notebook, self.filename)
        self.rotationTab = Rotation(self.notebook, self.filename)
        self.notebook.add(self.filterTab, text="Фильтры")
        self.notebook.add(self.adjustingTab, text="Регулировка")
        self.notebook.add(self.rotationTab, text="Поворот")
        self.notebook.pack(expand=False, fill='both')

        saveButton = tk.Button(buttonsFrame, text="Сохранить", bd=3)
        resetButton = tk.Button(buttonsFrame, text="Отменить", bd=3, command=self.reset)
        resetButton.pack(side=tk.RIGHT, padx=5, pady=5)
        saveButton.pack(side=tk.RIGHT, padx=5, pady=5)

    def reset(self):
        self.operations.reset()
        self.setNewImage()

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

    def setNewImage(self):
        b = self.operations.brightness
        c = self.operations.contrast
        s = self.operations.sharpness

        self.img = self.load.copy()
        filt.setFilter(self.operations.filter, self.img)
        self.img = img_transformation.rotate(self.img, self.operations.angle)
        if self.operations.left_right:
            self.img = img_transformation.flip_left(self.img)
        if self.operations.upside_down:
            self.img = img_transformation.flip_top(self.img)


        if b != 0:
            self.img = img_transformation.brightness(self.img, b)

        if c != 0:
            self.img = img_transformation.contrast(self.img, c)

        if s != 0:
            self.img = img_transformation.sharpness(self.img, s)

        h = THUMB_SIZE
        w = _get_ratio_width(self.img.width, self.img.height, h)
        self.img = self.img.resize((w, h))
        self.n_img = ImageTk.PhotoImage(self.img)
        self.image.configure(image=self.n_img)

class Filters(ttk.Frame):
    def __init__(self, master, filename):
        ttk.Frame.__init__(self, master)
        self._frame = None
        self.master = master
        self.filename = filename
        self.img = Image.open(self.filename).convert("RGB")
        filter_names = {'sepia': None, 'black_white': None, 'negative': None}
        for i in filter_names:
            filter_names[i] = self.img.copy()
            filt.setFilter(i, filter_names[i])
            filter_names[i] = filter_names[i].resize((160, 90))
        self.sepia = ImageTk.PhotoImage(filter_names['sepia'])
        self.black_white = ImageTk.PhotoImage(filter_names['black_white'])
        self.negative = ImageTk.PhotoImage(filter_names['negative'])
        sepia = tk.Button(self, image=self.sepia, command=self.setSepia)
        sepia.pack(side=tk.LEFT)
        black_white = tk.Button(self, image=self.black_white, command=self.setBlackWhite)
        black_white.pack(side=tk.LEFT)
        negative = tk.Button(self, image=self.negative, command=self.setNegative)
        negative.pack(side=tk.LEFT)

    def setSepia(self):
        self.master.master.master.operations.filter = 'sepia'
        self.master.master.master.setNewImage()
        pass

    def setBlackWhite(self):
        self.master.master.master.operations.filter = 'black_white'
        self.master.master.master.setNewImage()
        pass

    def setNegative(self):
        self.master.master.master.operations.filter = 'negative'
        self.master.master.master.setNewImage()
        pass

class Adjusting(ttk.Frame):
    def __init__(self, master, photo):
        ttk.Frame.__init__(self, master)
        self.photo = photo
        self.slider_brightness = tk.Scale(self, from_=SLIDER_MIN_VAL, to=SLIDER_MAX_VAL, orient=tk.HORIZONTAL, command=self.on_brightness_slider_released)
        self.slider_brightness.pack(side=tk.TOP)
        self.slider_sharpness = tk.Scale(self, from_=SLIDER_MIN_VAL, to=SLIDER_MAX_VAL, orient=tk.HORIZONTAL, command=self.on_sharpness_slider_released)
        self.slider_sharpness.pack(side=tk.TOP)
        self.slider_contrast = tk.Scale(self, from_=SLIDER_MIN_VAL, to=SLIDER_MAX_VAL, orient=tk.HORIZONTAL, command=self.on_contrast_slider_released)
        self.slider_contrast.pack(side=tk.TOP)



    def on_brightness_slider_released(self, e):
        factor = _get_converted_point(SLIDER_MIN_VAL, SLIDER_MAX_VAL, img_transformation.BRIGHTNESS_FACTOR_MIN,
                                      img_transformation.BRIGHTNESS_FACTOR_MAX, self.slider_brightness.get())

        self.master.master.master.operations.brightness = factor

        self.master.master.master.setNewImage()

    def on_sharpness_slider_released(self, e):
        factor = _get_converted_point(SLIDER_MIN_VAL, SLIDER_MAX_VAL, img_transformation.SHARPNESS_FACTOR_MIN,
                                      img_transformation.SHARPNESS_FACTOR_MAX, self.slider_sharpness.get())

        self.master.master.master.operations.sharpness = factor

        self.master.master.master.setNewImage()

    def on_contrast_slider_released(self, e):
        factor = _get_converted_point(SLIDER_MIN_VAL, SLIDER_MAX_VAL, img_transformation.CONTRAST_FACTOR_MIN,
                                      img_transformation.CONTRAST_FACTOR_MAX, self.slider_contrast.get())

        self.master.master.master.operations.contrast = factor

        self.master.master.master.setNewImage()

class Rotation(ttk.Frame):
    def __init__(self, master, filename):
        ttk.Frame.__init__(self, master)
        self.rotarion = 0
        self.filename = filename
        self.master = master
        self.load = Image.open(self.filename).convert("RGB")
        self.load = self.load.resize(
            (self.master.master.master.render.width(), self.master.master.master.render.height()))
        forward_rotation = tk.Button(self, text="Против часовой стрелки", command=self.rotateForward)
        forward_rotation.pack(side=tk.LEFT)
        backward_rotation = tk.Button(self, text="По часовой стрелки", command=self.rotateBackward)
        backward_rotation.pack(side=tk.LEFT)
        upside_down = tk.Button(self, text="↑↓", command=self.turnUpsideDown)
        upside_down.pack(side=tk.LEFT)
        left_to_right = tk.Button(self, text="⇆", command=self.turnLeft)
        left_to_right.pack(side=tk.LEFT)

    def rotateForward(self):
        self.master.master.master.operations.angle += 90
        self.master.master.master.setNewImage()
        pass

    def rotateBackward(self):
        self.master.master.master.operations.angle += 270
        self.master.master.master.setNewImage()
        pass

    def turnUpsideDown(self):
        self.master.master.master.operations.upside_down = not self.master.master.master.operations.upside_down
        self.master.master.master.setNewImage()
        pass

    def turnLeft(self):
        self.master.master.master.operations.left_right = not self.master.master.master.operations.left_right
        self.master.master.master.setNewImage()
        pass




