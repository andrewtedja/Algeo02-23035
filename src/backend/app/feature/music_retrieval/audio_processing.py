import librosa
import numpy as np
import os
from mido import MidiFile
import matplotlib.pyplot as plt

from audio_load import preprocess_midi, preprocess_wav

# Windowing
def apply_sliding_window(data, window, step): 
    segments = []
    
    for i in range(0, len(data) + 1 - window, step):
        segment = data[i:i + window]
        segments.append(segment)
    return segments;

# Audio Processing
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

    # # Normalisasi Pitch (Opsional)
    # mu = np.mean(pitches)
    # sigma = np.std(pitches)
    
    # if (sigma == 0):
    #     sigma = 1

    # processed_pitch_data = []
    # for p in pitch_data:
    #     if p > 0:
    #         normalized_value = (p - mu) / sigma
    #         processed_pitch_data.append(normalized_value)
    #     else:
    #         processed_pitch_data.append(0)
    return segments

# Create Histogram and Normalize
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

# Extract Features
def extract_features(pitch_data):
    
    # ATB [0, 127]
    bins_atb = 128
    atb_normalized = create_and_normalize_histogram(pitch_data, bins_atb)

    # RTB [-127, 127] (selisih antara nada-nada berurutan)
    bins_rtb = 255
    rtb_data = [pitch_data[i] - pitch_data[i-1] for i in range(1, len(pitch_data))]
    rtb_normalized = create_and_normalize_histogram(rtb_data, bins_rtb, (-127, 127))
    
    # FTB [-127, 127] (selisih antara nada-nada dengan nada pertama)
    bins_ftb = 255
    if len(pitch_data) > 0:
        ftb_data = [pitch_data[i] - pitch_data[0] for i in range(1, len(pitch_data))]
        ftb_normalized = create_and_normalize_histogram(ftb_data, bins_ftb, (-127, 127))
    else:
        ftb_normalized = np.zeros(255, dtype=float)

    # Gabung histogram menjadi 1 vektor
    vector_combined_features = np.concatenate((atb_normalized, rtb_normalized, ftb_normalized))

    return vector_combined_features

# Cosine Similarity
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

# Memproses data-data gambar dataset
def save_dataset_similarity(query_path, dataset_folder):
    dataset_similarity_list = [] # Bentuk tuple
    if (os.path.exists(query_path)) and (os.path.exists(dataset_folder)):
        # Check if file exists
        print(f"Query file exists {query_path}:", os.path.exists(query_path))
        print(f"Folder exists {dataset_folder}):", os.path.exists(dataset_folder))
        
        # Testing
        for dataset_file in os.listdir(dataset_folder):
            dataset_path = os.path.join(dataset_folder, dataset_file)

            if os.path.exists(dataset_path):
                print(f"Dataset file exists ({dataset_file}):", os.path.exists(dataset_path))

                # Preprocess wav/midi -> Get processed audio -> Extract features -> Get cosine similarity
                query_processed_pitch_data = get_processed_audio(query_path)
                dataset_processed_pitch_data = get_processed_audio(dataset_path)

                vector_query = extract_features(query_processed_pitch_data)
                vector_dataset = extract_features(dataset_processed_pitch_data)
                cosine_similarity = get_cosine_similarity(vector_query, vector_dataset)

                dataset_similarity_list.append((dataset_file, cosine_similarity))
            else:
                print("Gada Filenya")
    else:
        print(f"Gada Foldernya")

    return dataset_similarity_list

def get_similar_file(dataset_similarity_list):
    dataset_similarity_list.sort(key=lambda x: x[1], reverse=True)
    if (dataset_similarity_list):
        most_similar_file, cosine_similarity = dataset_similarity_list[0]
        return most_similar_file, cosine_similarity

# Main
def main():
    # query_path = "src/backend/app/feature/music_retrieval/music_files/twinklemidi.mid"
    query_path = "test/music_query/Speaker_0000_00000.wav"
    dataset_folder = "test/music_dataset"

    # Testing
    dataset_similar = save_dataset_similarity(query_path, dataset_folder)
    most_similar_file, cosine_similarity = get_similar_file(dataset_similar)

    print(f"Dataset Similarity: {dataset_similar}")
    print(f"Most similar file: {most_similar_file}")
    print(f"Cosine similarity: {cosine_similarity}")

if __name__ == "__main__":
    main()
