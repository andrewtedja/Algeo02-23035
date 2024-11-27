import librosa
import numpy as np
import os
from mido import MidiFile
import matplotlib.pyplot as plt

# Baca wav file, return list pitch contour
def preprocess_wav(file_path):
    audio_data, sample_rate = librosa.load(file_path)
    pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sample_rate)

    # pitches & magnitude berupa 2D array
    pitch_contour = []

    for frame in range(pitches.shape[1]):
        pitch = pitches[:, frame]
        if pitch.any():
            pitch_contour.append(np.argmax(pitch))
        else:
            # pitch kosong
            pitch_contour.append(0) 
    return pitch_contour
    
# Baca midi file, return list of msg/pitch values (0-127)
def preprocess_midi(file_path):
    midi = MidiFile(file_path)
    melody = []

    for track in midi.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                melody.append(msg.note)
    return melody

def audio_processing(pitch_contour):
    pitches = [p for p in pitch_contour if p > 0]
    if len(pitches) == 0:
        print("pitch contour empty cek again")
        return pitch_contour
    
    # Cari NP
    mu = np.mean(pitches)
    sigma = np.std(pitches)

    # Normalisasi tempo
    processed_contour = []
    for p in pitch_contour:
        if p > 0:
            processed_contour.append((p - mu) / sigma)
        else:
            processed_contour.append(0)
    return processed_contour


# TESTING
audio_file = "music_files/twinklewav.wav"

if os.path.exists(audio_file):
    print("File exists:", os.path.exists(audio_file))
    pitch_contour = preprocess_wav(audio_file)
    processed_contour = audio_processing(pitch_contour)

    print("Original Pitch Contour:", pitch_contour)
    print("Processed Pitch Contour:", processed_contour)

    # Plot test
    plt.plot(pitch_contour, label="Original Contour")
    plt.plot(processed_contour, label="Normalized Contour")
    plt.xlabel('Frame Index')
    plt.ylabel('Pitch Value')
    plt.title('Pitch Contour Comparison')
    plt.legend()
    plt.show()

else:
    print(f"Gada Filenya")
