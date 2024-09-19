import tkinter as tk
from tkinter import ttk, filedialog
import os
import subprocess
import threading
import shutil
import uuid
from PIL import Image, ImageTk
import time

file_queue = []
temp_directory = "C:\\soundfiles"  


os.makedirs(temp_directory, exist_ok=True)


def browse_input_file():
    filenames = filedialog.askopenfilenames(filetypes=(
        ("MP3 Files", "*.mp3"), ("MP4 Files", "*.mp4"), ("AIFF Files", "*.aiff"), ("WAV Files", "*.wav"),
        ("All Files", "*.*")))
    for filename in filenames:
        if filename:
            add_file_to_queue(filename)


def generate_unique_filename(original_filename):
    file_extension = os.path.splitext(original_filename)[1]
    unique_filename = f"soundfile_{uuid.uuid4().hex}{file_extension}"
    return unique_filename


def add_file_to_queue(filename):
    original_filename = os.path.basename(filename)
    new_filename = os.path.join(temp_directory, generate_unique_filename(original_filename))
    shutil.copy(filename, new_filename)

    file_queue.append((original_filename, new_filename))
    file_listbox.insert(tk.END, original_filename.replace(" ", "-"))  

def clear_choices():
    output_entry.delete(0, tk.END)
    language_var.set("")
    translate_var.set(False)
    file_queue.clear()
    file_listbox.delete(0, tk.END)
    duration_label.config(text="") 
    console.delete(0, tk.END)


def browse_output_folder():
    foldername = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(tk.END, foldername)


def transcribe():
    running_indices = []
    start_time_total = time.time()

    while file_queue:
        original_filename, filename = file_queue.pop(0)
        file_listbox.delete(0)

        start_time = time.time()
        running_index = console.size()
        console.insert(tk.END, f"Running {original_filename}...\n")
        running_indices.append(running_index)

        try:
            transcribe_file(original_filename, filename)
        except Exception as e:
            console.insert(tk.END, f"Error processing {original_filename}: {str(e)}\n")
        end_time = time.time()
        duration = (end_time - start_time) / 60

        console.delete(running_indices.pop(0))
        console.insert(tk.END, f"Done {original_filename} - Time taken: {duration:.2f} minutes\n")
        root.update_idletasks() 

    end_time_total = time.time()
    total_duration = (end_time_total - start_time_total) / 60
    console.insert(tk.END, f"Total time taken for all files: {total_duration:.2f} minutes\n")

    shutil.rmtree(temp_directory)


def transcribe_file(original_filename, input_file):
    output_folder = output_entry.get()
    language = language_var.get()
    task = "translate" if translate_var.get() else "transcribe"
    command = f'whisper {input_file} --model large --language {language} --task {task} --output_dir {output_folder}'
    subprocess.run(command, shell=True)

    output_folder_path = os.path.join(output_folder, os.path.splitext(original_filename)[0].replace(" ", "_"))
    os.makedirs(output_folder_path, exist_ok=True)

    for filename in os.listdir(output_folder):
        if not os.path.isdir(os.path.join(output_folder, filename)):
            shutil.move(os.path.join(output_folder, filename), output_folder_path)

    for filename in os.listdir(output_folder_path):
        file_extension = os.path.splitext(filename)[1]
        new_filename = original_filename.replace('.mp3', '').replace('.mp4', '').replace('.aiff', '').replace('.wav', '').replace(" ", "-") + file_extension 
        source = os.path.join(output_folder_path, filename)
        destination = os.path.join(output_folder_path, new_filename)
        if source != destination:
            counter = 1
            while os.path.exists(destination):
                new_filename = original_filename.replace('.mp3', '').replace('.mp4', '').replace('.aiff', '').replace('.wav', '').replace(" ", "-") + f'_{counter}{file_extension}'  
                destination = os.path.join(output_folder_path, new_filename)
                counter += 1
            os.rename(source, destination)

    if os.path.exists(input_file):
        os.remove(input_file)


def start_transcribe_thread():
    transcribe_thread = threading.Thread(target=transcribe)
    transcribe_thread.start()


def on_language_select(event):
    selected_language = language_combobox.get()
    language_var.set(selected_language)


def on_language_typing(event):

    cursor_position = language_combobox.index(tk.INSERT)

    filter_language_options(language_combobox.get())


    if language_combobox.get():
        language_combobox.event_generate('<Down>')


    language_combobox.icursor(cursor_position)


def filter_language_options(text):
    filtered_options = [option for option in language_options if text.lower() in option.lower()]
    language_combobox['values'] = filtered_options


root = tk.Tk()
root.title("WhispLUr")

root.minsize(500, 600)

icon_path = "lu.ico"
if os.path.exists(icon_path):
    root.iconbitmap(default=icon_path)

img = Image.open("lu.png")
img = img.resize((200, 230), Image.LANCZOS)
img = ImageTk.PhotoImage(img)
image_label = tk.Label(root, image=img)
image_label.pack(pady=(20, 0))

input_button = tk.Button(root, text="Upload Files", command=browse_input_file)
input_button.pack(pady=(30, 30))

output_entry = tk.Entry(root, width=70)
output_entry.pack()
output_button = tk.Button(root, text="Choose Output Folder", command=browse_output_folder)
output_button.pack(pady=(0, 30))

language_var = tk.StringVar(root)
language_var.set("")
language_options = ['Afrikaans', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Assamese', 'Azerbaijani', 'Bashkir',
                    'Basque', 'Belarusian', 'Bengali', 'Bosnian', 'Breton', 'Bulgarian', 'Burmese', 'Cantonese',
                    'Castilian', 'Catalan', 'Chinese', 'Croatian', 'Czech', 'Danish', 'Dutch', 'English', 'Estonian',
                    'Faroese', 'Finnish', 'Flemish', 'French', 'Galician', 'Georgian', 'German', 'Greek', 'Gujarati',
                    'Haitian', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hungarian', 'Icelandic',
                    'Indonesian', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Korean', 'Lao',
                    'Latin', 'Latvian', 'Letzeburgesch', 'Lingala', 'Lithuanian', 'Luxembourgish', 'Macedonian',
                    'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Mandarin', 'Maori', 'Marathi', 'Moldavian',
                    'Moldovan', 'Mongolian', 'Myanmar', 'Nepali', 'Norwegian', 'Nynorsk', 'Occitan', 'Panjabi',
                    'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Pushto', 'Romanian', 'Russian', 'Sanskrit',
                    'Serbian', 'Shona', 'Sindhi', 'Sinhala', 'Sinhalese', 'Slovak', 'Slovenian', 'Somali', 'Spanish',
                    'Sundanese', 'Swahili', 'Swedish', 'Tagalog', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai',
                    'Tibetan', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uzbek', 'Valencian', 'Vietnamese', 'Welsh',
                    'Yiddish', 'Yoruba']
language_combobox = ttk.Combobox(root, textvariable=language_var, values=language_options, width=67)
language_combobox.pack(pady=5)
language_combobox.bind("<<ComboboxSelected>>", on_language_select)
language_combobox.bind("<KeyRelease>", on_language_typing)

translate_var = tk.BooleanVar()
translate_check = tk.Checkbutton(root, text="Translate to English", variable=translate_var)
translate_check.pack(pady=5)

console = tk.Listbox(root, state='normal', width=70, height=7)
console.pack(pady=5)

file_listbox = tk.Listbox(root, width=70, height=10)
file_listbox.pack(pady=5)

transcribe_button = tk.Button(root, text="Transcribe", command=start_transcribe_thread)
transcribe_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear", command=clear_choices)
clear_button.pack(pady=5)

duration_label = tk.Label(root, text="", wraplength=400) 
duration_label.pack(pady=10)

root.mainloop()
