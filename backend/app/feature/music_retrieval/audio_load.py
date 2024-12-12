import librosa
import numpy as np
import os
from mido import MidiFile

# Convert wav to pitch data
def preprocess_wav(file_path):
    audio_data, sample_rate = librosa.load(file_path)

    # Get pitches from wav file
    pitches = librosa.yin(audio_data, fmin=librosa.note_to_hz('C1'), fmax=librosa.note_to_hz('C8'), sr=sample_rate)

    # Convert pitch (Hz) to MIDI note numbers
    pitch_data = []
    for pitch in pitches:
        if pitch > 0: 
            pitch_data.append(int(librosa.hz_to_midi(pitch)))
        else:
            pitch_data.append(0)  
    return pitch_data
    
# Convert midi to pitch data
def preprocess_midi(file_path):
    midi = MidiFile(file_path)
    pitch_data = []

    for track in midi.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                pitch_data.append(msg.note)
    return pitch_data



