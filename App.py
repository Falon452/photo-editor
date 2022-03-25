import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk


class MenuBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        menubar = tk.Menu(parent, background='#ff8000', foreground='black', activebackground='white',
                          activeforeground='black')

        parent.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False)

        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(
            label='Open Image',
            command=parent.toolbar.file_dialog,
        )

        file_menu.add_separator()

        file_menu.add_command(
            label='Exit',
            command=parent.destroy,
        )


class ToolBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.__create_widgets()

    def __create_widgets(self):
        self.button = ttk.Button(self, text="Open Image", command=self.file_dialog)
        self.button.pack()

    def file_dialog(self):
        self.filepath = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                                   filetypes=(("PNG files", "*.png"), ("JPG files", "*.jpg"),
                                                              ("all files", "*.*")))
        if self.filepath:
            self.parent.imageframe.set_image(filepath=self.filepath)


class ImageFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.image_label = ttk.Label(self)
        self.image_label.pack()

    def set_image(self, filepath):
        self.image_label.pack_forget()  # otherwise images are stacking up
        PIL_image = Image.open(filepath)
        tk_image = tk.PhotoImage(filepath)

        img = Image.open(filepath)
        photo = ImageTk.PhotoImage(img)

        self.image_label = ttk.Label(self, image=photo)
        self.image_label.image = photo  # this is necessary

        self.image_label.pack()


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Photo Editor")

        window_width = 600
        window_height = 400

        self.minsize(window_width, window_height)

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.toolbar = ToolBar(self)
        self.menubar = MenuBar(self)
        self.imageframe = ImageFrame(self)

        self.imageframe.pack(side="bottom", fill="x", expand=True)
        self.toolbar.pack(side="top", fill="x")


if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
