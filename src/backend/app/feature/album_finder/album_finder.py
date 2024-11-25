# COBA DI SATU FILE DULU 
from PIL import Image as PIL
import numpy as np
import os
from typing import *

# TYPE DEFINING
Matrix = np.ndarray
String = str
Vector = List[float]

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
def image_normalization(grayscale : Matrix) -> Matrix:
    img = PIL.fromarray(grayscale)
    resized_img = img.resize((64,64), PIL.Resampling.BILINEAR) # Resizing
    return np.array(resized_img) # Return numpy array

def matrix_to_1d(resized : Matrix) -> Vector:
    flattened = []
    for row in resized:
        for value in row:
            flattened.append(value)
    return np.array(flattened)      # numpy array untuk speed efficiency






###################### DEBUGGING/TESTING ######################
# Mengubah image menjadi grayscale  
def test_convert_img_to_grayscale(file_path : str) -> None:
    grayscale = extract_grayscale(file_path)
    gray_img = PIL.fromarray(grayscale)

    test_directory_assert()

    gray_img.save("result/dinogra.png")    # Save into img
    print("Saved succesfully")

def test_resize_img_to_64(file_path):
    img = PIL.open(file_path).convert("RGB")
    resized_img = img.resize((64,64), PIL.Resampling.BILINEAR) # Resizing
    
    test_directory_assert()
    
    resized_img.save("result/dinogra.png")    # Save into img
    print("Saved succesfully")

################# UTILITY #################
def test_directory_assert():
    output_dir = "result"                   # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)

# test_convert_img_to_grayscale("images/dino.png")
# test_resize_img_to_64("images/dino.png")

# test = matrix_to_1d(image_normalization(extract_grayscale("images/dino.png")))