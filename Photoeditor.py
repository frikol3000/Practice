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
    def __init__(self, img_widget, filename, master=None):
        tk.Toplevel.__init__(self, master)
        self.img_widget = img_widget
        self.filename = filename
        self.master = master
        self.title('Редактор фото')
        self.resizable(False, False)
        self._frame = None
        self.operations = Operations()


        photoFrame = tk.Frame(self, height=250, width=700, bg='white')
        photoFrame.pack(side=tk.TOP, expand=True, fill='both')
        widgetsFrame = tk.Frame(self, height=250, width=600, bg='gray')
        widgetsFrame.pack(side=tk.TOP, expand=False, fill='both')
        buttonsFrame = tk.Frame(self, height=40, width=40, bg='gray')
        buttonsFrame.pack(side=tk.TOP, fill='x')

        self.original_img = Image.open(filename).convert("RGB")
        self.load = Image.open(filename).convert("RGB")
        self.temp = self.getImg_With_All_Operations()
        self.render = ImageTk.PhotoImage(self.temp)
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

        saveButton = tk.Button(buttonsFrame, text="Сохранить", bd=3, command=self.save)
        resetButton = tk.Button(buttonsFrame, text="Сброс", bd=3, command=self.reset)
        resetButton.pack(side=tk.RIGHT, padx=5, pady=5)
        saveButton.pack(side=tk.RIGHT, padx=5, pady=5)

    def save(self):
        self.getImg_With_All_Operations(resize=False).save("./temp.png")
        load = self.getImg_With_All_Operations(resize=False)
        render = ImageTk.PhotoImage(image=load)
        self.img_widget.configure(image=render)
        self.img_widget.image = render
        pass

    def reset(self):
        self.operations.reset()
        self.adjustingTab.reset_sliders()
        self.load = self.original_img.copy()
        self.setNewImage()

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def setFilter(self):
        self.load = self.original_img.copy()
        filt.setFilter(self.operations.filter, self.load)
        self.setNewImage()

    def getImg_With_All_Operations(self, resize=True):
        b = self.operations.brightness
        c = self.operations.contrast
        s = self.operations.sharpness

        self.img = self.load.copy()
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

        if resize:
            h = THUMB_SIZE
            w = _get_ratio_width(self.img.width, self.img.height, h)
            self.img = self.img.resize((w, h))

        return self.img

    def setNewImage(self):
        img = self.getImg_With_All_Operations()
        self.n_img = ImageTk.PhotoImage(img)
        self.image.configure(image=self.n_img)

class Filters(ttk.Frame):
    def __init__(self, master, filename):
        ttk.Frame.__init__(self, master)
        self._frame = None
        self.master = master
        self.filename = filename
        self.img = Image.open(self.filename).convert("RGB")
        self.img = self.img.resize((200, 110))
        filter_names = {'sepia': None, 'black_white': None, 'negative': None}
        for i in filter_names:
            filter_names[i] = self.img.copy()
            filt.setFilter(i, filter_names[i])
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
        self.master.master.master.setFilter()
        pass

    def setBlackWhite(self):
        self.master.master.master.operations.filter = 'black_white'
        self.master.master.master.setFilter()
        pass

    def setNegative(self):
        self.master.master.master.operations.filter = 'negative'
        self.master.master.master.setFilter()
        pass

class Adjusting(ttk.Frame):
    def __init__(self, master, photo):
        ttk.Frame.__init__(self, master)
        self.photo = photo
        self.label_brightness = tk.Label(self, text="Яркость")
        self.label_brightness.place(x=130, y=18)
        self.slider_brightness = tk.Scale(self, length=400, from_=SLIDER_MIN_VAL, to=SLIDER_MAX_VAL, orient=tk.HORIZONTAL)
        self.slider_brightness.bind("<ButtonRelease-1>", self.on_brightness_slider_released)
        self.slider_brightness.pack(side=tk.TOP)
        self.label_sharpness = tk.Label(self, text="Четкость")
        self.label_sharpness.place(x=130, y=62)
        self.slider_sharpness = tk.Scale(self, length=400, from_=SLIDER_MIN_VAL, to=SLIDER_MAX_VAL, orient=tk.HORIZONTAL)
        self.slider_sharpness.bind("<ButtonRelease-1>", self.on_sharpness_slider_released)
        self.slider_sharpness.pack(side=tk.TOP)
        self.label_contrast = tk.Label(self, text="Контраст")
        self.label_contrast.place(x=130, y=104)
        self.slider_contrast = tk.Scale(self, length=400, from_=SLIDER_MIN_VAL, to=SLIDER_MAX_VAL, orient=tk.HORIZONTAL)
        self.slider_contrast.bind("<ButtonRelease-1>", self.on_contrast_slider_released)
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

    def reset_sliders(self):
        self.slider_contrast.set(0)
        self.slider_sharpness.set(0)
        self.slider_brightness.set(0)

class Rotation(ttk.Frame):
    def __init__(self, master, filename):
        ttk.Frame.__init__(self, master)
        self.rotarion = 0
        self.filename = filename
        self.master = master
        self.load = Image.open(self.filename).convert("RGB")
        self.load = self.load.resize(
            (self.master.master.master.render.width(), self.master.master.master.render.height()))
        forward_rotation = tk.Button(self, text="Против часовой стрелки", font=50, command=self.rotateForward)
        forward_rotation.pack(side=tk.LEFT, padx=10, pady=10)
        backward_rotation = tk.Button(self, text="По часовой стрелки", font=50, command=self.rotateBackward)
        backward_rotation.pack(side=tk.LEFT, padx=10, pady=10)
        upside_down = tk.Button(self, text="↑↓", width=20, font=50, command=self.turnUpsideDown)
        upside_down.pack(side=tk.LEFT, padx=10, pady=10)
        left_to_right = tk.Button(self, text="⇆", width=20, font=50, command=self.turnLeft)
        left_to_right.pack(side=tk.LEFT, padx=10, pady=10)

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




