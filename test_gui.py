from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import os
import re

list_input_folder = []
list_compare_folder = []
sentences_by_file_input = [] 
sentences_by_file_compare = [] 
similarity_level = 0


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def split_sentences(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return sentences

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

def choose_folder(folder_path_label, is_input_folder, callback=None):
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

    if is_input_folder:
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

    num_lines = max([len(sentences) for sentences in sentences_by_file])

    for i in range(len(list_folder)):

        entry_i = tk.Text(
            parent,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            wrap='word',
            font=("Arial", 10),
            height=num_lines,
        )
        entry_i.grid(row=i, column=0, sticky='nsew')  # Sticky 'nsew' to expand in all directions
        
        # Insert the file name and its sentences
        entry_i.insert("end", f"File {list_folder[i]}:\n")
        for sentence in sentences_by_file[i]:
            entry_i.insert("end", sentence + '\n')
        entry_i.insert("end", '\n')
        entry_i.config(state=tk.DISABLED)  # Disable editing
        text_widgets.append(entry_i)

    return text_widgets


def main():
    window = draw_window("Sentence Similarity Checker", "1055x668", "#FFFFFF")

    # Create the frames
    choose_compare_folder_frame = tk.Frame(window, bg="#FFFFFF")
    choose_input_folder_frame = tk.Frame(window, bg="#FFFFFF")
    similarity_frame = tk.Frame(window, bg="#FFFFFF")
    input_frame = tk.Frame(window, bg="#FFFFFF")  # Frame for input data
    compare_frame = tk.Frame(window, bg="#FFFFFF")  # Frame for compare data

    # Configure grid layout weights
    window.grid_rowconfigure(3, weight=1)  # Adjusted to allocate space for input_frame and compare_frame
    window.grid_rowconfigure(4, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Place the frames
    choose_compare_folder_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
    choose_input_folder_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
    similarity_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nw")
    input_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")  # Place input_frame
    compare_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")  # Place compare_frame

    # Create scrollable canvas in compare_frame
    compare_canvas = tk.Canvas(compare_frame, bg="#FFFFFF")
    compare_canvas.pack(side="left", fill="both", expand=True)

    # Add scrollbar to the canvas in compare_frame
    scrollbar = tk.Scrollbar(compare_frame, orient="vertical", command=compare_canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the canvas in compare_frame
    compare_canvas.configure(yscrollcommand=scrollbar.set)
    scrollable_frame = tk.Frame(compare_canvas)
    compare_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def update_scrollregion():
        compare_canvas.configure(scrollregion=compare_canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", lambda event: update_scrollregion())

    def create_compare_widgets():
        """Callback to create text widgets in compare frame."""
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        create_text_widgets_from_sentences(list_compare_folder, sentences_by_file_compare, scrollable_frame)

    # Create and place the "Choose compare folder" button
    choose_compare_folder_button = create_button_widget(choose_compare_folder_frame, "Choose compare folder", ("Arial", 12), "#FFFFFF", lambda: choose_folder(folder_path_label, False, create_compare_widgets))
    choose_compare_folder_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    # Create and place the "Choose input folder" button
    choose_input_folder_button = create_button_widget(choose_input_folder_frame, "Choose input folder", ("Arial", 12), "#FFFFFF", lambda: choose_folder(input_folder_path_label, True))
    choose_input_folder_button.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

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

    # Create and place the "Compare" button
    compare_button = create_button_widget(similarity_frame, "Compare", ("Arial", 12), "#FFFFFF", lambda: print(similarity_input.get()))
    compare_button.grid(row=2, column=0, padx=10, pady=10, sticky="nw")

    window.mainloop()

if __name__ == "__main__":
    main()
