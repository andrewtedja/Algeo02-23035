import sqlite3 as SQL
import backend.app.feature.album_finder.image_processing as IMG
import backend.app.feature.music_retrieval.main as MSC
import backend.app.data.mapper as MAP
import numpy as np
import os
import time
import json
# DI RUN DARI ROOT (src)

# NGECEK DB
# /mnt/d/RaFa/Main/School/ITB/Kuliah 4 Tahun/Sem 3/Algeo/Tubes/Algeo02-23035/src/backend/app/data


DB_NAME = "backend/app/data/data.db"
DIR = "backend/app/data/dataset/"
DATADIR = "backend/app/data/"
IMG_DIR = "backend/app/data/dataset/image"
AUD_DIR = "backend/app/data/dataset/audio"


# Menyimpan semua data sekaligus
class ImageDataset:
    def __init__(self):
        self.dataset = None
        self.Uk = None
        self.pixel_means = None

    def load(self):
        self.dataset, self.Uk, self.pixel_means = load_and_proccess_image_dataset()


class AudioDataset:
    def __init__(self):
        self.dataset = None

    def load(self):
        self.dataset = load_and_proccess_audio_dataset()


# Dipanggil saat upload dataset
def load_and_proccess_image_dataset() -> tuple[list[IMG.ImageData], list, IMG.Vector]:
    dataset = IMG.load_dataset(IMG_DIR)
    pixel_means = IMG.get_pixel_means(dataset)
    IMG.standardize_images(dataset, pixel_means)
    Uk = IMG.principal_component_analysis_dataset(dataset)

    return dataset, Uk, pixel_means


def load_and_proccess_audio_dataset() -> list[MSC.AudioData]:
    audio_dataset = []
    for filename in os.listdir(AUD_DIR):
        if filename.endswith((".mid", ".wav")):
            audio_file = MSC.AudioData(filename)
            audio_file.extract_features()
            audio_dataset.append(audio_file)
    return audio_dataset


def matrix_buffering(matrix: list):
    buffer = IMG.io.BytesIO()
    np.save(buffer, matrix)
    return buffer.getvalue()


def create_tables() -> None:
    # CLEAR TABLE
    conn = SQL.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS image_dataset')
    cursor.execute('DROP TABLE IF EXISTS image_matrix')
    cursor.execute('DROP TABLE IF EXISTS audio_dataset')

    cursor.execute('''
    CREATE TABLE image_dataset (
        filename TEXT PRIMARY KEY NOT NULL,
        pixels BLOB NOT NULL,
        pca BLOB NOT NULL)
''')
    # Filename nanti dipake untuk nyimpen nama .zip?( kalo bukan .zip?)
    cursor.execute('''
    CREATE TABLE image_matrix (
        Uk_matrix BLOB NOT NULL,
        pixel_means BLOB NOT NULL)
''')
    cursor.execute('''
    CREATE TABLE audio_dataset (
        filename TEXT PRIMARY KEY,
        atb BLOB NOT NULL,
        rtb BLOB NOT NULL,
        ftb BLOB NOT NULL)
''')
    cursor.close()


# def save_to_database(dataset: list[IMG.ImageData], Uk: IMG.Matrix, pixel_means: IMG.Vector) -> None:  # noqa
def save_image_to_database() -> float:  # return runtime
    start = time.time()

    conn = SQL.connect(DB_NAME)
    cursor = conn.cursor()

    data = ImageDataset()
    data.load()

    dataset = data.dataset
    Uk = data.Uk
    pixel_means = data.pixel_means

    for image in dataset:
        filename = image.filename
        pixels = image.compress_pixels()
        pca = matrix_buffering(image.pca)
        cursor.execute(
            "INSERT INTO image_dataset (filename, pixels, pca) VALUES (?, ?, ?)",
            (filename, pixels, pca)
        )

    cursor.execute("INSERT INTO image_matrix (Uk_matrix, pixel_means) VALUES (?, ?)",
                   (matrix_buffering(Uk), matrix_buffering(pixel_means)))
    conn.commit()
    conn.close()
    return (time.time() - start)


def save_audio_to_database() -> float:
    start = time.time()
    conn = SQL.connect(DB_NAME)
    cursor = conn.cursor()

    data = AudioDataset()
    start = time.time()
    data.load()

    dataset = data.dataset

    for audio in dataset:
        filename = audio.filename
        atb = matrix_buffering(audio.atb)
        rtb = matrix_buffering(audio.rtb)
        ftb = matrix_buffering(audio.ftb)
        cursor.execute(
            "INSERT INTO audio_dataset (filename, atb, rtb, ftb) VALUES (?, ?, ?, ?)",
            (filename, atb, rtb, ftb)
        )

    conn.commit()
    conn.close()
    return (time.time() - start)


def fetch_images_from_database() -> ImageDataset:
    conn = SQL.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT filename, pixels, pca FROM image_dataset")
    rows = cursor.fetchall()

    dataset = []
    for filename, pixels, pca in rows:
        imageData = IMG.ImageData(filename, None, None)
        pixels_buffer = IMG.io.BytesIO(pixels)
        img = IMG.PIL.open(pixels_buffer)

        imageData.pixels = np.array(img)
        imageData.pca = np.load(IMG.io.BytesIO(pca))
        dataset.append(imageData)

    cursor.execute("SELECT Uk_matrix, pixel_means FROM image_matrix")
    row = cursor.fetchone()
    Uk_matrix = np.load(IMG.io.BytesIO(row[0]))
    pixel_means = np.load(IMG.io.BytesIO(row[1]))
    conn.close()

    data = ImageDataset()
    data.dataset = dataset
    data.Uk = Uk_matrix
    data.pixel_means = pixel_means
    return data


def fetch_audio_from_database() -> AudioDataset:
    conn = SQL.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT filename, atb, rtb, ftb FROM audio_dataset")
    rows = cursor.fetchall()

    dataset = []
    for filename, atb, rtb, ftb in rows:
        audioData = MSC.AudioData(filename)

        audioData.atb = np.load(IMG.io.BytesIO(atb))
        audioData.rtb = np.load(IMG.io.BytesIO(rtb))
        audioData.ftb = np.load(IMG.io.BytesIO(ftb))
        dataset.append(audioData)

    conn.close()

    data = ImageDataset()
    data.dataset = dataset
    return data


def query_image(query_path, pic_to_audio: dict) -> tuple[list[dict], float]:
    start_time = time.time()
    similarity_list = []
    query = [IMG.load_query(query_path)]

    image_dataset = fetch_images_from_database()
    dataset = image_dataset.dataset
    Uk = image_dataset.Uk
    pixel_means = image_dataset.pixel_means

    IMG.standardize_images(query, pixel_means)
    query[0].k = image_dataset.dataset[0].k
    IMG.principal_component_analysis_query(query[0], Uk)
    IMG.calculate_eucledian_distance(dataset, query[0])

    closest_results = sorted(
        [image for image in dataset if image.euclid_distance < 1000000],  # Filter
        key=lambda image: image.euclid_distance)

    for image_file in closest_results:
        similarity_entry = {
            "image_name": image_file.filename,
            "similarity": image_file.similarity
        }

        if image_file.filename in pic_to_audio:
            similarity_entry["audio_name"] = pic_to_audio[image_file.filename]
        else:
            similarity_entry["audio_name"] = "Not Found"

        similarity_list.append(similarity_entry)
    return filter_result(similarity_list), (time.time() - start_time)


def query_audio(query_path, audio_to_pic: dict) -> tuple[list[dict], float]:
    start_time = time.time()
    similarity_list = []
    query_name = query_path.rsplit("/", 1)[-1]
    query = MSC.AudioData(query_name, 'q')
    query.extract_features()

    audio_dataset = fetch_audio_from_database()

    for audio_file in audio_dataset.dataset:
        audio_file.calculate_similarity(query)
        similarity_entry = {
            "audio_name": audio_file.filename,
            "similarity": audio_file.similarity
        }

        if audio_file.filename in audio_to_pic:
            similarity_entry["image_name"] = audio_to_pic[audio_file.filename]
        else:
            similarity_entry["image_name"] = "Not Found"

        similarity_list.append(similarity_entry)

    return filter_result(similarity_list), (time.time() - start_time)


def filter_result(similarity_list: list):
    filtered_list = [item for item in similarity_list if item["similarity"] >= 0.5]
    filtered_list.sort(key=lambda x: x["similarity"], reverse=True)

    if len(filtered_list) > 30:
        filtered_list = filtered_list[:30]
    return filtered_list


# Create Tables dulu biar table sebelumny kehapus
if __name__ == "__main__":
    audio_to_pic, pic_to_audio = MAP.load_mapper(DATADIR)
    # create_tables()
    # print(f"Load Image Runtime: {save_image_to_database()}")
    # print(f"Load Audio Runtime: {save_audio_to_database()}")

    # similarity_list_img, runtime_img = query_image(DIR + 'query/query.png', pic_to_audio)
    # with open(DIR + "image.json", 'w') as json_file:
    #     json.dump(similarity_list_img, json_file, indent=4)
    # print(f"Query Image: {runtime_img}")

    similarity_list_aud, runtime_aud = query_audio(DIR + 'query/query.wav', audio_to_pic)
    with open(DIR + "audio.json", 'w') as json_file:
        json.dump(similarity_list_aud, json_file, indent=4)
    print(f"Query Audio: {runtime_aud}")


