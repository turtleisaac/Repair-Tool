from tkinter import ttk, TOP, TRUE, LEFT, W, E
from tkinter import filedialog
from tkinter import messagebox
from ttkthemes import ThemedTk
import os
from tkinter.ttk import *
from tkinter import *

from Repairer import Repairer

# Developed by Turtleisaac

root = ThemedTk(theme="breeze")
root.title('Repair Tool')
root.resizable(False, False)
root.geometry('350x100')

top_frame = ttk.Frame(root)
top_frame.pack(side=TOP, pady=1)

style = ttk.Style()
style.configure("Hyperlink.TLabel", foreground="blue")

label1 = ttk.Label(top_frame, text="Repair Tool", font='Helvetica 18 bold')
label2 = ttk.Label(top_frame, text="Created by Turtleisaac")
label3 = ttk.Label(top_frame, text="PPREctifies what's been PPRExploded", font='14')


def create():
    filetypes = [
        ('NDS File', '*.nds *.srl')
    ]

    rom_in = filedialog.askopenfile(title='Select ROM', filetypes=filetypes, mode='r')
    if rom_in is not None:
        rom_path = os.path.abspath(rom_in.name)
        rom_in.close()

        repairer = Repairer(rom_path)
        repairer.repair()

        f_out = filedialog.asksaveasfilename(title='Select Output File', defaultextension=".nds")
        if f_out is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        filepath_output = os.path.abspath(f_out)

        # creator.pickle(filepath_output)
        messagebox.showinfo(title='Repair Tool', message='ROM Repair Complete! Output can be found at:\n' +
                                                         filepath_output)


# open button
create_button = ttk.Button(
    top_frame,
    text='Repair ROM',
    command=create,
    width=30,
    # font='Helvetica 12 bold'
)

label1.grid(row=0, column=0, columnspan=2)
label3.grid(row=1, column=0, columnspan=2)
create_button.grid(row=2, column=0, columnspan=2, pady=5)
label2.grid(row=3, column=0, columnspan=2)
top_frame.columnconfigure(0, weight=5, uniform='row')
top_frame.columnconfigure(1, weight=7, uniform='row')

root.eval('tk::PlaceWindow . center')

root.mainloop()
