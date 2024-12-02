import sqlite3 as SQL
import backend.app.feature.album_finder.image_processing as IMG
import numpy as np

# DI RUN DARI ROOT (src)

# NGECEK DB
# /mnt/d/RaFa/Main/School/ITB/Kuliah 4 Tahun/Sem 3/Algeo/Tubes/Algeo02-23035/src/backend/app/data





DB_NAME = "backend/app/data/data.db"
IMG_DIR = "backend/app/data/dataset/image"

def load_and_proccess_image_dataset() -> tuple[list[IMG.ImageData], IMG.Matrix, IMG.Vector ]:
    dataset = IMG.load_dataset(IMG_DIR)
    pixel_means = IMG.get_pixel_means(dataset)
    IMG.standardize_images(dataset, pixel_means)
    Uk = IMG.principal_component_analysis_dataset(dataset)

    return dataset, Uk, pixel_means
# how do i make it so that everytime this file is run, clear the .db file?
def save_image_data_to_database(dataset: list[IMG.ImageData], Uk: IMG.Matrix, pixel_means: IMG.Vector) -> None:
    conn = SQL.connect(DB_NAME)
    cursor = conn.cursor()
    
    # CLEAR TABLE
    cursor.execute('DROP TABLE IF EXISTS image_dataset')
    cursor.execute('''
    CREATE TABLE image_dataset (
        filename TEXT PRIMARY KEY NOT NULL,               
        pca_projection BLOB NOT NULL)                  
''')
    
    for image in dataset:
        filename = image.filename
        projection = image.pca
        pca = projection.tobytes()
        cursor.execute(
            "INSERT INTO image_dataset (filename, pca_projection) VALUES (?, ?)",
            (filename, pca)
        )
    conn.commit()
    conn.close()

dataset, Uk, means = load_and_proccess_image_dataset()
save_image_data_to_database(dataset, Uk, means)