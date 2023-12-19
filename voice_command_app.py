import tkinter as tk
import numpy as np
import sounddevice as sd
import librosa
import random
import keras
import soundfile as sf
import threading

class AudioRecorded:
    def __init__(self):
        self.recording = False
        self.frames = []
    
    def start_recording(self):
        self.recording = True
        self.frames = []
        sd.default.samplerate = 44100
        sd.default.channels = 1

        def callback(indata, framse, time, status):
            if self.recording:
                self.frames.append(indata.copy())

        with sd.InputStream(callback=callback):
            sd.sleep(1000 * 2)
            self.stop_recording()
    
    def stop_recording(self):
        self.recording = False
    
    def save_recording(self, filename):
        if self.frames:
            audio_data = np.concatenate(self.frames, axis=0)
            sf.write(filename, audio_data, samplerate=44100)

class VoiceCommandApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice commander")
        self.command = None
        self.commands = ['izbrisi', 'krug', 'kvadrat', 'oboji', 'trougao']
        self.shape = None
        self.color = 'white'
        self.available_colors = ['blue', 'green', 'red', 'yellow']
        self.model = keras.models.load_model('model.h5')

        self.canvas = tk.Canvas(self.root, width=400, height=200, bg="white")
        self.canvas.pack(pady=10)

        self.recorder = AudioRecorded()

        self.start_button = tk.Button(root, text="Voice command", command=self.start_recording)
        self.start_button.pack(side=['left'], pady=10, padx=50)

    def start_recording(self):
        self.recording_thread = threading.Thread(target=self.recorder.start_recording)
        self.recording_thread.start()

        self.root.after(2000, self.stop_recording)

    def stop_recording(self):
        self.recorder.stop_recording()
        self.recording_thread.join()
        #self.recorder.save_recording('record.wav')
        mfcc = librosa.feature.mfcc(y=np.squeeze(np.concatenate(self.recorder.frames)), sr=44100, n_mfcc=13, n_fft=2048, hop_length=512)
        prediction = self.model.predict(np.expand_dims(mfcc[:,:80], axis=0))
        print("Predictions for\n", self.commands)
        print(prediction)                                        
        command = np.argmax(prediction)
        print("Predicted command: ", self.commands[command])
        self.draw_shapes(command)

    def draw_shapes(self, command):
        if command == 0:
            self.clear_screen()
            self.shape = None
            self.color = 'white'
        elif command == 1:
            self.clear_screen()
            self.shape = 1
            self.canvas.create_oval(150, 50, 250, 150, fill=self.color, outline="black")
            self.color = 'white'
        elif command == 2:
            self.clear_screen()
            self.shape = 2
            self.canvas.create_rectangle(150, 50, 250, 150, fill=self.color, outline="black")
            self.color = 'white'
        elif command == 3:
            self.clear_screen()
            self.color = self.available_colors[random.randint(0, len(self.available_colors)-1)]
            if self.shape != None:
                self.draw_shapes(self.shape)
            else:
                self.color = 'white'
        else:
            self.clear_screen()
            self.shape = 4
            self.canvas.create_polygon(150, 150, 250, 150, 200, 50, fill=self.color, outline="black")
            self.color = 'white'

    def clear_screen(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300")
    app = VoiceCommandApp(root)
    root.mainloop()