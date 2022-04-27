import tkinter as tk
from tkinter import ttk,ALL
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
        self.__create_widgets()

    def __create_widgets(self):
        self.button = ttk.Button(self, text="Paint Effect", command=self.parent.img_UI.paint_effect)
        self.button.grid(row=0, column=0)

        self.button = ttk.Button(self, text="Invert Effect", command=self.parent.img_UI.invert_effect)
        self.button.grid(row=0, column=1)

        self.button = ttk.Button(self, text="Solarize Effect", command=self.parent.img_UI.solarize_effect)
        self.button.grid(row=0, column=2)

        self.button = ttk.Button(self, text='Filter Color', command=self.parent.img_UI.change_color)
        self.button.grid(row=0, column=3)

        self.slider_label = ttk.Label(self, text='Brightness: ')
        self.slider_label.grid(row=0, column=4)

        self.slider = ttk.Scale(self, from_=0, to=2, orient=HORIZONTAL, value=1)
        self.slider.bind("<ButtonRelease-1>", self.parent.img_UI.brightness_effect)
        self.slider.grid(row=0, column=5)

        self.button = ttk.Button(self, text="Rotate Right", command=self.parent.img_UI.rotate_right)
        self.button.grid(row=1, column=0)

        self.button = ttk.Button(self, text="Rotate Left", command=self.parent.img_UI.rotate_left)
        self.button.grid(row=1, column=1)

        self.button = ttk.Button(self, text="Flip Horizontally", command=self.parent.img_UI.flip_horizontally)
        self.button.grid(row=1, column=2)

        self.button = ttk.Button(self, text="Flip Vertically", command=self.parent.img_UI.flip_vertically)
        self.button.grid(row=1, column=3)

        self.button = ttk.Button(self, text="Resolution", command=self.open_window)
        self.button.grid(row=1, column=4)

        self.button = ttk.Button(self, text="Crop", command=self.parent.image_frame.start_cropping)
        self.button.grid(row=1, column=5)


        #ADD
        self.button = ttk.Button(self, text='Drawing', command=self.parent.img_UI.draw)
        self.button.grid(row=1, column=6)

        
        selected_shape = tk.StringVar()
        self.draw_option = ttk.Combobox(self, textvariable=selected_shape)
        self.draw_option['values'] = ['circle', 'rectangle' ,'eclipse']
        
        self.draw_option['state'] = 'readonly'

        self.draw_option.grid(row=1, column=7)
        def shape_changed(event):
            self.parent.img_UI.do_capture=False
        self.draw_option.bind('<<ComboboxSelected>>', shape_changed)


        selected_paint_size = tk.StringVar()
        
        self.draw_size = ttk.Combobox(self, textvariable=selected_paint_size ,width=5)
        
        self.draw_size['values'] = [1,2,3,4,5,6,7,8]
        self.draw_size['state'] = 'readonly'
        self.draw_size.current(5)
        self.draw_size.grid(row=1, column=8)
        def  paint_size_changed(event):
            self.parent.img_UI.do_capture=False
        self.draw_size.bind('<<ComboboxSelected>>',  paint_size_changed)
        

        self.slider_label = ttk.Label(self, text='Zoom: ')
        self.slider_label.grid(row=0, column=6)
        self.slider_zoom = ttk.Scale(self, from_=1, to=5, orient=HORIZONTAL, value=1)
        self.slider_zoom.bind("<ButtonRelease-1>", self.parent.img_UI.do_zoom)
        self.slider_zoom.grid(row=0, column=7)
        #END ADD


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
        self.do_capture = False  #ADDED
        self.scale= 1.0 #ADDED
       

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

    #ADD
    def capture(self,flag):
            self.do_capture = flag

    def draw(self):
        colors = askcolor(title="Color Chooser")
        global draw_color 
        draw_color = colors[0]
        self.parent.image_frame.draw_bind()
    

    def drawing_effect(self,event):
        if self.do_capture:
            res= np.asarray(self.img)
            toggle = self.parent.effects_bar.draw_option.current()
            paint_size =2*self.parent.effects_bar.draw_size.current()
            if paint_size<0:
                paint_size = 4 #default value
            if  toggle==0: # print circles
                cv2.circle(res,(int((event.x)*(res.shape[1]/600)),int((event.y)*(res.shape[0]/450))),int(paint_size*(res.shape[0]/450)),draw_color, -1)
            elif  toggle==1:
                cv2.rectangle(res,(int((event.x)*(res.shape[1]/600)),int((event.y)*(res.shape[0]/450))),(int((event.x)*(res.shape[1]/600))+int(paint_size*2*(res.shape[0]/450)),int((event.y)*(res.shape[0]/450))+int(paint_size*2*(res.shape[0]/450))),draw_color,-1)
            else:
                cv2.circle(res,(int((event.x)*(res.shape[1]/600)),int((event.y)*(res.shape[0]/450))),int(paint_size*2*(res.shape[0]/450)),draw_color,int(1*(res.shape[0]/450)))
            
            
            res = Image.fromarray(res)
            self.change_img(res)



    def do_zoom(self,new_value):
        new_value = self.parent.effects_bar.slider_zoom.get()
        size = self.parent.image_frame.show_resolution
        resize_image = self.img.resize((int(size[0]*new_value) , int(size[1]*new_value)))
        self.img=resize_image
        if new_value == 1:   #not working - set in the middle of frame
            self.parent.image_frame.canvas.scan_dragto(0, 0, gain=1)
            self.change_img(self.img)
            return
        self.change_img(self.img)
        self.parent.image_frame.canvas.delete("all")
        self.parent.image_frame.shown_image = ImageTk.PhotoImage(resize_image)
        self.parent.image_frame.canvas.create_image(0,0, anchor=tk.NW, image=self.parent.image_frame.shown_image)
        self.parent.image_frame.canvas.pack()

       

    def move_img(self,event):
        #print(event.x, event.y)
        self.parent.image_frame.canvas.scan_dragto(event.x, event.y, gain=1)

    def scan_img(self,event):
        self.parent.image_frame.canvas.scan_mark(event.x, event.y)
    #END ADD

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
        res = res.resize(self.show_resolution)
        self.shown_image = ImageTk.PhotoImage(res)
        #self.zoom_img = self.shown_image
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
        self.canvas.bind('<Control-ButtonPress-1>',self.parent.img_UI.scan_img)
        self.canvas.bind("<Control-B1-Motion>", self.parent.img_UI.move_img )        


    def draw_bind(self):
        self.canvas.bind("<Motion>", self.parent.img_UI.drawing_effect)
        self.canvas.bind('<ButtonPress-1>', lambda event: self.parent.img_UI.capture(True))
        self.canvas.bind("<ButtonRelease-1>", lambda event: self.parent.img_UI.capture(False))



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
        #self.__debugging()

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