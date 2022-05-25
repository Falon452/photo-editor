from locale import currency
from tkinter import END, EW, NE, NSEW, RIDGE, SE, ttk, ALL
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


class ImageEffectsBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.button_width = 15
        self.__create_widgets()

    def add_labels(self):
        self.filter_label = ttk.Label(self, text="Filters: ", borderwidth=2, relief="groove")
        self.filter_label.grid(row=0, column=0, columnspan=2, sticky=EW)

        self.filter_label = ttk.Label(self, text="Image convert: ", borderwidth=2, relief="groove")
        self.filter_label.grid(row=0, column=2, columnspan=3, sticky=EW)

        self.filter_label = ttk.Label(self, text="Drawing: ", borderwidth=2, relief="groove")
        self.filter_label.grid(row=0, column=5, columnspan=4, sticky=EW)

        self.filter_label = ttk.Label(self, text="Object recognize: ", borderwidth=2, relief="groove")
        self.filter_label.grid(row=0, column=9, columnspan=3, sticky=EW)

    def add_filter_buttons(self):
        self.button = ttk.Button(self, text="Paint Effect", command=self.parent.img_UI.paint_effect,
                                 width=self.button_width)
        self.button.grid(row=1, column=0)

        self.button = ttk.Button(self, text="Invert Effect", command=self.parent.img_UI.invert_effect,
                                 width=self.button_width)
        self.button.grid(row=1, column=1)

        self.button = ttk.Button(self, text="Solarize Effect", command=self.parent.img_UI.solarize_effect,
                                 width=self.button_width)
        self.button.grid(row=3, column=0)

        self.button = ttk.Button(self, text='Filter Color', command=self.parent.img_UI.change_color,
                                 width=self.button_width)
        self.button.grid(row=3, column=1)

    def add_convert_buttons(self):
        self.button = ttk.Button(self, text="Rotate Left", command=self.parent.img_UI.rotate_left,
                                 width=self.button_width)
        self.button.grid(row=1, column=2)

        self.button = ttk.Button(self, text="Rotate Right", command=self.parent.img_UI.rotate_right,
                                 width=self.button_width)
        self.button.grid(row=1, column=3)

        self.button = ttk.Button(self, text="Flip Horizontally", command=self.parent.img_UI.flip_horizontally,
                                 width=self.button_width)
        self.button.grid(row=3, column=2)

        self.button = ttk.Button(self, text="Flip Vertically", command=self.parent.img_UI.flip_vertically,
                                 width=self.button_width)
        self.button.grid(row=3, column=3)

        self.button = ttk.Button(self, text="Resolution", command=self.open_window, width=self.button_width)
        self.button.grid(row=1, column=4)

        self.button = ttk.Button(self, text="Crop", command=self.parent.image_frame.start_cropping,
                                 width=self.button_width)
        self.button.grid(row=3, column=4)

    def add_object_detection_buttons(self):
        start_column = 9
        self.button = ttk.Button(self, text='Face', command=self.parent.img_UI.detect_face, width=self.button_width)
        self.button.grid(row=1, column=start_column)

        self.button = ttk.Button(self, text='Full body', command=self.parent.img_UI.detect_fullbody,
                                 width=self.button_width)
        self.button.grid(row=1, column=start_column + 1)

        self.button = ttk.Button(self, text='smile', command=self.parent.img_UI.detect_smile, width=self.button_width)
        self.button.grid(row=1, column=start_column + 2)
        self.button = ttk.Button(self, text='cars', command=self.parent.img_UI.detect_cars, width=self.button_width)
        self.button.grid(row=3, column=start_column)
        self.button = ttk.Button(self, text='edges', command=self.parent.img_UI.detect_edges, width=self.button_width)
        self.button.grid(row=3, column=start_column + 1)

        self.button = ttk.Button(self, text='Pattern match', command=self.parent.img_UI.pattern_match,
                                 width=self.button_width)
        self.button.grid(row=3, column=start_column + 2)

    def add_computional_photograpy(self):
        self.button = ttk.Button(self, text='Denoise', command=self.parent.img_UI.denoise, width=self.button_width)
        self.button.grid(row=1, column=13)

        self.button = ttk.Button(self, text='Inpaint', command=self.parent.img_UI.inpaint,
                                 width=self.button_width)
        self.button.grid(row=1, column=14)

        self.button = ttk.Button(self, text='HDR', command=self.parent.img_UI.hdr, width=self.button_width)
        self.button.grid(row=3, column=13)

    def __create_widgets(self):
        self.add_labels()
        self.add_filter_buttons()
        self.add_convert_buttons()
        self.add_object_detection_buttons()
        self.add_computional_photograpy()

        # Sliders

        self.slider_label = ttk.Label(self, text='Brightness: ')
        self.slider_label.grid(row=0, column=12, sticky=NE, rowspan=2)

        self.slider = ttk.Scale(self, from_=0, to=2, orient=HORIZONTAL, value=1)
        self.slider.bind("<ButtonRelease-1>", self.parent.img_UI.brightness_effect)
        self.slider.grid(row=0, column=13, sticky=NE, rowspan=2)

        self.slider_label = ttk.Label(self, text='Zoom: ')
        self.slider_label.grid(row=2, column=12, sticky=SE, rowspan=2)
        self.slider_zoom = ttk.Scale(self, from_=1, to=5, orient=HORIZONTAL, value=1)
        self.slider_zoom.bind("<ButtonRelease-1>", self.parent.img_UI.do_zoom)
        self.slider_zoom.grid(row=2, column=13, sticky=SE, rowspan=2)

        # Draw effects fields

        self.button = ttk.Button(self, text='Color', command=self.parent.img_UI.draw, width=self.button_width // 2)
        self.button.grid(row=1, column=5)

        self.shape_label = ttk.Label(self, text="Shape: ", width=self.button_width // 2)
        self.shape_label.grid(row=1, column=6)
        self.selected_shape = tk.StringVar()
        self.draw_option = ttk.Combobox(self, textvariable=self.selected_shape, width=self.button_width // 2,
                                        state="readonly")
        self.draw_option['values'] = ['circle', 'rectangle', 'triangle']
        self.draw_option.current(0)

        self.draw_option.grid(row=1, column=7)

        self.shape_label = ttk.Label(self, text="Effect: ", width=self.button_width // 2)
        self.shape_label.grid(row=3, column=6)

        self.selected_effect_option = tk.StringVar()

        self.selected_draw_effect = tk.StringVar()
        self.effect_option = ttk.Combobox(self, textvariable=self.selected_effect_option, width=self.button_width // 2,
                                          state="readonly")
        self.effect_option['values'] = ['filled', 'very light border', 'light border', 'medium border', "solid border"]
        self.effect_option.current(0)

        self.effect_option.grid(row=3, column=7)

        def shape_changed(event):
            self.parent.img_UI.do_capture = False

        self.draw_option.bind('<<ComboboxSelected>>', shape_changed)

        self.selected_paint_size = tk.StringVar()

        self.draw_size = ttk.Combobox(self, textvariable=self.selected_paint_size, width=4, state="readonly")
        self.draw_size['values'] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.draw_size.current(5)
        self.draw_size.grid(row=3, column=5)

        def paint_size_changed(event):
            self.parent.img_UI.do_capture = False

        self.draw_size.bind('<<ComboboxSelected>>', paint_size_changed)

        ##TEST TEXT
        self.button = ttk.Button(self, text='Text add', command=self.parent.img_UI.text_effect, width=self.button_width)
        self.button.grid(row=3, column=8)

        self.text_input = tk.Entry(self, width=self.button_width)  # ,justify="right"
        self.text_input.insert(END, 'add text')
        self.text_input.grid(row=1, column=8)

    def open_window(self):
        new_window = tk.Toplevel(self.parent)
        new_window.geometry("300x150")
        new_window.resizable(False, False)

        self.width_label = ttk.Label(new_window, text="Width:")
        self.width_label.pack(fill='x')

        self.width_entry = ttk.Entry(new_window)
        self.width_entry.pack(fill='x')
        self.width_entry.focus()

        self.height_label = ttk.Label(new_window, text="Height:")
        self.height_label.pack(fill='x')

        self.height_entry = ttk.Entry(new_window)
        self.height_entry.pack(fill='x')

        self.button = ttk.Button(new_window, text="save", command=self.parent.img_UI.change_resolution)
        self.button.pack(fill='x')
