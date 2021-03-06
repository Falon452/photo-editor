import sys
import tkinter as tk

from CompPhotography import ComputionalPhotography
from ImageEffectsBar import ImageEffectsBar
from ImageFrame import ImageFrame
from ImageUI import ImgUI
from MenuBar import MenuBar
from ObjectDetection import ObjectDetection


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Photo Editor")


        window_width = 1400
        window_height = 800

        self.minsize(window_width, window_height)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')  # open in middle of scren

        self.img_UI = ImgUI(self)
        self.image_frame = ImageFrame(self)
        self.cv = ObjectDetection(self)
        self.comp_photo = ComputionalPhotography(self)
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

    def __debugging(self, img_path):
        self.img_UI.set_image(filepath=img_path)


if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()



