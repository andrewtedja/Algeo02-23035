# COBA DI SATU FILE DULU 
from PIL import Image as PIL
import numpy as np
import os
from time import time
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
        self.standardized_pixels = None
        self.pca = None
        self.k = None   # Principal Component Count
        self.euclid_distance = None
    def __str__(self):
        # return '\n'.join(f"{key}: {value}" for key, value in self.__dict__.items())
        return f"File: {self.filename}\nEuclid: {self.euclid_distance}\n"


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
def crop_image(grayscale : Matrix) -> Matrix:
    width, height = grayscale.shape[1], grayscale.shape[0]

    if (width > height):
        start_row = 0
        end_row = height

        start_col = (width - height) / 2
        end_col = width - start_col
    else:
        start_row = (height - width) / 2
        end_row = height - start_row

        start_col = 0
        end_col = width

    cropped = grayscale[int(start_row):int(end_row), int(start_col):int(end_col)]
    return cropped

def normalize_image(cropped : Matrix) -> Matrix:
    dim = (2,2)
    img = PIL.fromarray(cropped)
    resized_img = img.resize(dim, PIL.Resampling.BILINEAR) # Resizing
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
    cropped = crop_image(grayscale)
    resized = normalize_image(cropped)
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
# Menghitung rata2 pixel gambar dataset
def get_pixel_means(dataset : list[ImageData]) -> Vector:
    pixel_matrix = np.array([image.pixels for image in dataset])
    img_total = len(dataset)
    pixel_means = []

    for j in range(pixel_matrix.shape[1]):
        pixel_sum = 0
        for i in range(img_total):
            pixel_sum += pixel_matrix[i][j]
        pixel_means.append(pixel_sum/img_total)

    return np.array(pixel_means)

def standardize_images(dataset : list[ImageData], pixel_means) -> None:
    # Ubah vector menjadi matrix, dimana setiap baris adalah image berbeda
    # dan setiap kolom adalah pixel2 nya matrix N*jumlah_pixel
    pixel_matrix = np.array([image.pixels for image in dataset])
    standardized_pixels_list = pixel_matrix - pixel_means # Standarisasi Pixel
    
    # Perbarui pixel pada dataset
    for image, standardized_pixels in zip(dataset, standardized_pixels_list):
        image.standardized_pixels = standardized_pixels





################# PCA Computation (SVD) #################
# Digunakan pada dataset terstandarisasi
def get_covariance_matrix(dataset : list[ImageData]) -> Matrix:

    img_count = len(dataset)
    # Mengubah banyak flattened vectors menjadi matrix
    X_matrix = np.array([image.standardized_pixels for image in dataset])

    covariance_matrix = (X_matrix.T @ X_matrix) / img_count

    return covariance_matrix

# Helper to get eigenvalues
def qr_decomposition(A : Matrix) -> Tuple[Matrix, Matrix]:
    m, n = A.shape  # Ambil row dan col
    Q = np.zeros((m, n))
    R = np.zeros((n, n))

    for i in range(n):
        v = A[:, i].copy()

        for j in range(i):
            R[j, i] = np.dot(Q[:, j], v)
            v = v - R[j, i] * Q[:, j]

        R[i, i] = np.sqrt(np.sum(v**2))
        Q[:, i] = v / R[i, i]

    return Q, R

# Menggunakan QR Algorithm https://www.youtube.com/watch?v=McHW221J3UM
def get_eigen(A : Matrix) -> Tuple[Vector, Matrix]:
    iter = 1000
    tol = 10-6  # Tolerance (presisi)

    n = A.shape[0]
    Q_total = np.eye(n)

    for _ in range(iter):
        Q, R = qr_decomposition(A)

        A = R @ Q
        Q_total = Q_total @ Q

        # Convergence check
        off_diag = A - np.diag(np.diagonal(A))
        if np.sqrt(np.sum(off_diag**2)) < tol:
            break
        
        eigenvalues = np.maximum(np.diagonal(A), 0) # Round negatives to zero
        return eigenvalues, Q_total
    
# Mencari angka optimal untuk k
def choose_k(eigenvalues : Vector) -> int:
    threshold = 0.95
    S = np.sqrt(eigenvalues)    # singular values

    total_variance = np.sum(S**2)
    cumulative_variance = np.cumsum(S**2)
    k = np.argmax(cumulative_variance >= threshold * total_variance) + 1
    return k 
    
# I.S. M adalah matriks n x n (square)
# Mengembalikan Matriks U
def singular_value_decomposition(C : Matrix) -> Tuple[Matrix, int]:
    eigenvalues, eigenvectors = np.linalg.eig(C)
    # eigenvalues, eigenvectors = get_eigen(C)
    # Urut eigenvalue berdasarkan nilai singular
    sorted_indices = np.argsort(eigenvalues)[::-1]
    U = eigenvectors[:,sorted_indices]
    # U, s, vh = np.linalg.svd(C)
    k = choose_k(eigenvalues)
    return U, k

def get_top_k_components(U : Matrix, k : int) -> Matrix:
    return U[:, :k]

# Digunakan pada dataset yang sudah distandarisasi
# Set atribut pca pada List ImageData
def principal_component_analysis_dataset(dataset : list[ImageData]) -> Matrix:
    X = np.array([image.standardized_pixels for image in dataset])

    C = get_covariance_matrix(dataset)
    U, k = singular_value_decomposition(C)

    if dataset[0].k is not None:    # Overwrite k (ini hanya untuk query)
        k = dataset[0].k
    Uk = get_top_k_components(U,k)
    Z_matrix = X @ Uk

    for image, projection in zip(dataset, Z_matrix):
        image.pca = np.real(projection)
        image.k = k
    return Uk

def principal_component_analysis_query(query : ImageData, Uk : Matrix) -> None:
    pixels = query.standardized_pixels
    projection = pixels @ Uk
    query.pca = np.real(projection)


################# Similarity Computation #################
def calculate_eucledian_distance(dataset: list[ImageData], query: ImageData) -> None:
    q = query.pca
    k = query.k
    for images in dataset:
        z = images.pca
        distance = np.sqrt(np.sum((q - z) ** 2)) 
        images.euclid_distance = distance




################# Retrieval and Output #################
def master():
    start = time()

    dataset = load_dataset()
    query = [load_query("query/query.png")]

    pixel_means = get_pixel_means(dataset)

    standardize_images(dataset, pixel_means)
    standardize_images(query, pixel_means)

    Uk = principal_component_analysis_dataset(dataset)
    query[0].k = dataset[0].k
    principal_component_analysis_query(query[0], Uk)
    calculate_eucledian_distance(dataset, query[0])

    # TESTING
    closest_results = sorted(
    [image for image in dataset if image.euclid_distance < 10],  # Filter
    key=lambda image: image.euclid_distance  # Sort
)
    displayObjectList(closest_results)

    end = time()

    print(f"Runtime: {end - start}")


################# UTILITY #################
def displayObjectList(list : list[object]) -> None :
    for object in list:
        print(object)
        print()


master()

