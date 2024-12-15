import numpy as np
import os

from audio_load import preprocess_midi, preprocess_wav
from feature_extraction import extract_features
from similarity import calculate_similarity
from audio_processing import get_processed_audio

AUD_DIR = "backend/app/data/dataset/audio"


class AudioData:
    def __init__(self, filename):
        self.filename = filename
        self.pitch_data = get_processed_audio(AUD_DIR + filename)
        self.atb = 


# Memproses data-data gambar dataset
def save_dataset_similarity(query_path, dataset_folder):
    similarity_list = []  # Bentuk tuple
    if (os.path.exists(query_path)) and (os.path.exists(dataset_folder)):
        # Check if file exists
        print(f"Query file exists {query_path}:", os.path.exists(query_path))
        print(f"Folder exists {dataset_folder}):", os.path.exists(dataset_folder))

        # Testing
        for dataset_file in os.listdir(dataset_folder):
            dataset_path = os.path.join(dataset_folder, dataset_file)

            if os.path.exists(dataset_path):
                print(f"Dataset file exists ({dataset_file}):", os.path.exists(dataset_path)) # Kalo dah jadi semua ilangin
                query_pitch = get_processed_audio(query_path)
                dataset_pitch = get_processed_audio(dataset_path)

                cosine_similarity = calculate_similarity(query_pitch, dataset_pitch)
                similarity_list.append((dataset_file, cosine_similarity))
            else:
                print("Gada Filenya")
    else:
        print(f"Gada Foldernya")

    return similarity_list

def get_similar_file(similarity_list):
    similarity_list.sort(key=lambda x: x[1], reverse=True)
    if (similarity_list):
        most_similar_file, cosine_similarity = similarity_list[0]
        return most_similar_file, cosine_similarity

# Main
def main():
    # query_path = "src/backend/app/feature/music_retrieval/music_files/twinklemidi.mid"
    query_path = "test/music_query/Speaker_0000_00001.wav"
    dataset_folder = "test/music_dataset"

    # Testing
    dataset_similar = save_dataset_similarity(query_path, dataset_folder)
    most_similar_file, cosine_similarity = get_similar_file(dataset_similar)

    print(f"Dataset Similarity: {dataset_similar}")
    print(f"Most similar file: {most_similar_file}")
    print(f"Cosine similarity: {cosine_similarity}")

if __name__ == "__main__":
    main()
