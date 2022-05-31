from tkinter import filedialog
import tkinter as tk
import urllib.request
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from urllib.request import urlopen

import cv2
import numpy as np
from PIL import Image, ImageTk, ImageEnhance
from PIL import ImageOps
from Stack import Stack


class ImgUI:
    def __init__(self, parent):
        self.parent = parent
        self.img = None
        self.__enhancer = None
        self.stack = Stack()
        self.do_capture = False
        self.scale = 1.0
        self.width_move = 0  # vector of move in zoom
        self.height_move = 0  # vector of move in zoom
        self.new_value = 1
        self.last_event_x = None
        self.last_event_y = None
        self.crop_start_x = None
        self.crop_start_y = None
        self.crop_end_x = None
        self.crop_end_y = None
        self.rectangle_id = None
        self.draw_color = None

    def set_image(self, file_path):
        self.img = cv2.imread(file_path)
        self.parent.image_frame.show_resolution = (650 * self.img.shape[1] // self.img.shape[0], 650)

        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img = Image.fromarray(self.img)
        self.img = self.img.resize(self.parent.image_frame.show_resolution)

        self.stack.add(self.img)
        self.__update_enhancer()
        self.parent.image_frame.show_img(self.img)

    def save_image(self):
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if not filename:
            return
        self.img.save(filename)

    def open_image(self):
        file_path = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                               filetypes=(("PNG files", "*.png"), ("JPG files", "*.jpg"),
                                                          ("all files", "*.*")))
        if file_path:
            self.stack.clear()
            self.set_image(file_path)

    def change_img(self, res, brightness_effect=False, add_to_stack=True):
        self.img = res
        if not brightness_effect:
            self.__update_enhancer()
        if add_to_stack:
            self.stack.add(self.img)
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
        img = self.stack.undo()
        if img:
            self.img = img
            self.parent.image_frame.show_img(img)
            self.__update_enhancer()

    def redo(self):
        img = self.stack.redo()
        if img:
            self.img = img
            self.parent.image_frame.show_img(img)
            self.__update_enhancer()

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

    def capture(self, flag):
        self.do_capture = flag

    def draw(self):
        colors = askcolor(title="Color Chooser")
        self.draw_color = colors[0]
        self.parent.image_frame.draw_bind()

    def drawing_effect(self, event):
        if self.do_capture:
            effect_map = [-1, 1, 2, 3, 6]

            self.img = np.asarray(self.img)

            x, y = int(event.x - self.width_move), int(event.y - self.height_move)

            toggle = self.parent.effects_bar.draw_option.current()
            paint_size = 2 * self.parent.effects_bar.draw_size.current()
            effect_idx = self.parent.effects_bar.effect_option.current()
            width, height = self.parent.image_frame.show_resolution

            if paint_size < 0:
                paint_size = 4

            if toggle == 0:
                cv2.circle(self.img, (x, y),
                           int(paint_size * (self.img.shape[0] / height)), self.draw_color, effect_map[effect_idx])
            elif toggle == 1:
                cv2.rectangle(self.img, (x, y), (
                    int(x * (self.img.shape[1] / width)) + int(paint_size * 2 * (self.img.shape[0] / height)),
                    int(y * (self.img.shape[0] / height)) + int(paint_size * 2 * (self.img.shape[0] / height))),
                              self.draw_color, effect_map[effect_idx])
            elif toggle == 2:
                painting_size = int(paint_size) * 2
                pts = np.array(
                    [[x, y + painting_size * 0.66], [x - painting_size * 0.5, y - painting_size * 0.33],
                     [x + painting_size * 0.5, y - painting_size * 0.33]], np.int32)

                if effect_idx == 0:
                    cv2.fillPoly(self.img, [pts], self.draw_color)
                else:
                    pts = pts.reshape((-1, 1, 2))
                    cv2.polylines(self.img, [pts], True, self.draw_color, thickness=effect_map[effect_idx])

            res = np.asarray(self.img)
            res = Image.fromarray(res)
            self.change_img(res)

    def do_zoom(self, new_value):
        self.new_value = self.parent.effects_bar.slider_zoom.get()
        size = self.parent.image_frame.show_resolution
        resize_image = self.img.resize((int(size[0] * self.new_value), int(size[1] * self.new_value)))
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
        if not self.last_event_x or abs(event.x - self.last_event_x) > 10:
            self.last_event_x = event.x
            self.last_event_y = event.y
        else:
            self.width_move += event.x - self.last_event_x
            self.height_move += event.y - self.last_event_y
            self.last_event_x = event.x
            self.last_event_y = event.y
            self.parent.image_frame.canvas.scan_dragto(event.x, event.y, gain=1)

    def scan_img(self, event):
        self.parent.image_frame.canvas.scan_mark(event.x, event.y)

    def text_effect(self):
        self.parent.image_frame.add_text_bind()

    def add_text(self, event):
        self.new_value = self.parent.effects_bar.slider_zoom.get()
        size = self.parent.image_frame.show_resolution
        self.img = self.img.resize((int(size[0] * self.new_value), int(size[1] * self.new_value)))

        paint_size = self.parent.effects_bar.draw_size.current()

        if paint_size < 0:
            paint_size = 4  # default value
        text = self.parent.effects_bar.text_input.get()
        tmp_img = np.asarray(self.img)
        image_with_text = cv2.putText(img=tmp_img, text=text, org=(event.x + self.width_move, event.y),
                                      fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=paint_size, color=self.draw_color,
                                      thickness=paint_size)
        res = Image.fromarray(image_with_text)
        self.change_img(res)

    def detect_face(self):
        res = self.parent.cv.detect_face(self.img)
        self.change_img(res)

    def detect_full_body(self):
        res = self.parent.cv.detect_full_body(self.img)
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

    def denoise(self):
        res = self.parent.comp_photo.denoise(self.img)
        self.change_img(res)

    def inpaint(self):
        res = self.parent.comp_photo.inpaint(self.img)
        self.change_img(res)

    def hdr(self):
        res = self.parent.comp_photo.hdr(self.img)
        self.change_img(res)

    def __update_enhancer(self):
        self.parent.effects_bar.slider.get()
        self.__enhancer = ImageEnhance.Brightness(self.img)

    def open_img_from_url(self):
        url = self.parent.image_frame.entry1.get()
        self.parent.image_frame.root.destroy()
        resp = urllib.request.urlopen(url)
        self.img = np.asarray(bytearray(resp.read()), dtype="uint8")
        self.img = cv2.imdecode(self.img, cv2.COLOR_RGB2BGR)

        height, width = self.img.shape[0], self.img.shape[1]
        self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
        self.img = Image.fromarray(self.img)

        self.parent.image_frame.show_resolution = (int(650 * width / height), 650)

        self.img = self.img.resize(self.parent.image_frame.show_resolution)
        self.stack.add(self.img)
        # self.__add_to_stack()
        self.__update_enhancer()
        self.parent.image_frame.show_img(self.img)
