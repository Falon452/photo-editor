import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, Scale, HORIZONTAL
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageEnhance
from PIL import ImageFilter, ImageOps
from PIL.ImageFilter import (
    ModeFilter)
import cv2
import sys
import numpy as np


# pip install opencv-contrib-python

class MenuBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.menubar = tk.Menu(parent, background='#ff8000', foreground='black', activebackground='white',
                               activeforeground='black')

        self.parent.config(menu=self.menubar)

        file_menu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label='Open Image',
            command=self.parent.img_UI.open_image,
        )
        file_menu.add_command(
            label='Save Image',
            command=self.parent.img_UI.save_image
        )
        file_menu.add_separator()
        file_menu.add_command(
            label='Exit',
            command=self.parent.destroy,
        )

        edit_menu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(
            label='Undo',
            command=self.parent.img_UI.undo
        )
        edit_menu.add_command(
            label='Redo',
            command=self.parent.img_UI.redo
        )


class ImageEffectsBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.__create_widgets()

    def __create_widgets(self):
        self.button = ttk.Button(self, text="Paint Effect", command=self.parent.img_UI.paint_effect)
        self.button.pack(side="left")

        self.button = ttk.Button(self, text="Invert Effect", command=self.parent.img_UI.invert_effect)
        self.button.pack(side="left")

        self.button = ttk.Button(self, text="Solarize Effect", command=self.parent.img_UI.solarize_effect)
        self.button.pack(side="left")

        self.button = ttk.Button(self, text='Filter Color', command=self.parent.img_UI.change_color)
        self.button.pack(side="left", expand=True)

        self.slider_label = ttk.Label(self, text='Brightness: ')
        self.slider_label.pack(side="left", expand=True)

        self.slider = ttk.Scale(self, from_=0, to=2, orient=HORIZONTAL, value=1)
        self.slider.bind("<ButtonRelease-1>", self.parent.img_UI.brightness_effect)
        self.slider.pack(side="left", expand=True)


class ImgUI:
    def __init__(self, parent):
        self.parent = parent
        self.img = None
        self.__enhancer = None
        self.__stack = []
        self.__stack_ix = -1

    def set_image(self, filepath):
        self.img = cv2.imread(filepath)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img = Image.fromarray(self.img)
        self.__add_to_stack()
        self.__update_enhancer()
        self.parent.image_frame.show_img(self.img)

    def save_image(self):
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if not filename:
            return
        self.img.save(filename)

    def open_image(self):
        filepath = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                              filetypes=(("PNG files", "*.png"), ("JPG files", "*.jpg"),
                                                         ("all files", "*.*")))
        if filepath:
            self.set_image(filepath)

    def change_img(self, res, brightness_effect=False, add_to_stack=True):
        self.img = res
        if not brightness_effect:
            self.__update_enhancer()
        if add_to_stack:
            self.__add_to_stack()
        self.parent.image_frame.show_img(self.img)

    def paint_effect(self):
        res = cv2.xphoto.oilPainting(np.asarray(self.img), 7, 1)
        res = Image.fromarray(res)
        self.change_img(res)

        # res = self.img.filter(ModeFilter(size=7))
        # self.change_img(res)

    def invert_effect(self):
        res = ImageOps.invert(self.img)
        self.change_img(res)

    def solarize_effect(self):
        res = ImageOps.solarize(self.img, threshold=50)
        self.change_img(res)

    def color_effect(self, color):
        effect_image = self.img.convert('L')
        res = ImageOps.colorize(effect_image, black=color, white="white")
        self.change_img(res)

    def brightness_effect(self, new_value):
        new_value = self.parent.effects_bar.slider.get()
        res = self.__enhancer.enhance(new_value)
        self.change_img(res, brightness_effect=True)

    def undo(self):
        if self.__stack:
            self.__stack_ix = max(0, self.__stack_ix - 1)
            self.parent.image_frame.change_img(self.__stack[self.__stack_ix], add_to_stack=False)

    def redo(self):
        if self.__stack:
            self.__stack_ix = min(len(self.__stack) - 1, self.__stack_ix + 1)
            self.parent.image_frame.change_img(self.__stack[self.__stack_ix], add_to_stack=False)

    def change_color(self):
        colors = askcolor(title="Color Chooser")
        self.color_effect(colors[0])

    def __update_enhancer(self):
        self.parent.effects_bar.slider.get()
        self.__enhancer = ImageEnhance.Brightness(self.img)

    def __add_to_stack(self):
        if self.__stack_ix < len(self.__stack) - 1:
            self.__stack = self.__stack[0:self.__stack_ix + 1]

        self.__stack.append(self.img)
        self.__stack_ix += 1


class ImageFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.image_label = ttk.Label(self)
        self.image_label.pack()
        self.show_resolution = (600, 450)

    def show_img(self, res):
        self.image_label.pack_forget()
        res = res.resize(self.show_resolution)
        res = ImageTk.PhotoImage(res)
        self.image_label = ttk.Label(self, image=res)
        self.image_label.image = res
        self.image_label.pack()


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Photo Editor")

        window_width = 800
        window_height = 600

        self.minsize(window_width, window_height)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')  # open in middle of scren

        self.img_UI = ImgUI(self)
        self.image_frame = ImageFrame(self)
        self.effects_bar = ImageEffectsBar(self)
        self.menu_bar = MenuBar(self)

        self.image_frame.pack(side="bottom", fill="x", expand=True)
        self.menu_bar.pack(side="top", fill="x")
        self.effects_bar.pack(side="left", fill="x")

        self._bindings()
        self.__debugging()

    def _bindings(self):
        if sys.platform == "darwin":  # mac os
            self.bind('<Command-z>', lambda event: self.img_UI.undo())
            self.bind('<Command-Shift-Z>', lambda event: self.img_UI.redo())
            self.bind('<Command-o>', lambda event: self.img_UI.open_image())
            self.bind('<Command-s>', lambda event: self.img_UI.save_image())
        else:
            self.bind('<Control-z>', lambda event: self.img_UI.undo())
            self.bind('<Control-Shift-Z>', lambda event: self.img_UI.redo())
            self.bind('<Control-o>', lambda event: self.img_UI.open_image())
            self.bind('<Control-s>', lambda event: self.img_UI.save_image())

    def __debugging(self):
        self.img_UI.set_image(filepath='/Users/damiantworek/Desktop/pic.png')


if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
