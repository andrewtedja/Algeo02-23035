# COBA DI SATU FILE DULU 
from PIL import Image as PIL
import numpy as np
import os
from typing import *

# TYPE DEFINING
Matrix = np.ndarray
String = str
Vector = List[float]
VectorList = List[Vector]

# CLASS
class ImageData:
    def __init__(self, filename : String, pixels: Vector)-> None:
        self.filename = filename
        self.pixels = pixels
        self.size =  int(np.sqrt(len(self.pixels)))if self.pixels is not None else None
        self.euclid_distance = None
    def __str__(self):
        return '\n'.join(f"{key}: {value}" for key, value in self.__dict__.items())


################# Image Processing and Loading #################
# Mendapatkan Matrix grayscale
def extract_grayscale(file_path : String) -> Matrix:
    img = PIL.open(file_path).convert("RGB")
    rgb = np.array(img) # Array RGB

    R = rgb[:, :, 0]
    G = rgb[:, :, 1]
    B = rgb[:, :, 2]
    
    grayscale = 0.2989 * R + 0.5870 * G + 0.1140 * B
    grayscale = grayscale.astype(np.uint8)  # Membuat hasil perhitungan Integer

    return grayscale

# Menyamakan ukuran dari gambar (mengubah satu gambar menjadi ukuran tertentu)
def normalize_image(grayscale : Matrix) -> Matrix:
    img = PIL.fromarray(grayscale)
    resized_img = img.resize((64,64), PIL.Resampling.BILINEAR) # Resizing
    return np.array(resized_img) # Return numpy array

def matrix_to_1d(resized : Matrix) -> Vector:
    flattened = []
    for row in resized:
        for value in row:
            flattened.append(value) # append setiap row ke dalam 1 row saja
    return np.array(flattened)      # numpy array untuk speed efficiency

# Menyatukan semua proses diatas
def preprocess_image(file_path : String) -> Vector:
    grayscale = extract_grayscale(file_path)
    resized = normalize_image(grayscale)
    vector = matrix_to_1d(resized)
    return vector

# Memproses data-data gambar dataset
def load_dataset() -> list[ImageData]:
    dataset_list = []
    directory = "images"
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        image = ImageData(filename, preprocess_image(file_path))
        dataset_list.append(image)
    return dataset_list

# Memproses data gambar query
def load_query(file_path) -> ImageData:
    filename = os.path.basename(file_path)
    image = ImageData(filename, preprocess_image(file_path))
    return image


################# Data Centering (Standardization) #################

def get_pixel_means(dataset : list[ImageData]) -> Vector:
    pixel_matrix = np.array([image.pixels for image in dataset])    
    return np.mean(pixel_matrix, axis=0)  # Menghitung rata2 pixel dataset

def standardize_images(dataset : list[ImageData]) -> None:
    # Ubah vector menjadi matrix, dimana setiap baris adalah image berbeda
    # dan setiap kolom adalah pixel2 nya matrix N*jumlah_pixel
    pixel_matrix = np.array([image.pixels for image in dataset])
    pixel_means = get_pixel_means(dataset)
    standardized_pixels_list = pixel_matrix - pixel_means # Standarisasi Pixel
    
    # Perbarui pixel pada dataset
    for image, standardized_pixels in zip(dataset, standardized_pixels_list):
        image.pixels = standardized_pixels

################# UTILITY #################
def displayObjectList(list : list[object]) -> None :
    for object in list:
        print(object)
        print()

dataset = load_dataset()
displayObjectList(dataset)

standardize_images(dataset)
displayObjectList(dataset)




