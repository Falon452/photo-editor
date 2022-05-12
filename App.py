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

# pip install opencv-contrib-python
# pip install imutils
# pip install Pillow
global toggle



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
        
        self.button_width = 15
        self.__create_widgets()

    def add_labels(self):
        self.filter_label = ttk.Label(self , text="Filters: " , borderwidth=2, relief="groove")
        self.filter_label.grid(row = 0 , column=0 ,columnspan=2 , sticky= EW)

        self.filter_label = ttk.Label(self , text="Image convert: " , borderwidth=2, relief="groove")
        self.filter_label.grid(row = 0 , column=2  ,columnspan=3 , sticky= EW )

        self.filter_label = ttk.Label(self , text="Drawing: " , borderwidth=2, relief="groove")
        self.filter_label.grid(row = 0 , column=5 ,columnspan=3 , sticky= EW )

        self.filter_label = ttk.Label(self , text="Object recognize: " , borderwidth=2, relief="groove")
        self.filter_label.grid(row = 0 , column=8 ,columnspan=2  , sticky= EW)


    def add_filter_buttons(self):
        self.button = ttk.Button(self, text="Paint Effect", command=self.parent.img_UI.paint_effect ,width=self.button_width)
        self.button.grid(row=1, column=0)

        self.button = ttk.Button(self, text="Invert Effect", command=self.parent.img_UI.invert_effect ,width=self.button_width)
        self.button.grid(row=1, column=1)

        self.button = ttk.Button(self, text="Solarize Effect", command=self.parent.img_UI.solarize_effect ,width=self.button_width)
        self.button.grid(row=3, column=0)

        self.button = ttk.Button(self, text='Filter Color', command=self.parent.img_UI.change_color ,width=self.button_width)
        self.button.grid(row=3, column=1)
       
    def add_convert_buttons(self):
        self.button = ttk.Button(self, text="Rotate Left", command=self.parent.img_UI.rotate_left ,width=self.button_width)
        self.button.grid(row=1, column=2)

        self.button = ttk.Button(self, text="Rotate Right", command=self.parent.img_UI.rotate_right ,width=self.button_width)
        self.button.grid(row=1, column=3)


        self.button = ttk.Button(self, text="Flip Horizontally", command=self.parent.img_UI.flip_horizontally ,width=self.button_width)
        self.button.grid(row=3, column=2)

        self.button = ttk.Button(self, text="Flip Vertically", command=self.parent.img_UI.flip_vertically ,width=self.button_width)
        self.button.grid(row=3, column=3)

        self.button = ttk.Button(self, text="Resolution", command=self.open_window ,width=self.button_width)
        self.button.grid(row=1, column=4)

        self.button = ttk.Button(self, text="Crop", command=self.parent.image_frame.start_cropping ,width=self.button_width)
        self.button.grid(row=3, column=4)
    
    def add_object_detection_buttons(self):
        self.button = ttk.Button(self, text='Face', command=self.parent.img_UI.detect_face)
        self.button.grid(row=1, column=8)

        self.button = ttk.Button(self, text='Full body', command=self.parent.img_UI.detect_fullbody)
        self.button.grid(row=1, column=9)

        self.button = ttk.Button(self, text='smile', command=self.parent.img_UI.detect_smile)
        self.button.grid(row=2, column=8)
        self.button = ttk.Button(self, text='cars', command=self.parent.img_UI.detect_cars)
        self.button.grid(row=2, column=9)
        self.button = ttk.Button(self, text='edges', command=self.parent.img_UI.detect_edges)
        self.button.grid(row=3, column=8)

        self.button = ttk.Button(self, text='Pattern match', command=self.parent.img_UI.pattern_match)
        self.button.grid(row=3, column=9)

    def __create_widgets(self):
        self.add_labels()
        self.add_filter_buttons()
        self.add_convert_buttons()
        self.add_object_detection_buttons()

        # Sliders

        self.slider_label = ttk.Label(self, text='Brightness: ')
        self.slider_label.grid(row=0, column=10 , sticky=NE  , rowspan=2)

        self.slider = ttk.Scale(self, from_=0, to=2, orient=HORIZONTAL, value=1)
        self.slider.bind("<ButtonRelease-1>", self.parent.img_UI.brightness_effect)
        self.slider.grid(row=0, column=11 , sticky=NE , rowspan=2)

        self.slider_label = ttk.Label(self, text='Zoom: ' )
        self.slider_label.grid(row=2, column=10, sticky=SE , rowspan=2)
        self.slider_zoom = ttk.Scale(self, from_=1, to=5, orient=HORIZONTAL, value=1)
        self.slider_zoom.bind("<ButtonRelease-1>", self.parent.img_UI.do_zoom)
        self.slider_zoom.grid(row=2, column=11,sticky=SE , rowspan=2)

        #Draw effects fields

        self.button = ttk.Button(self, text='Color', command=self.parent.img_UI.draw ,width=self.button_width//2)
        self.button.grid(row=1, column=5)


        self.shape_label = ttk.Label(self , text="Shape: " ,width=self.button_width//2)
        self.shape_label.grid(row = 1 , column=6)
        self.selected_shape = tk.StringVar()
        self.draw_option = ttk.Combobox(self, textvariable=self.selected_shape  , width=18 , state="readonly")
        self.draw_option['values'] = ['circle', 'rectangle', 'triangle']
        self.draw_option.current(0)
        
        self.draw_option.grid(row=1, column=7)

        self.shape_label = ttk.Label(self , text="Effect: " ,width=self.button_width//2)
        self.shape_label.grid(row = 3 , column=6)
       
        self.selected_effect_option = tk.StringVar()
        
        self.selected_draw_effect = tk.StringVar()
        self.effect_option = ttk.Combobox(self, textvariable=self.selected_effect_option  , width=18 , state="readonly")
        self.effect_option['values'] = ['filled', 'very light border','light border' , 'medium border' , "solid border" ]
        self.effect_option.current(0)
     

        self.effect_option.grid(row=3, column=7)

        def shape_changed(event):
            self.parent.img_UI.do_capture = False

        self.draw_option.bind('<<ComboboxSelected>>', shape_changed)

        self.selected_paint_size = tk.StringVar()

        self.draw_size = ttk.Combobox(self, textvariable=self.selected_paint_size, width=4 , state="readonly" )
 
        self.draw_size['values'] = [2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        
        self.draw_size.current(5)
        self.draw_size.grid(row=3, column=5)

        def paint_size_changed(event):
            self.parent.img_UI.do_capture = False

        self.draw_size.bind('<<ComboboxSelected>>', paint_size_changed)

       
        # END ADD

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
                cv2.rectangle(zoomed, (int(event.x) , int(event.y)),
                    int(event.x * (zoomed.shape[1] / width)) + int(paint_size * 2 * (zoomed.shape[0] / height)),
                    int(event.y * (zoomed.shape[0] / height)) + int(paint_size * 2 * (zoomed.shape[0] / height)), draw_color, effect_map[effect_idx])
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


class ImageFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.image_label = ttk.Label(self)
        self.image_label.pack()
        self.show_resolution = (600, 450)

        self.canvas = tk.Canvas(self, bg="gray", width=600, height=450)

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


class ObjectDetection():
    def __init__(self, parent):
        self.parent = parent
        self.face_cascade = None
        self.smile_cascade = None
        self.cars_cascade = None

    def detect_face(self, img):
        img = np.array(img)
        if not self.face_cascade:
            self.face_cascade = cv2.CascadeClassifier()

        if not self.face_cascade.load(cv2.samples.findFile('haarcascades\haarcascade_frontalface_alt.xml')):
            print('--(!)Error loading face cascade')
            exit(0)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.equalizeHist(img_gray)

        faces = self.face_cascade.detectMultiScale(img_gray, scaleFactor=1.05, minNeighbors=5)
        
        print(f"Number of faces detected: {len(faces)}")

        for (x,y,w,h) in faces:
            center = (x + w//2, y + h//2)
            img = cv2.ellipse(img, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)

        res = Image.fromarray(img)
        return res 
    

    def detect_smile(self, img):
        img = np.array(img)
        if not self.smile_cascade:
            self.smile_cascade = cv2.CascadeClassifier()
        if not self.face_cascade:
            self.face_cascade = cv2.CascadeClassifier()

        if not self.face_cascade.load(cv2.samples.findFile('haarcascades\haarcascade_frontalface_alt.xml')):
            print('--(!)Error loading face cascade')
            exit(0)
        if not self.smile_cascade.load(cv2.samples.findFile('haarcascades\haarcascade_smile.xml')):
            print('--(!)Error loading smile cascade')
            exit(0)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.equalizeHist(img_gray)

        faces = self.face_cascade.detectMultiScale(img_gray, scaleFactor=1.05, minNeighbors=5)
        
        for (x,y,h,w) in faces:
            center = (x + w//2, y + h//2)
            face = img[y : y + h, x : x + w, :]
            face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            face_gray = cv2.equalizeHist(face_gray)

            smiles = self.smile_cascade.detectMultiScale(face_gray, scaleFactor=1.05, minNeighbors=11)

            for (x1,y1,w1,h1) in smiles:
                center = (x + x1 + w1//2, y + y1 + h1//2)
                img = cv2.ellipse(img, center, (w1//2, h1//2), 0, 0, 360, (249, 215, 18), 3)

        res = Image.fromarray(img)
        return res 

    def detect_fullbody(self, img):
        img = np.array(img)

        hog = cv2.HOGDescriptor() 
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector()) 
        
        (humans, _) = hog.detectMultiScale(img,  
                                            winStride=(4, 4),
                                            padding=(8, 8),
                                            scale=1.03)
      
        humans = np.array([[x, y, x + w, y + h] for (x, y, w, h) in humans])                           
        humans = non_max_suppression(humans, probs=None, overlapThresh=0.45)
        print('Humans detected: ', len(humans))
        
        for (x, y, x1, y1) in humans:
            cv2.rectangle(img, (x, y),  
                        (x1, y1),  
                        (0, 0, 255), 2) 

        res = Image.fromarray(img)
        return res 

    def detect_cars(self, img):
        img = np.array(img)
        if not self.cars_cascade:
            self.cars_cascade = cv2.CascadeClassifier()

        if not self.cars_cascade.load(cv2.samples.findFile('haarcascades\haarcascade_cars.xml')):
            print('--(!)Error loading cars cascade')
            exit(0)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cars = self.cars_cascade.detectMultiScale(gray, 1.1, 1)

        cars = np.array([[x, y, x + w, y + h] for (x, y, w, h) in cars])                           
        cars = non_max_suppression(cars, probs=None, overlapThresh=0.45)

        for (x, y, x1, y1) in cars:
            cv2.rectangle(img, (x, y),  
                        (x1, y1),  
                        (0, 0, 255), 2) 

        res = Image.fromarray(img)
        return res
    
    def detect_edges(self, img):
        img = np.array(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
        corners = np.int0(corners)

        for i in corners:
            x,y = i.ravel()
            cv2.circle(img,(x,y), 3, (0, 255, 0), -1)
        
        res = Image.fromarray(img)
        return res

    def pattern_match(self, img):
        NO_MATCHES = 5

        original = np.array(img)

        filepath = filedialog.askopenfilename(initialdir="/", title="Select a pattern",
                                              filetypes=(("PNG files", "*.png"), ("JPG files", "*.jpg"),
                                                         ("all files", "*.*")))

        pattern = cv2.imread(filepath) # trainImage
        pattern = Image.fromarray(pattern)
        pattern = pattern.convert('RGB')
        pattern = np.array(pattern)


        gray_face = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)
        gray_pattern = cv2.cvtColor(pattern, cv2.COLOR_RGB2GRAY)

        orb = cv2.ORB_create()
        original_keypoints, original_descriptor = orb.detectAndCompute(gray_face, None)
        query_keypoints, query_descriptor = orb.detectAndCompute(gray_pattern, None)
        keypoints_without_size = np.copy(original)
        keypoints_with_size = np.copy(original)

        cv2.drawKeypoints(original, original_keypoints, keypoints_without_size, color = (0, 255, 0))
        cv2.drawKeypoints(original, original_keypoints, keypoints_with_size, flags = 
        cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

        matches = brute_force.match(original_descriptor, query_descriptor)
        matches = sorted(matches, key = lambda x : x.distance)
        
        matches = matches[:NO_MATCHES]

        result = cv2.drawMatches(original, original_keypoints, gray_pattern, query_keypoints, matches, 
        gray_pattern, flags = 2)
        print("The number of matching keypoints between the original and the query image is {}\n".format(len(matches)))

        res = Image.fromarray(result)
        return res

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Photo Editor")

        window_width  = 1100 #800
        window_height = 800  #600

        self.minsize(window_width, window_height)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')  # open in middle of scren

        self.img_UI = ImgUI(self)
        self.image_frame = ImageFrame(self)
        self.cv = ObjectDetection(self)
        self.effects_bar = ImageEffectsBar(self)
        self.menu_bar = MenuBar(self)

        self.image_frame.pack(side="bottom", fill="x", expand=True)
        self.menu_bar.pack(side="top", fill="x")
        self.effects_bar.pack(side="left", fill="x")

        self._bindings()
        # self.__debugging()

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

    # def __debugging(self):
    #     self.img_UI.set_image(filepath='/Users/damiantworek/Desktop/pic.png')


if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()