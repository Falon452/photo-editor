
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

class ImgUI:
    def __init__(self, parent):
        self.parent = parent
        self.img = None
        self.__enhancer = None
        self.__stack = []
        self.__stack_ix = -1
        self.do_capture = False  # ADDED
        self.scale = 1.0  # ADDED
        self.width_shift_start = 0
        self.width_shift_end = 0
        self.height_shift_start = 0
        self.height_shift_end = 0
        self.new_value = 1


    def set_image(self, filepath):
        self.img = cv2.imread(filepath)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img = Image.fromarray(self.img)
        self.__add_to_stack()
        self.__update_enhancer()
        self.img = self.img.resize(self.parent.image_frame.show_resolution)
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
            self.parent.image_frame.show_img(self.__stack[self.__stack_ix])
            self.img = self.__stack[self.__stack_ix]

    def redo(self):
        if self.__stack:
            self.__stack_ix = min(len(self.__stack) - 1, self.__stack_ix + 1)
            self.parent.image_frame.show_img(self.__stack[self.__stack_ix])
            self.img = self.__stack[self.__stack_ix]

    def change_color(self):
        colors = askcolor(title="Color Chooser")
        self.color_effect(colors[0])

    def rotate_right(self):
        res = cv2.rotate(np.array(self.img), cv2.ROTATE_90_CLOCKWISE)
        res = Image.fromarray(res)
        self.change_img(res)

    def rotate_left(self):
        res = cv2.rotate(np.array(self.img), cv2.ROTATE_90_COUNTERCLOCKWISE)
        res = Image.fromarray(res)
        self.change_img(res)

    def flip_horizontally(self):
        res = cv2.flip(np.array(self.img), 1)
        res = Image.fromarray(res)
        self.change_img(res)

    def flip_vertically(self):
        res = cv2.flip(np.array(self.img), 0)
        res = Image.fromarray(res)
        self.change_img(res)

    def change_resolution(self):
        height = int(self.parent.effects_bar.height_entry.get())
        width = int(self.parent.effects_bar.width_entry.get())
        resized_image = cv2.resize(np.array(self.img), (height, width))
        res = Image.fromarray(resized_image)
        self.change_img(res)

    def start_crop(self, event):

        self.crop_start_x = event.x
        self.crop_start_y = event.y
        self.rectangle_id = None

    def crop(self, event):
        if self.rectangle_id:
            self.parent.image_frame.canvas.delete(self.rectangle_id)

        self.crop_end_x = event.x
        self.crop_end_y = event.y

        self.rectangle_id = self.parent.image_frame.canvas.create_rectangle(
            self.crop_start_x, self.crop_start_y, self.crop_end_x, self.crop_end_y, width=1)

    def end_crop(self, event):

        if self.crop_start_x <= self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = self.crop_start_x
            start_y = self.crop_start_y
            end_x = self.crop_end_x
            end_y = self.crop_end_y
        elif self.crop_start_x > self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = self.crop_end_x
            start_y = self.crop_start_y
            end_x = self.crop_start_x
            end_y = self.crop_end_y
        elif self.crop_start_x <= self.crop_end_x and self.crop_start_y > self.crop_end_y:
            start_x = self.crop_start_x
            start_y = self.crop_end_y
            end_x = self.crop_end_x
            end_y = self.crop_start_y
        else:
            start_x = self.crop_end_x
            start_y = self.crop_end_y
            end_x = self.crop_start_x
            end_y = self.crop_start_y

        start_x, start_y, end_x, end_y = list(map(int, (start_x, start_y, end_x, end_y)))

        original_width, original_height = self.img.size

        show_width, show_height = self.parent.image_frame.show_resolution

        ratio_x = original_width / show_width
        start_x = int(start_x * ratio_x)
        end_x = int(end_x * ratio_x)

        ratio_y = original_height / show_height
        start_y = int(start_y * ratio_y)
        end_y = int(end_y * ratio_y)

        res = np.array(self.img)[start_y: end_y, start_x: end_x]
        res = Image.fromarray(res)
        self.change_img(res)

        self.parent.image_frame.stop_cropping()

    # ADD
    def capture(self, flag):
        self.do_capture = flag

    def draw(self):
        colors = askcolor(title="Color Chooser")
        global draw_color
        draw_color = colors[0]
        self.parent.image_frame.draw_bind()

   


    def drawing_effect(self, event):
        if self.do_capture:
            # tutaj chcielibyśmy mieć wycinek co jest na wyświetlany
            effect_map = [-1 , 1,2, 3,6]

            width_shift = self.width_shift_end - self.width_shift_start
            height_shift = self.height_shift_end - self.height_shift_start
            zoomed = np.asarray(self.img)[height_shift: 450 + height_shift][width_shift:600 + width_shift]

            # zoomed = np.asarray(self.img)[int(height_shift / self.new_value): int((450 + height_shift) / self.new_value)][int(width_shift / self.new_value):int((600 + width_shift) / self.new_value)]

            print(height_shift, 450 + height_shift, width_shift, 600 + width_shift)
            toggle = self.parent.effects_bar.draw_option.current()
            paint_size = 2 * self.parent.effects_bar.draw_size.current()
            effect_idx =self.parent.effects_bar.effect_option.current()
            width, height = self.parent.image_frame.show_resolution

            if paint_size < 0:
                paint_size = 4  # default value
      
            if toggle == 0:  # print circles
                cv2.circle(zoomed, (int(event.x) , int(event.y)),
                        #    (int(event.x * (zoomed.shape[1] / width)), int(event.y * (zoomed.shape[0] / height))),
                           int(paint_size * (zoomed.shape[0] / height)), draw_color, effect_map[effect_idx])
            elif toggle == 1:
                    cv2.rectangle(zoomed, (int(event.x ), int(event.y )), (
                    int(event.x * (zoomed.shape[1] / width)) + int(paint_size * 2 * (zoomed.shape[0] / height)),
                    int(event.y * (zoomed.shape[0] / height)) + int(paint_size * 2 * (zoomed.shape[0] / height))), draw_color,  effect_map[effect_idx])



                # cv2.rectangle(zoomed, (int(event.x) , int(event.y)),(int(event.x * (zoomed.shape[1] / width)), int(event.y * (zoomed.shape[0] / height))),  int(paint_size * (zoomed.shape[0] / height)), draw_color, effect_map[effect_idx])
                      #(int(event.x * (zoomed.shape[1] / width)), int(event.y * (zoomed.shape[0] / height))), (
            elif toggle == 2:

                new_x = int(event.x) #, int(event.x * (zoomed.shape[1] / width))
                new_y =  int(event.y) 
                painting_size = int(paint_size ) *2
                pts = np.array([[new_x , new_y +  painting_size* 0.66], [new_x - painting_size*0.5, new_y- painting_size* 0.33],
                 [new_x + painting_size*0.5, new_y -painting_size* 0.33]] , np.int32)

               
                if effect_idx==0:
                    cv2.fillPoly(zoomed,[pts],draw_color )
                else:
                    pts = pts.reshape((-1,1,2))
                    cv2.polylines(zoomed,[pts],True,draw_color , 	thickness=effect_map[effect_idx])
            res = np.asarray(self.img)
            res[height_shift: 450 + height_shift][width_shift:600 + width_shift] = zoomed
            res = Image.fromarray(res)
            self.width_shift_start = 0
            self.height_shift_start = 0

            self.change_img(res)

    def do_zoom(self, new_value):
        self.new_value = self.parent.effects_bar.slider_zoom.get()
        size = self.parent.image_frame.show_resolution
        resize_image = self.img.resize((int(size[0] * self.new_value), int(size[1] * self.new_value)))
        print(resize_image.size)
        self.img = resize_image

        if self.new_value == 1:  # not working - set in the middle of frame
            self.parent.image_frame.canvas.scan_dragto(0, 0, gain=1)
            self.change_img(self.img)
            return
        self.change_img(self.img)

        self.parent.image_frame.canvas.delete("all")
        self.parent.image_frame.shown_image = ImageTk.PhotoImage(resize_image)
        self.parent.image_frame.canvas.create_image(0, 0, anchor=tk.NW, image=self.parent.image_frame.shown_image)
        self.parent.image_frame.canvas.pack()

    def move_img(self, event):
        if not self.width_shift_start:
            self.width_shift_start = event.x
            self.height_shift_start = event.y
        self.width_shift_end = event.x
        self.height_shift_end = event.y

        print(event.x, event.y)
        self.parent.image_frame.canvas.scan_dragto(event.x, event.y, gain=1)

    def scan_img(self, event):
        self.parent.image_frame.canvas.scan_mark(event.x, event.y)

    # END ADD
    #opencv
    def detect_face(self):
        res = self.parent.cv.detect_face(self.img)
        self.change_img(res)

    def detect_fullbody(self):
        res = self.parent.cv.detect_fullbody(self.img)
        self.change_img(res)

    def detect_smile(self):
        res = self.parent.cv.detect_smile(self.img)
        self.change_img(res)
    
    def detect_cars(self):
        res = self.parent.cv.detect_cars(self.img)
        self.change_img(res)

    def detect_edges(self):
        res = self.parent.cv.detect_edges(self.img)
        self.change_img(res)

    def pattern_match(self):
        res = self.parent.cv.pattern_match(self.img)
        self.change_img(res)
    #end opencv

    def __update_enhancer(self):
        self.parent.effects_bar.slider.get()
        self.__enhancer = ImageEnhance.Brightness(self.img)

    def __add_to_stack(self):
        if self.__stack_ix < len(self.__stack) - 1:
            self.__stack = self.__stack[0:self.__stack_ix + 1]

        self.__stack.append(self.img)
        self.__stack_ix += 1

