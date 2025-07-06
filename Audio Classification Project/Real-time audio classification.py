import tkinter as tk
from tkinter import messagebox
import numpy as np
import librosa
import sounddevice as sd
from tensorflow.keras.models import load_model
import time

# Load the trained model
model = load_model("C:/Users/DELL/Downloads/Introduction to Neural Networks/Projects/UrbanSound8K_model.h5")

# Define class labels
class_labels = [
    "air_conditioner", "car_horn", "children_playing", "dog_bark",
    "drilling", "engine_idling", "gun_shot", "jackhammer",
    "siren", "street_music"
]

def extract_features_from_array(audio, sr=22050):
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    return np.mean(mfcc.T, axis=0)

def record_and_predict():
    try:
        duration = 2  # seconds
        sr = 22050

        # Update GUI to show "Recording..." and start countdown
        result_label.config(text="Recording...", fg="red")
        for i in range(duration, 0, -1):
            countdown_label.config(text=f"{i} sec left")
            root.update()
            time.sleep(1)
        countdown_label.config(text="Recording complete")

        # Record audio
        audio = sd.rec(int(duration * sr), samplerate=sr, channels=1)
        sd.wait()
        audio = audio.flatten()

        # Extract features and predict
        mfcc = extract_features_from_array(audio, sr)
        mfcc = (mfcc - np.mean(mfcc)) / np.std(mfcc)
        mfcc = mfcc.reshape(1, 40, 1)

        prediction = model.predict(mfcc)
        predicted_index = np.argmax(prediction)
        confidence = np.max(prediction)

        label = class_labels[predicted_index]
        result_label.config(text=f"Predicted: {label} ({confidence:.2f})", fg="green")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Real-Time Sound Classifier")

tk.Label(root, text="Click the button to record and classify sound").pack(pady=10)
tk.Button(root, text="Record & Predict", command=record_and_predict).pack(pady=10)

countdown_label = tk.Label(root, text="", font=("Arial", 12))
countdown_label.pack()

result_label = tk.Label(root, text="", font=("Arial", 14), fg="blue")
result_label.pack(pady=20)

root.mainloop()
