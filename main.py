import os
import tkinter as tk
from tkinter import filedialog
import imageio
import subprocess
from datetime import datetime

def clear_folder(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def clear_jpg_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

def extract_frames(video_path, output_folder):
    reader = imageio.get_reader(video_path)

    clear_folder('out')
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    for i, frame in enumerate(reader):
        filename = os.path.join(output_folder, f"frame-{i:04d}.png")
        imageio.imwrite(filename, frame)



def combine_frames_to_video(input_folder, output_video):

    try:
        clear_jpg_files('out')
    except:
        pass

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_video = f"video_{timestamp}.mp4"
    # Comando para combinar los frames usando ffmpeg
    cmd = [
        'ffmpeg',
        '-r', '8',  # Tasa de 8 fps
        '-f', 'image2',
        '-i', os.path.join(input_folder, 'frame-%04d-0000.png'),
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        output_video
    ]
    
    subprocess.run(cmd)


def load_video():
    filepath = filedialog.askopenfilename(title="Select a Video", filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))
    if filepath:
        extract_frames(filepath, 'in')

root = tk.Tk()
root.geometry("500x300")
root.title("Extract and Combine Frames")

load_button = tk.Button(root, text="Load Video", command=load_video)
load_button.pack(pady=20)

combine_button = tk.Button(root, text="Combine Frames", command=lambda: combine_frames_to_video('out', 'video_salida.mp4'))
combine_button.pack(pady=20)

root.mainloop()
