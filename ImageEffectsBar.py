from tkinter import END, EW, NE, SE, ttk
import tkinter as tk
from tkinter import END, EW, NE, SE, ttk
from tkinter import HORIZONTAL


class ImageEffectsBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.button_width = 12
        self.curr_column = 0
        self.slider = None
        self.slider_zoom = None
        self.selected_shape = None
        self.draw_option = None
        self.draw_size = None
        self.selected_paint_size = None
        self.width_entry = None
        self.height_entry = None
        self.draw_option = None
        self.draw_size = None
        self.effect_option = None
        self.text_input = None
        self.__create_widgets()

    def add_labels(self):
        filter_label = ttk.Label(self, text="Filters: ", borderwidth=2, relief="groove", width=10)
        filter_label.grid(row=0, column=0, columnspan=2, sticky=EW)

        filter_label = ttk.Label(self, text="Image convert: ", borderwidth=2, relief="groove")
        filter_label.grid(row=0, column=2, columnspan=3, sticky=EW)

        filter_label = ttk.Label(self, text="Drawing: ", borderwidth=2, relief="groove")
        filter_label.grid(row=0, column=5, columnspan=4, sticky=EW)

        filter_label = ttk.Label(self, text="Object recognize: ", borderwidth=2, relief="groove")
        filter_label.grid(row=0, column=9, columnspan=3, sticky=EW)

    def add_filter_buttons(self):
        button = ttk.Button(self, text="Paint Effect", command=self.parent.img_UI.paint_effect,
                            width=self.button_width)
        button.grid(row=1, column=self.curr_column)

        button = ttk.Button(self, text="Invert Effect", command=self.parent.img_UI.invert_effect,
                            width=self.button_width)
        button.grid(row=1, column=self.curr_column + 1)

        button = ttk.Button(self, text="Solarize Effect", command=self.parent.img_UI.solarize_effect,
                            width=self.button_width)
        button.grid(row=3, column=self.curr_column)

        button = ttk.Button(self, text='Filter Color', command=self.parent.img_UI.change_color,
                            width=self.button_width)
        button.grid(row=3, column=self.curr_column + 1)

        self.curr_column += 2

    def add_convert_buttons(self):
        button = ttk.Button(self, text="Rotate Left", command=self.parent.img_UI.rotate_left,
                            width=self.button_width)
        button.grid(row=1, column=self.curr_column)

        button = ttk.Button(self, text="Rotate Right", command=self.parent.img_UI.rotate_right,
                            width=self.button_width)
        button.grid(row=1, column=self.curr_column + 1)

        button = ttk.Button(self, text="Flip Horizontally", command=self.parent.img_UI.flip_horizontally,
                            width=self.button_width)
        button.grid(row=3, column=self.curr_column)

        button = ttk.Button(self, text="Flip Vertically", command=self.parent.img_UI.flip_vertically,
                            width=self.button_width)
        button.grid(row=3, column=self.curr_column + 1)

        button = ttk.Button(self, text="Resolution", command=self.open_window, width=self.button_width)
        button.grid(row=1, column=self.curr_column + 2)

        button = ttk.Button(self, text="Crop", command=self.parent.image_frame.start_cropping,
                            width=self.button_width)
        button.grid(row=3, column=self.curr_column + 2)

        self.curr_column += 3

    def add_draw_effect_fields(self):
        button = ttk.Button(self, text='Color', command=self.parent.img_UI.draw, width=self.button_width // 2)
        button.grid(row=1, column=self.curr_column)

        shape_label = ttk.Label(self, text="Shape: ", width=self.button_width // 2)
        shape_label.grid(row=1, column=self.curr_column + 1)

        selected_shape = tk.StringVar()
        self.draw_option = ttk.Combobox(self, textvariable=selected_shape, width=self.button_width // 2,
                                        state="readonly")
        self.draw_option['values'] = ['circle', 'rectangle', 'triangle']
        self.draw_option.current(0)

        self.draw_option.grid(row=1, column=self.curr_column + 2)

        shape_label = ttk.Label(self, text="Effect: ", width=self.button_width // 2)
        shape_label.grid(row=3, column=self.curr_column + 1)

        selected_effect_option = tk.StringVar()

        selected_draw_effect = tk.StringVar()

        self.effect_option = ttk.Combobox(self, textvariable=selected_effect_option, width=self.button_width // 2,
                                          state="readonly")
        self.effect_option['values'] = ['filled', 'very light border', 'light border', 'medium border', "solid border"]
        self.effect_option.current(0)

        self.effect_option.grid(row=3, column=self.curr_column + 2)

        def shape_changed(event):
            self.parent.img_UI.do_capture = False

        self.draw_option.bind('<<ComboboxSelected>>', shape_changed)

        selected_paint_size = tk.StringVar()

        self.draw_size = ttk.Combobox(self, textvariable=selected_paint_size, width=4, state="readonly")
        self.draw_size['values'] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.draw_size.current(5)
        self.draw_size.grid(row=3, column=self.curr_column)

        def paint_size_changed(event):
            self.parent.img_UI.do_capture = False

        self.draw_size.bind('<<ComboboxSelected>>', paint_size_changed)

        # TEST TEXT
        button = ttk.Button(self, text='Text add', command=self.parent.img_UI.text_effect, width=self.button_width)
        button.grid(row=3, column=self.curr_column + 3)

        self.text_input = tk.Entry(self, width=self.button_width)  # ,justify="right"
        self.text_input.insert(END, 'add text')
        self.text_input.grid(row=1, column=self.curr_column + 3)

        self.curr_column += 4

    def add_object_detection_buttons(self):
        self.curr_column = 9
        button = ttk.Button(self, text='Face', command=self.parent.img_UI.detect_face, width=self.button_width)
        button.grid(row=1, column=self.curr_column)

        button = ttk.Button(self, text='Full body', command=self.parent.img_UI.detect_full_body,
                            width=self.button_width)
        button.grid(row=1, column=self.curr_column + 1)

        button = ttk.Button(self, text='smile', command=self.parent.img_UI.detect_smile, width=self.button_width)
        button.grid(row=1, column=self.curr_column + 2)
        button = ttk.Button(self, text='cars', command=self.parent.img_UI.detect_cars, width=self.button_width)
        button.grid(row=3, column=self.curr_column)
        button = ttk.Button(self, text='edges', command=self.parent.img_UI.detect_edges, width=self.button_width)
        button.grid(row=3, column=self.curr_column + 1)

        button = ttk.Button(self, text='Pattern match', command=self.parent.img_UI.pattern_match,
                            width=self.button_width)
        button.grid(row=3, column=self.curr_column + 2)

        self.curr_column += 3

    def add_computional_photograpy(self):
        button = ttk.Button(self, text='Denoise', command=self.parent.img_UI.denoise, width=self.button_width // 2)
        button.grid(row=0, column=self.curr_column)

        button = ttk.Button(self, text='Inpaint', command=self.parent.img_UI.inpaint,
                            width=self.button_width // 2)
        button.grid(row=1, column=self.curr_column)

        button = ttk.Button(self, text='HDR', command=self.parent.img_UI.hdr, width=self.button_width // 2)
        button.grid(row=3, column=self.curr_column)

        self.curr_column += 1

    def add_sliders(self):
        slider_label = ttk.Label(self, text='Brightness: ')
        slider_label.grid(row=0, column=self.curr_column, sticky=NE, rowspan=2)

        self.slider = ttk.Scale(self, from_=0, to=2, orient=HORIZONTAL, value=1)
        self.slider.bind("<ButtonRelease-1>", self.parent.img_UI.brightness_effect)
        self.slider.grid(row=0, column=self.curr_column + 1, sticky=NE, rowspan=2)

        slider_label = ttk.Label(self, text='Zoom: ')
        slider_label.grid(row=2, column=self.curr_column, sticky=SE, rowspan=2)

        self.slider_zoom = ttk.Scale(self, from_=1, to=5, orient=HORIZONTAL, value=1)
        self.slider_zoom.bind("<ButtonRelease-1>", self.parent.img_UI.do_zoom)
        self.slider_zoom.grid(row=2, column=self.curr_column + 1, sticky=SE, rowspan=2)

        self.curr_column += 2

    def __create_widgets(self):
        self.add_labels()
        self.add_filter_buttons()
        self.add_convert_buttons()
        self.add_draw_effect_fields()
        self.add_object_detection_buttons()
        self.add_computional_photograpy()
        self.add_sliders()

    def open_window(self):
        new_window = tk.Toplevel(self.parent)
        new_window.geometry("300x150")
        new_window.resizable(False, False)

        width_label = ttk.Label(new_window, text="Width:")
        width_label.pack(fill='x')

        self.width_entry = ttk.Entry(new_window)
        self.width_entry.pack(fill='x')
        self.width_entry.focus()

        height_label = ttk.Label(new_window, text="Height:")
        height_label.pack(fill='x')

        self.height_entry = ttk.Entry(new_window)
        self.height_entry.pack(fill='x')

        button = ttk.Button(new_window, text="save", command=self.parent.img_UI.change_resolution)
        button.pack(fill='x')
