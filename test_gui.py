from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import os
import re
import random
import algo

list_input_folder = []
list_compare_folder = []
sentences_by_file_input = [] 
sentences_by_file_compare = [] 
list_color_hex = []
similarity_level = 0

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def split_sentences(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return sentences

def random_hex_color():
    # Generate three random numbers between 0 and 255
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    
    # Convert them to hex format
    r_hex = hex(r)[2:]
    g_hex = hex(g)[2:]
    b_hex = hex(b)[2:]

    # Add leading zeros if necessary
    if len(r_hex) == 1:
        r_hex = "0" + r_hex
    if len(g_hex) == 1:
        g_hex = "0" + g_hex
    if len(b_hex) == 1:
        b_hex = "0" + b_hex

    # Return the hex color code as a string
    global list_color_hex
    if "#" + r_hex + g_hex + b_hex in list_color_hex:
        return random_hex_color()
    else:
        list_color_hex.append("#" + r_hex + g_hex + b_hex)
    return "#" + r_hex + g_hex + b_hex

def draw_window(title, size, bg_color):
    window = tk.Tk()
    window.title(title)
    window.geometry(size)
    window.configure(bg=bg_color)
    return window

def create_button_widget(parent, text, font, bg_color, command):
    return tk.Button(parent, text=text, font=font, bg=bg_color, command=command)

def create_text_field_widget(parent, label_text):
    label = tk.Label(parent, text=label_text)
    entry = tk.Entry(parent)
    return label, entry

def update_folder_path_label(folder_path, label):
    label.config(text="Folder path: " + folder_path)

def choose_folder(folder_path_label, is_compare_folder, callback=None):
    current_dir = os.getcwd()
    foldername = filedialog.askdirectory(
        initialdir=current_dir,
        title="Select folder"
    )
    if not foldername:  # If the user cancelled the folder selection dialog
        foldername = "No folder selected"
        return None
    update_folder_path_label(foldername, folder_path_label)

    contents_data = list()  # List of contents of the files in the folder    
    list_folder = list()    # List of the files in the folder

    # Read the files in the folder
    for filename in os.listdir(foldername):
        list_folder.append(filename)
        if filename.endswith(".txt"):
            filepath = os.path.join(foldername, filename)
            with open(filepath, encoding='utf-8') as f:
                contents = f.read()
            contents_data.append(contents)

    # Split the contents of each file into sentences, map each file to a list of sentences
    sentences_by_file = list()
    for content in contents_data:
        sentences_by_file.append(split_sentences(content))

    if not is_compare_folder:
        global list_input_folder, sentences_by_file_input
        list_input_folder = list_folder
        sentences_by_file_input = sentences_by_file
    else:
        global list_compare_folder, sentences_by_file_compare
        list_compare_folder = list_folder
        sentences_by_file_compare = sentences_by_file

    if callback:
        callback()

def create_text_widgets_from_sentences(list_folder, sentences_by_file, parent):
    text_widgets = []
    parent.grid_columnconfigure(0, weight=1)  # Configure the column to expand

    for i in range(len(list_folder)):
        entry_i = tk.Text(
            parent,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            wrap='word',
            font=("Arial", 10),
            height=5,  # Set a default minimum height
        )
        entry_i.grid(row=i, column=0, sticky='nsew')  # Sticky 'nsew' to expand in all directions
        
        # Define a tag for bold text
        entry_i.tag_configure("bold", font=("Arial", 10, "bold"))

        color_hex = random_hex_color()

        # Define a tag for colored text
        entry_i.tag_configure("colored", foreground=color_hex)
        
        # Insert the file name with the bold tag
        file_name = f"File {list_folder[i]}:\n"
        entry_i.insert("end", file_name, "bold")
        
        # Insert the sentences normally
        for sentence in sentences_by_file[i]:
            entry_i.insert("end", sentence + '\n', "colored")
        entry_i.insert("end", '\n')  # Add an extra empty line for separation

        # Update the height of the Text widget to fit its content
        num_lines = int(entry_i.index('end-1c').split('.')[0])
        entry_i.config(height=num_lines)

        entry_i.config(state=tk.DISABLED)  # Disable editing
        text_widgets.append(entry_i)

    return text_widgets

def main():
    window = draw_window("Sentence Similarity Checker", "1055x830", "#FFFFFF")

    # Create the frames
    choose_compare_folder_frame = tk.Frame(window, bg="#FFFFFF")
    choose_input_folder_frame = tk.Frame(window, bg="#FFFFFF")
    similarity_frame = tk.Frame(window, bg="#FFFFFF")
    input_frame = tk.Frame(window, bg="#FFFFFF")  # Frame for input data
    compare_frame = tk.Frame(window, bg="#FFFFFF")  # Frame for compare data

    # Configure grid layout weights
    window.grid_columnconfigure(0, weight=1)  # Configure the column to expand
    window.grid_rowconfigure(5, weight=1)  # Configure the row to expand

    # Place the frames
    choose_compare_folder_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
    choose_input_folder_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
    similarity_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nw")
    input_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")  # Place input_frame
    compare_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")  # Place compare_frame

    # Create scrollable canvas in compare_frame
    compare_canvas = tk.Canvas(compare_frame, bg="#FFFFFF")
    compare_canvas.pack(side="left", fill="both", expand=True)

    # Create scrollable canvas in input_frame
    input_canvas = tk.Canvas(input_frame, bg="#FFFFFF")
    input_canvas.pack(side="left", fill="both", expand=True)

    # Add scrollbar to the canvas in compare_frame
    scrollbar = tk.Scrollbar(compare_frame, orient="vertical", command=compare_canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Add scrollbar to the canvas in input_frame
    scrollbar2 = tk.Scrollbar(input_frame, orient="vertical", command=input_canvas.yview)
    scrollbar2.pack(side="right", fill="y")

    # Configure the canvas in compare_frame
    compare_canvas.configure(yscrollcommand=scrollbar.set)
    scrollable_frame = tk.Frame(compare_canvas)
    compare_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1000)

    # Configure the canvas in input_frame
    input_canvas.configure(yscrollcommand=scrollbar2.set)
    scrollable_frame2 = tk.Frame(input_canvas)
    input_canvas.create_window((0, 0), window=scrollable_frame2, anchor="nw", width=1000)

    def update_scrollregion(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig("window", width=canvas.winfo_width())

    def on_folder_selected(compare_folder):
        if compare_folder:
            create_compare_widgets(scrollable_frame, list_compare_folder, sentences_by_file_compare)
        else:
            create_compare_widgets(scrollable_frame2, list_input_folder, sentences_by_file_input)

    def create_compare_widgets(scroll_frame, list_folder, sentences_by_file):
        for widget in scroll_frame.winfo_children():
            widget.destroy()
        create_text_widgets_from_sentences(list_folder, sentences_by_file, scroll_frame)

    # Adjust the lambda to pass the function reference
    choose_compare_folder_button = create_button_widget(
        choose_compare_folder_frame,
        "Choose compare folder",
        ("Arial", 12),
        "#FFFFFF",
        lambda: choose_folder(folder_path_label, True, lambda: on_folder_selected(True))
    )
    choose_compare_folder_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    choose_input_folder_button = create_button_widget(
        choose_input_folder_frame,
        "Choose input folder",
        ("Arial", 12),
        "#FFFFFF",
        lambda: choose_folder(input_folder_path_label, False, lambda: on_folder_selected(False))
    )
    choose_input_folder_button.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

    scrollable_frame.bind("<Configure>", lambda event: update_scrollregion(compare_canvas))
    scrollable_frame2.bind("<Configure>", lambda event: update_scrollregion(input_canvas))

    # Label to display the compare folder path
    folder_path_label = tk.Label(choose_compare_folder_frame, text="Folder path: No folder selected", font=("Arial", 10), bg="#FFFFFF")
    folder_path_label.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

    # Label to display the input folder path
    input_folder_path_label = tk.Label(choose_input_folder_frame, text="Folder path: No folder selected", font=("Arial", 10), bg="#FFFFFF")
    input_folder_path_label.grid(row=1, column=1, padx=10, pady=10, sticky="nw")

    # Create and place the similarity input field
    similarity_label, similarity_input = create_text_field_widget(similarity_frame, "Similarity level (%):")
    similarity_label.grid(row=1, column=0, padx=10, pady=2, sticky="nw")
    similarity_input.grid(row=1, column=1, padx=10, pady=2, sticky="nw")        # To get the input value, use similarity_input.get()

    def cal_similarity():
        global similarity_level, list_input_folder, list_compare_folder, sentences_by_file_input, sentences_by_file_compare
        similarity_level = similarity_input.get()
        res = algo.find_similar_sentences_in_files(list_input_folder, list_compare_folder, sentences_by_file_input[0], sentences_by_file_compare, float(similarity_level) / 100)
        print(similarity_level)
        for input_idx,file_idx,sentence_idx in res:
            print(f"input_idx: {input_idx}")
            print(f"file_idx: {file_idx}")
            print(f"sentence_idx: {sentence_idx}")

    # Create and place the "Compare" button
    compare_button = create_button_widget(similarity_frame, "Compare", ("Arial", 12), "#FFFFFF", lambda: cal_similarity())
    compare_button.grid(row=2, column=0, padx=10, pady=10, sticky="nw")

    window.mainloop()

if __name__ == "__main__":
    main()