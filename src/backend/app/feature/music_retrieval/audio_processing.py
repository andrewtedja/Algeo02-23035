import librosa
import numpy as np
import os
from mido import MidiFile
import matplotlib.pyplot as plt

# Baca wav file, return list pitch data
def preprocess_wav(file_path):
    audio_data, sample_rate = librosa.load(file_path)
    pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sample_rate)

    # pitches & magnitude berupa 2D array
    pitch_data = []

    for frame in range(pitches.shape[1]):
        pitch = pitches[:, frame]
        if pitch.any():
            pitch_data.append(np.argmax(pitch))
        else:
            # pitch kosong
            pitch_data.append(0) 
    return pitch_data
    
# Baca midi file, return list pitch data
def preprocess_midi(file_path):
    midi = MidiFile(file_path)
    pitch_data = []

    for track in midi.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                pitch_data.append(msg.note)
    return pitch_data

# Bagi data menjadi segmen-segmen berdasarkan window dan step
def apply_sliding_window(data, window, step):
    segments = []
    for i in range(0, len(data) + 1 - window, step):
        segment = data[i:i + window]
        segments.append(segment)
    return segments;

def get_processed_audio(pitch_data):
    # Windowing
    pitches = apply_sliding_window(pitch_data, 40, 8)

    pitches = [p for p in pitches if p > 0]
    if len(pitches) == 0:
        print("Pitches list is empty.")
        return pitch_data

    # Normalisasi Tempo
    mu = np.mean(pitches)
    sigma = np.std(pitches)
    processed_pitch_data = []
    for p in pitch_data:
        if p > 0:
            processed_pitch_Data.append((p - mu) / sigma)
        else:
            processed_pitch_Data.append(0)
    return processed_pitch_Data




# TESTING
audio_file = "music_files/twinklewav.wav"

if os.path.exists(audio_file):
    print("File exists:", os.path.exists(audio_file))
    pitch_data = preprocess_wav(audio_file)
    processed_pitch_Data = get_processed_audio(pitch_data)

    print("Original Pitch Data:", pitch_data)
    print("Processed Pitch Data:", processed_pitch_Data)

    # Plot test
    plt.plot(pitch_data, label="Original Pitch")
    plt.plot(processed_pitch_Data, label="Normalized Pitch")
    plt.xlabel('Frame Index')
    plt.ylabel('Pitch Value')
    plt.title('Pitch Data Comparison')
    plt.legend()
    plt.show()

else:
    print(f"Gada Filenya")
