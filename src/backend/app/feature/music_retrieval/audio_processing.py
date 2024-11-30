import librosa
import numpy as np
import os
from mido import MidiFile
import matplotlib.pyplot as plt

# PREPROCESS WAV
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
    
# PREPROCESS MIDI
def preprocess_midi(file_path):
    midi = MidiFile(file_path)
    pitch_data = []

    for track in midi.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                pitch_data.append(msg.note)
    return pitch_data

# APPLY SLIDING WINDOW
def apply_sliding_window(data, window, step):
    segments = []
    for i in range(0, len(data) + 1 - window, step):
        segment = data[i:i + window]
        segments.append(segment)
    return segments;

# MAIN AUDIO PROCESSING FUNCTION
def get_processed_audio(file_path):
    if file_path.endswith('.wav'):
        pitch_data = preprocess_wav(file_path)
    elif file_path.lower().endswith(('.mid', '.midi')):
        pitch_data = preprocess_midi(file_path)
    else:
        raise ValueError("Unsupported file format")

    # Windowing
    segments = apply_sliding_window(pitch_data, 40, 8)
    pitches = [p for segment in segments for p in segment if p > 0]
    if len(pitches) == 0:
        print("Pitches list is empty.")
        return pitch_data

    # Normalisasi Tempo
    mu = np.mean(pitches)
    sigma = np.std(pitches)
    
    if (sigma == 0):
        sigma = 1

    processed_pitch_data = []
    for p in pitch_data:
        if p > 0:
            normalized_value = (p - mu) / sigma
            processed_pitch_data.append(normalized_value)
        else:
            processed_pitch_data.append(0)
    return processed_pitch_data

# CREATE AND NORMALIZE HISTOGRAM
def create_and_normalize_histogram(data, num_bins, val_range = None):
    # Create
    if val_range is None:
        val_range = (0, num_bins)
    histogram, _ = np.histogram(data, bins=num_bins, range=val_range)
    
    # Normalize
    total = np.sum(histogram)
    if total > 0:
        return histogram / total
    else:
        print("Error Warning: Histogram sum 0 atau negatif")
        return histogram

# EXTRACT FEATURES
def extract_features(pitch_data):
    # ATB [0, 127]
    bins_atb = 128
    atb_normalized = create_and_normalize_histogram(pitch_data, bins_atb)


    # RTB [-127, 127] (selisih antara nada-nada berurutan)
    bins_rtb = 255
    for i in range(1, len(pitch_data)):
        rtb_data = pitch_data[i] - pitch_data[i - 1]
        rtb_normalized = create_and_normalize_histogram(rtb_data, bins_rtb, (-127, 127))
    
    # FTB [-127, 127] (selisih antara nada-nada dengan nada pertama)
    bins_ftb = 255
    if len(pitch_data > 0):
        for i in range(1, len(pitch_data)):
            first_tone = pitch_data[0]
            ftb_data = pitch_data[i] - first_tone
            ftb_normalized = create_and_normalize_histogram(ftb_data, bins_ftb, (-127, 127))
    else:
        ftb_normalized = np.zeros(255, dtype=float)

    # Gabung histogram menjadi 1 vektor
    vector_combined_features = np.concatenate((atb_normalized, rtb_normalized, ftb_normalized))

    return vector_combined_features

# GET COSINE SIMILARITY
def get_cosine_similarity(vector_A, vector_B):
    dot_product = np.dot(vector_A, vector_B)
    norm_vector_A = np.linalg.norm(vector_A)
    norm_vector_B = np.linalg.norm(vector_B)
    norm_product = norm_vector_A * norm_vector_B

    # check handle division by zero
    if norm_product == 0:
        return 0

    cosine_similarity = dot_product / norm_product
    return cosine_similarity

# MAIN
def main():
    # upload_audio_path = "src/backend/app/feature/music_retrieval/music_files/twinklemidi.mid"
    upload_audio_path = "test/music_files/twinklewav.wav"
    dataset_audio_path = "test//twinklemidi.mid"

    if (os.path.exists(upload_audio_path)) and (os.path.exists(dataset_audio_path)):
        print("File exists (upload):", os.path.exists(upload_audio_path))
        print("File exists (dataset):", os.path.exists(dataset_audio_path))
        
        # Preprocess wav/midi -> Get processed audio -> Extract features -> Get cosine similarity
        upload_processed_pitch_data = get_processed_audio(upload_audio_path)
        dataset_processed_pitch_data = get_processed_audio(dataset_audio_path)

        vector_upload = extract_features(upload_processed_pitch_data)
        vector_dataset = extract_features(dataset_processed_pitch_data)

        cosine_similarity = get_cosine_similarity(vector_upload, vector_dataset)
        print(f"Cosine Similarity: {cosine_similarity}")
    else:
        print(f"Gada Filenya")

# TESTING
if __name__ == "__main__":
    main()

