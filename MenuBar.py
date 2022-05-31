import tkinter as tk
from tkinter import ttk


class MenuBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.menu_bar = tk.Menu(parent, background='#ff8000', foreground='black', activebackground='white',
                                activeforeground='black')

        self.parent.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label='Open Image',
            command=self.parent.img_UI.open_image,
        )
        file_menu.add_command(
            label='Open Image from URL',
            command=self.parent.image_frame.open_image_url_window,
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

        edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(
            label='Undo',
            command=self.parent.img_UI.undo
        )
        edit_menu.add_command(
            label='Redo',
            command=self.parent.img_UI.redo
        )
