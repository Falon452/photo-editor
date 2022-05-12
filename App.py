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
from ImageUI import ImgUI
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
        self.filter_label.grid(row = 0 , column=8 ,columnspan=3  , sticky= EW)


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
        self.button = ttk.Button(self, text='Face', command=self.parent.img_UI.detect_face  ,width=self.button_width)
        self.button.grid(row=1, column=8)

        self.button = ttk.Button(self, text='Full body', command=self.parent.img_UI.detect_fullbody  ,width=self.button_width)
        self.button.grid(row=1, column=9)

        self.button = ttk.Button(self, text='smile', command=self.parent.img_UI.detect_smile ,width=self.button_width)
        self.button.grid(row=1, column=10)
        self.button = ttk.Button(self, text='cars', command=self.parent.img_UI.detect_cars  ,width=self.button_width)
        self.button.grid(row=3, column=8)
        self.button = ttk.Button(self, text='edges', command=self.parent.img_UI.detect_edges  ,width=self.button_width)
        self.button.grid(row=3, column=9)

        self.button = ttk.Button(self, text='Pattern match', command=self.parent.img_UI.pattern_match  ,width=self.button_width)
        self.button.grid(row=3, column=10)

    def __create_widgets(self):
        self.add_labels()
        self.add_filter_buttons()
        self.add_convert_buttons()
        self.add_object_detection_buttons()

        # Sliders

        self.slider_label = ttk.Label(self, text='Brightness: ')
        self.slider_label.grid(row=0, column=11 , sticky=NE  , rowspan=2)

        self.slider = ttk.Scale(self, from_=0, to=2, orient=HORIZONTAL, value=1)
        self.slider.bind("<ButtonRelease-1>", self.parent.img_UI.brightness_effect)
        self.slider.grid(row=0, column=12 , sticky=NE , rowspan=2)

        self.slider_label = ttk.Label(self, text='Zoom: ' )
        self.slider_label.grid(row=2, column=11, sticky=SE , rowspan=2)
        self.slider_zoom = ttk.Scale(self, from_=1, to=5, orient=HORIZONTAL, value=1)
        self.slider_zoom.bind("<ButtonRelease-1>", self.parent.img_UI.do_zoom)
        self.slider_zoom.grid(row=2, column=12,sticky=SE , rowspan=2)

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

        window_width  = 1200 #800
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