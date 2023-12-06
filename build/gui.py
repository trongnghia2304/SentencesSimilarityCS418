
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

from ast import List
import os
from pathlib import Path
from os import listdir
from os.path import isfile, join
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,filedialog
from tkinter import *
from token import COMMA
from tokenize import String


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")
def update_scroll_region():
    frame.update_idletasks()
    scrollable_canvas.config(scrollregion=scrollable_canvas.bbox("all"))

def clear_text_widgets():
    for widget in text_widgets:
        widget.destroy()
    text_widgets.clear()

def browse_button():
    foldername = filedialog.askdirectory()
    folder_path.set(foldername)
    print(foldername)
    print("button_1 clicked")
    button_1['text'] = foldername if(foldername) else "Choose folder"
    folder_storage = list()

    if foldername:
        clear_text_widgets()
        for file in os.listdir(foldername):
            if file.endswith(".txt"):
                file_path = os.path.join(foldername, file)
                folder_storage.append(file_path)
                print(os.path.join("/mydir", file))

        # Create Text widgets dynamically based on the length of folder_storage
        for i in range(len(folder_storage)):
            entry_image_i = PhotoImage(file=relative_to_assets(f"entry_2.png"))
            entry_i = Text(
                scrollable_canvas,
                bd=0,
                bg="#FFFFFF",
                fg="#000716",
                highlightthickness=0,
                padx=10,
                pady=10,
            )
            entry_i.place(
                relx=0,  # Specify the relative x-coordinate
                y=i * 400,  # Adjust the y-coordinate for each Text widget
                width=406.0,
                height=375.0
            )
            text_widgets.append(entry_i)

            # Associate each Text widget with the corresponding content from folder_storage
            content = get_content(folder_storage[i])
            entry_i.insert("end", f"File {i + 1}:\n")
            entry_i.insert("end", content)
            entry_i.insert("end", "\n\n")
            entry_i.config(state=DISABLED)
            
        update_scroll_region()

    print(len(folder_storage))

   
def get_content(filename):
    with open(filename) as f:
        contents = f.read()
    return contents

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

text_widgets = []
folder_path = StringVar()
folder_storage = list()
window.geometry("1055x668")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 668,
    width = 1055,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    31.0,
    64.0,
    anchor="nw",
    text="Choose folder",
    fill="#000000",
    font=("Inter Bold", 25 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    text='Choose folder',
    font=("Helvetica",16),
    borderwidth=0,
    highlightbackground="#000000",
    highlightthickness=0,
    command= browse_button,
    relief="flat"
)
button_1.place(
    x=246.0,
    y=41.0,
    width=297.0,
    height=66.0
)

canvas.create_text(
    31.0,
    528.0,
    anchor="nw",
    text="Type in similarity level (%):",
    fill="#000000",
    font=("Inter Bold", 25 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    471.5,
    543.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=400.0,
    y=520.0,
    width=143.0,
    height=44.0
)

canvas.create_rectangle(
    572.0,
    25.999908447265625,
    576.4921875,
    575.0000305175781,
    fill="#000000",
    outline="")

canvas.create_text(
    612.0,
    28.0,
    anchor="nw",
    text="List of similarity text:",
    fill="#000000",
    font=("Inter Bold", 25 * -1)
)




entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    280.5,
    324.0,
    image=entry_image_3
)

# Declare scroll_y before using it in entry_3

entry_3 = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    wrap='none'
)
scroll_y = Scrollbar(entry_3)
scroll_y.pack(side=RIGHT, fill=Y)
entry_3.place(
    x=18.0,
    y=150.0,
    width=525.0,
    height=346.0,
)

# Configure scroll_y after entry_3 is created
entry_3.config(yscrollcommand=scroll_y.set)
scroll_y.config(command=entry_3.yview)

# Create a scrollable canvas
scrollable_canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=668,
    width=1055,
    bd=0,
    highlightthickness=3,
    relief="ridge"
)
scrollable_canvas.place(x=600.0, y=80.0,
    width=430.0,
    height=520.0,)

# Create a vertical scrollbar
scroll_y1 = Scrollbar(scrollable_canvas)
scroll_y1.pack(side=RIGHT, fill=Y)

# Configure the canvas to be scrollable
scrollable_canvas.config(yscrollcommand=scroll_y1.set)
scroll_y1.config(command=scrollable_canvas.yview)

# Create a frame to contain all the widgets
frame = Frame(scrollable_canvas, bg="#FFFFFF")
scrollable_canvas.create_window((0, 0), window=frame, anchor="nw")

# Update the scroll region of the canvas
frame.update_idletasks()
scrollable_canvas.config(scrollregion=scrollable_canvas.bbox("all"))

canvas.create_rectangle(
    627.0,
    497.5,
    1021.5,
    498.5,
    fill="#000000",
    outline="")


canvas.create_rectangle(
    669.0,
    888.0,
    1080.0,
    890.0,
    fill="#000000",
    outline="")
window.resizable(False, False)
window.mainloop()
