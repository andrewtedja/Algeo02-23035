import sqlite3 as SQL
import backend.app.feature.album_finder.image_processing as IMG
# import backend.app.feature.music_retrieval as MSC
import numpy as np  # noqa

# DI RUN DARI ROOT (src)

# NGECEK DB
# /mnt/d/RaFa/Main/School/ITB/Kuliah 4 Tahun/Sem 3/Algeo/Tubes/Algeo02-23035/src/backend/app/data


DB_NAME = "backend/app/data/data.db"
DIR = "backend/app/data/dataset/"
IMG_DIR = "backend/app/data/dataset/image"
AUD_DIR = "backend/app/data/dataset/audio"


class ImageDataset:
    def __init__(self):
        pass

    def load(self):
        self.dataset, self.Uk, self.pixel_means = load_and_proccess_image_dataset()


def load_and_proccess_image_dataset() -> tuple[list[IMG.ImageData], IMG.Matrix, IMG.Vector]:
    dataset = IMG.load_dataset(IMG_DIR)
    pixel_means = IMG.get_pixel_means(dataset)
    IMG.standardize_images(dataset, pixel_means)
    Uk = IMG.principal_component_analysis_dataset(dataset)

    return dataset, Uk, pixel_means

# def load_and_proccess_audio_dataset():


def matrix_buffering(matrix: IMG.Matrix):
    buffer = IMG.io.BytesIO()
    np.save(buffer, matrix)
    return buffer.getvalue()


def create_tables(cursor: SQL.Cursor) -> None:
    # CLEAR TABLE
    cursor.execute('DROP TABLE IF EXISTS image_dataset')
    cursor.execute('DROP TABLE IF EXISTS image_matrix')
    cursor.execute('DROP TABLE IF EXISTS music_features')

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
    CREATE TABLE music_features (
        filename TEXT PRIMARY KEY,
        atb BLOB NOT NULL,
        rtb BLOB NOT NULL,
        ftb BLOB NOT NULL)
''')



def save_to_database(dataset: list[IMG.ImageData], Uk: IMG.Matrix, pixel_means: IMG.Vector) -> None:  # noqa
    conn = SQL.connect(DB_NAME)
    cursor = conn.cursor()

    create_tables(cursor)

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


def fetch_images_from_database() -> tuple[list[IMG.ImageData], IMG.Matrix, IMG.Vector]:
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
    return dataset, Uk_matrix, pixel_means


# dataset, Uk, means = load_and_proccess_image_dataset()
# save_to_database(dataset, Uk, means)
dataset, Uk, means = fetch_images_from_database()
