import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, Scale, HORIZONTAL
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageEnhance
from PIL import ImageFilter, ImageOps
from PIL.ImageFilter import (
    ModeFilter)
import sys


class MenuBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        menubar = tk.Menu(parent, background='#ff8000', foreground='black', activebackground='white',
                          activeforeground='black')

        parent.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label='Open Image',
            command=parent.imageframe.open_image,
        )
        file_menu.add_command(
            label='Save Image',
            command=parent.imageframe.save_image
        )
        file_menu.add_separator()
        file_menu.add_command(
            label='Exit',
            command=parent.destroy,
        )

        edit_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(
            label='Undo',
            command=self.parent.imageframe.undo
        )
        edit_menu.add_command(
            label='Redo',
            command=self.parent.imageframe.redo
        )


class ImageEffectsBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.__create_widgets()

    def __create_widgets(self):
        self.button = ttk.Button(self, text="Paint Effect", command=self.parent.imageframe.paint_effect)
        self.button.pack(side="left")

        self.button = ttk.Button(self, text="Invert Effect", command=self.parent.imageframe.invert_effect)
        self.button.pack(side="left")

        self.button = ttk.Button(self, text="Solarize Effect", command=self.parent.imageframe.solarize_effect)
        self.button.pack(side="left")

        self.button = ttk.Button(self, text='Filter Color', command=self.change_color)
        self.button.pack(side="left", expand=True)

        self.slider_label = ttk.Label(self, text='Brightness: ')
        self.slider_label.pack(side="left", expand=True)

        self.slider = ttk.Scale(self, from_=0, to=2, orient=HORIZONTAL, value=1)
        self.slider.bind("<ButtonRelease-1>", self.change_brightness)
        self.slider.pack(side="left", expand=True)

    def change_color(self):
        colors = askcolor(title="Color Chooser")
        self.parent.imageframe.color_effect(colors[0])

    def change_brightness(self, new_value):
        new_value = self.slider.get()
        self.parent.imageframe.brightness_effect(new_value)


class ImageFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.image_label = ttk.Label(self)
        self.image_label.pack()
        self.show_resolution = (600, 450)
        self.stack = []
        self.stack_ix = -1

    def set_image(self, filepath):
        self.image_label.pack_forget()
        PIL_image = Image.open(filepath)
        tk_image = tk.PhotoImage(filepath)
        # self.opencv_img = cv2.imread(filepath)     #not working
        # self.opencv_img = cv2.cvtColor(self.opencv_img, cv2.COLOR_BGR2RGB)
        img = Image.open(filepath)
        self.img = img.convert('RGB')

        self._add_to_stack(self.img)

        img = img.resize(self.show_resolution)

        photo = ImageTk.PhotoImage(img)

        self.image_label = ttk.Label(self, image=photo)
        self.image_label.image = photo  # this is necessary
        self.enhancer = ImageEnhance.Brightness(self.img)

        self.image_label.pack()

    def save_image(self):
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if not filename:
            return
        self.img.save(filename)

    def open_image(self):
        self.filepath = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                                   filetypes=(("PNG files", "*.png"), ("JPG files", "*.jpg"),
                                                              ("all files", "*.*")))
        if self.filepath:
            self.parent.imageframe.set_image(filepath=self.filepath)

    def change_img(self, res, is_brightness=False, add_to_stack=True):
        self.image_label.pack_forget()
        self.img = res

        res = res.resize(self.show_resolution)
        photo1 = ImageTk.PhotoImage(res)
        self.image_label = ttk.Label(self, image=photo1)
        self.image_label.image = photo1

        if add_to_stack:
            self._add_to_stack(self.img)

        if not is_brightness:
            self.enhancer = ImageEnhance.Brightness(self.img)

        self.img_without_effects = res  # no usage
        self.image_label.pack()

    def paint_effect(self):
        # self.opencv_img = cv2.xphoto.oilPainting(self.opencv_img, 7, 1)
        res = self.img.filter(ModeFilter(size=7))
        self.change_img(res)

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
        res = self.enhancer.enhance(new_value)
        self.change_img(res, is_brightness=True)

    def undo(self):
        if self.stack:
            self.stack_ix = max(0, self.stack_ix - 1)
            self.change_img(self.stack[self.stack_ix], add_to_stack=False)

    def redo(self):
        if self.stack:
            self.stack_ix = min(len(self.stack) - 1, self.stack_ix + 1)
            self.change_img(self.stack[self.stack_ix], add_to_stack=False)

    def _add_to_stack(self, img):
        if self.stack_ix < len(self.stack) - 1:
            self.stack = self.stack[0:self.stack_ix + 1]

        self.stack.append(img)
        self.stack_ix += 1


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

        self.imageframe = ImageFrame(self)
        self.menubar = MenuBar(self)
        self.effectsbar = ImageEffectsBar(self)

        self.imageframe.pack(side="bottom", fill="x", expand=True)
        self.menubar.pack(side="top", fill="x")
        self.effectsbar.pack(side="left", fill="x")

        self._bindings()
        self.__debugging()

    def _bindings(self):
        if sys.platform == "darwin":  # mac os
            self.bind('<Command-z>', lambda event: self.imageframe.undo())
            self.bind('<Command-Shift-Z>', lambda event: self.imageframe.redo())
            self.bind('<Command-o>', lambda event: self.imageframe.open_image())
            self.bind('<Command-s>', lambda event: self.imageframe.save_image())
        else:
            self.bind('<Control-z>', lambda event: self.imageframe.undo())
            self.bind('<Control-Shift-Z>', lambda event: self.imageframe.redo())
            self.bind('<Control-o>', lambda event: self.imageframe.open_image())
            self.bind('<Control-s>', lambda event: self.imageframe.save_image())

    def __debugging(self):
        self.imageframe.set_image(filepath='/Users/damiantworek/Desktop/pic.png')


if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
