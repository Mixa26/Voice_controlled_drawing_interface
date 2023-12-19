import tkinter as tk
import numpy as np
import sounddevice as sd
import librosa
import random
import keras
import soundfile as sf

shape = None
color = None
available_colors = ['blue', 'green', 'red', 'yellow']
canvas = None
voice_command = []
is_recording = False

model = keras.models.load_model('model.h5')

def draw_shapes(command):

    if command == 0:
        clear_screen()
    elif command == 1:
        shape = 1
        canvas.create_oval(200, 50, 300, 150, fill=color, outline="black")
        color = None
    elif command == 2:
        shape = 2
        canvas.create_rectangle(350, 50, 450, 150, fill=color, outline="black")
        color = None
    elif command == 3:
        clear_screen()
        color = available_colors[random.randint(len(available_colors))]
        draw_shapes(shape)
    else:
        shape = 4
        canvas.create_polygon(50, 150, 150, 150, 100, 50, fill=color, outline="black")
        color = None


def clear_screen():
    canvas.delete("all")

def start_audio_capture():
    global voice_command, is_recording
    voice_command = []
    is_recording = True
    stream = sd.InputStream(callback=audio_callback)
    stream.start()

def stop_audio_capture():
    global is_recording
    is_recording = False
    audio = np.concatenate(voice_command, axis=0)
    #audio = np.concatenate(audio, axis=0)
    sf.write("record.wav", audio, 44100)
    librosa.load("record.wav")
    print('majmune')
    #print(a[0])
    #librosa.feature.mfcc(y=a[0])
    #mfcc = extract_mfcc(a[0])[:,:80]
    #print(mfcc)
    #command = np.argmax(model.predict(np.expand_dims(mfcc), axis=0))


def audio_callback(indata, frames, time, status):
    if status:
        print('Error:', status)
    if is_recording:
        voice_command.append(indata.copy())

def extract_mfcc(audio, n_mfcc=13, n_fft=2048, hop_length=512):
    mfccs = librosa.feature.mfcc(y=audio, sr=None, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)
    return mfccs

root = tk.Tk()
root.title("Voice application demo")

canvas = tk.Canvas(root, width=500, height=300)
canvas.pack()

start_button = tk.Button(root, text="Start Recording", command=start_audio_capture)
start_button.pack(side=tk.LEFT, padx=10, pady=10)

stop_button = tk.Button(root, text="Stop Recording", command=stop_audio_capture)
stop_button.pack(side=tk.RIGHT, padx=10, pady=10)

root.mainloop()