import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import os
import subprocess
import threading
import shutil
from PIL import Image, ImageTk

original_filename = ""

def browse_input_file():
    global original_filename
    filename = filedialog.askopenfilename(filetypes=(("MP3 Files", "*.mp3"), ("MP4 Files", "*.mp4"), ("All Files", "*.*")))
    if filename:
        # sparar namnet som den först hade
        original_filename = os.path.basename(filename)
        if not (original_filename == "soundfile.mp3" or original_filename == "soundfile.mp4"):
            new_filename = os.path.join(os.path.dirname(filename), "soundfile" + os.path.splitext(original_filename)[1])
            shutil.copy(filename, new_filename)
            filename = new_filename
        input_entry.delete(0, tk.END)
        input_entry.insert(tk.END, filename)

def clear_choices():
    input_entry.delete(0, tk.END)
    output_entry.delete(0, tk.END)
    model_var.set("Choose Model")
    language_var.set("Spoken Language")
    translate_var.set(False)

def browse_output_folder():
    foldername = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(tk.END, foldername)

def transcribe():
    global original_filename
    console.delete('1.0', tk.END)
    input_file = input_entry.get()
    output_folder = output_entry.get()
    model = model_var.get()
    language = language_var.get()
    task = "translate" if translate_var.get() else "transcribe"
    console.insert(tk.END, "Running...")  # säger när den börjar
    command = f'whisper {input_file} --model {model} --language {language} --task {task} --output_dir {output_folder}'
    subprocess.run(command, shell=True)
    console.delete('1.0', tk.END)
    print("Done!")  # säger när den ä klar

    # gör en mapp
    output_folder_path = os.path.join(output_folder, original_filename.replace('.mp3', '').replace('.mp4', ''))
    os.makedirs(output_folder_path, exist_ok=True)

    # flyttar filerna till mappen
    for filename in os.listdir(output_folder):
        if not os.path.isdir(os.path.join(output_folder, filename)):
            shutil.move(os.path.join(output_folder, filename), output_folder_path)

    # bytar namn till de dem var från början
    for filename in os.listdir(output_folder_path):
        file_extension = os.path.splitext(filename)[1]
        new_filename = original_filename.replace('.mp3', '').replace('.mp4', '') + file_extension
        source = os.path.join(output_folder_path, filename)
        destination = os.path.join(output_folder_path, new_filename)
        if source != destination:
            counter = 1
            while os.path.exists(destination):

                new_filename = original_filename.replace('.mp3', '').replace('.mp4', '') + f'_{counter}{file_extension}'
                destination = os.path.join(output_folder_path, new_filename)
                counter += 1
            os.rename(source, destination)

    # tar bort soundfile.mp3 eller soundfile.mp4
    if os.path.exists(input_file):
        os.remove(input_file)
    console.insert(tk.END, 'Done')

def start_transcribe_thread():
    transcribe_thread = threading.Thread(target=transcribe)
    transcribe_thread.start()

def on_language_select(event):
    selected_language = language_combobox.get()
    language_var.set(selected_language)

def on_language_typing(event):
    filter_language_options(language_combobox.get())

def filter_language_options(text):
    filtered_options = [option for option in language_options if text.lower() in option.lower()]
    language_combobox['values'] = filtered_options

root = tk.Tk()
root.title("WhispLUr")

icon_path = "lu.ico"
if os.path.exists(icon_path):
    root.iconbitmap(default=icon_path)

img = Image.open("lu.png")
img = img.resize((200, 230), Image.LANCZOS)  # anpassar storleken lite
img = ImageTk.PhotoImage(img)
image_label = tk.Label(root, image=img)
image_label.pack()

input_entry = tk.Entry(root, width=50)
input_entry.pack()
input_button = tk.Button(root, text="Choose File", command=browse_input_file)
input_button.pack(pady=(0, 30))

output_entry = tk.Entry(root, width=50)
output_entry.pack()
output_button = tk.Button(root, text="Choose Output Folder", command=browse_output_folder)
output_button.pack(pady=(0, 30))

model_var = tk.StringVar(root)
model_var.set("Choose Model") # väljer vilken bas modell
model_options = ["tiny", "base", "small", "medium", "large"]
model_menu = tk.OptionMenu(root, model_var, *model_options)
model_menu.pack(pady=5)

language_var = tk.StringVar(root)
language_var.set("Spoken Language") # bas språk
language_options = ['Afrikaans', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Assamese', 'Azerbaijani', 'Bashkir', 'Basque', 'Belarusian', 'Bengali', 'Bosnian', 'Breton', 'Bulgarian', 'Burmese', 'Cantonese', 'Castilian', 'Catalan', 'Chinese', 'Croatian', 'Czech', 'Danish', 'Dutch', 'English', 'Estonian', 'Faroese', 'Finnish', 'Flemish', 'French', 'Galician', 'Georgian', 'German', 'Greek', 'Gujarati', 'Haitian', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hungarian', 'Icelandic', 'Indonesian', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Korean', 'Lao', 'Latin', 'Latvian', 'Letzeburgesch', 'Lingala', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Mandarin', 'Maori', 'Marathi', 'Moldavian', 'Moldovan', 'Mongolian', 'Myanmar', 'Nepali', 'Norwegian', 'Nynorsk', 'Occitan', 'Panjabi', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Pushto', 'Romanian', 'Russian', 'Sanskrit', 'Serbian', 'Shona', 'Sindhi', 'Sinhala', 'Sinhalese', 'Slovak', 'Slovenian', 'Somali', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tagalog', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tibetan', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uzbek', 'Valencian', 'Vietnamese', 'Welsh', 'Yiddish', 'Yoruba']
language_combobox = ttk.Combobox(root, textvariable=language_var, values=language_options)
language_combobox.pack(pady=5)
language_combobox.bind("<<ComboboxSelected>>", on_language_select)
language_combobox.bind("<KeyRelease>", on_language_typing)

translate_var = tk.BooleanVar()
translate_check = tk.Checkbutton(root, text="Translate to English", variable=translate_var)
translate_check.pack(pady=5)

console = scrolledtext.ScrolledText(root, state='normal', width=10, height=2)
console.pack()

transcribe_button = tk.Button(root, text="Transcribe", command=start_transcribe_thread)
transcribe_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear", command=clear_choices)
clear_button.pack(pady=5)

root.mainloop()
