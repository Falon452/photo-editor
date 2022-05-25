from locale import currency
from tkinter import EW, NE, NSEW, RIDGE, SE, ttk, ALL
from tkinter import filedialog, Scale, HORIZONTAL
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageEnhance
from PIL import ImageFilter, ImageOps
from PIL.ImageFilter import (
    ModeFilter)
from imutils.object_detection import non_max_suppression
from imutils import resize as imutils_resize


import tkinter as tk
import cv2
import sys
import numpy as np


class ImageFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.image_label = ttk.Label(self)
        self.image_label.pack()
        self.show_resolution = (600, 450)
        self.canvas = tk.Canvas(self, bg="gray", width=self.show_resolution[0], height=self.show_resolution[1])

    def show_img(self, res):
        self.canvas.delete("all")
        if self.parent.img_UI.new_value == 1:
            res = res.resize(self.show_resolution)
        self.shown_image = ImageTk.PhotoImage(res)
        # self.zoom_img = self.shown_image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.shown_image)
        self.zoom_bind()

        self.canvas.pack()

    def start_cropping(self):
        self.parent.img_UI.do_capture = False

        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<ButtonPress>", self.parent.img_UI.start_crop)
        self.canvas.bind("<B1-Motion>", self.parent.img_UI.crop)
        self.canvas.bind("<ButtonRelease-1>", self.parent.img_UI.end_crop)

    def stop_cropping(self):
        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def zoom_bind(self):
        self.canvas.bind('<Control-ButtonPress-1>', self.parent.img_UI.scan_img)
        self.canvas.bind("<Control-B1-Motion>", self.parent.img_UI.move_img)

    def draw_bind(self):
        self.canvas.bind("<Motion>", self.parent.img_UI.drawing_effect)
        self.canvas.bind('<ButtonPress-1>', lambda event: self.parent.img_UI.capture(True))
        self.canvas.bind("<ButtonRelease-1>", lambda event: self.parent.img_UI.capture(False))

    def add_text_bind(self):
        self.canvas.bind('<ButtonPress-1>', self.parent.img_UI.add_text)