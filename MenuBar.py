from locale import currency
from tkinter import EW, NE, NSEW, RIDGE, SE, ttk, ALL
from tkinter import filedialog, Scale, HORIZONTAL
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageEnhance
from PIL import ImageFilter, ImageOps
from PIL.ImageFilter import (
    ModeFilter)
from imutils.object_detection import non_max_suppression

import tkinter as tk
import cv2
import sys
import numpy as np



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
