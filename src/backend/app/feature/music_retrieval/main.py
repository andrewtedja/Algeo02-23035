import os
# import time

from src.backend.app.feature.music_retrieval.feature_extraction import extract_features
from src.backend.app.feature.music_retrieval.similarity import get_cosine_similarity
from src.backend.app.feature.music_retrieval.audio_processing import get_processed_audio

DIR = "backend/app/data/dataset/"
AUD_DIR = "backend/app/data/dataset/audio/"


class AudioData:
    def __init__(self, filename, type=None):
        if (type == "q"):
            self.dir = DIR + "query/"
        else:
            self.dir = AUD_DIR
        self.filename = filename
        self.pitch_data = None
        self.atb = None
        self.rtb = None
        self.ftb = None
        self.similarity = None

    def extract_features(self):
        self.pitch_data = get_processed_audio(self.dir + self.filename)
        self.atb, self.rtb, self.ftb = extract_features(self.pitch_data)

    def calculate_similarity(self, query: 'AudioData'):
        # Hitung cosine similarity ATB, FTB, FTB terpisah
        atb_query, rtb_query, ftb_query = query.atb, query.rtb, query.ftb
        atb_dataset, rtb_dataset, ftb_dataset = self.atb, self.rtb, self.ftb

        similarity_atb = get_cosine_similarity(atb_query, atb_dataset)
        similarity_rtb = get_cosine_similarity(rtb_query, rtb_dataset)
        similarity_ftb = get_cosine_similarity(ftb_query, ftb_dataset)

        # Rata-rata cosine similarity
        avg_similarity = (similarity_atb + similarity_rtb + similarity_ftb) / 3
        self.similarity = float(avg_similarity)

    def __str__(self):
        # return '\n'.join(f"{key}: {value}" for key, value in self.__dict__.items())
        return f"File: {self.filename}\nATB: {self.atb}\nRTB: {self.rtb}\nFTB: {self.ftb}\n"


# Memproses data-data gambar dataset
def save_dataset_similarity(query_path, dataset_folder):
    similarity_list = []  # Bentuk tuple
    query_name = query_path.rsplit("/", 1)[-1]
    query = AudioData(query_name, 'q')
    query.extract_features()
    if (os.path.exists(query_path)) and (os.path.exists(dataset_folder)):
        # Check if file exists
        print(f"Query file exists {query_path}:", os.path.exists(query_path))
        print(f"Folder exists {dataset_folder}):", os.path.exists(dataset_folder))

        # Testing
        for dataset_file in os.listdir(dataset_folder):
            dataset_path = os.path.join(dataset_folder, dataset_file)

            if os.path.exists(dataset_path):
                print(f"Dataset file exists ({dataset_file}):", os.path.exists(dataset_path))  # Kalo dah jadi ilangin
                dataset = AudioData(dataset_file)
                dataset.extract_features()
                dataset.calculate_similarity(query)
                similarity_list.append((dataset_file, dataset.similarity))
            else:
                print("Gada Filenya")
    else:
        print("Gada Foldernya")

    return similarity_list


def get_similar_file(similarity_list):
    similarity_list.sort(key=lambda x: x[1], reverse=True)
    if (similarity_list):
        most_similar_file, cosine_similarity = similarity_list[0]
        return most_similar_file, cosine_similarity


# Main
def main():
    query_path = "backend/app/feature/music_retrieval/query/query.mid"
    # dataset_folder = "test/music_dataset"

    # Testing
    dataset_similar = save_dataset_similarity(query_path, AUD_DIR)
    most_similar_file, cosine_similarity = get_similar_file(dataset_similar)

    print(f"Dataset Similarity: {dataset_similar}")
    print(f"Most similar file: {most_similar_file}")
    print(f"Cosine similarity: {cosine_similarity}")


if __name__ == "__main__":
    main()
