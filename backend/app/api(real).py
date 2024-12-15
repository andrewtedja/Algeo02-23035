from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from backend.app.utils import reset_folder

import os
import shutil  
import subprocess  
import requests
import urllib.request 

from backend.app.feature.music_retrieval.main import save_dataset_similarity, get_similar_file

app = FastAPI()

origins = [
    'https://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],    
)

class Item(BaseModel):
    url: str

UPLOAD_FOLDER = "src/uploads/"
DATASET_FOLDER = "src/datasets/"

# Ensure necessary folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATASET_FOLDER, exist_ok=True)

# =========================== CHECKER ===============================
def is_image(filename):
    return any(filename.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png"))

def is_audio(filename):
    return filename.lower().endswith(('.mid', '.midi', '.wav'))

def is_folder_empty(folder_path):
    return not any(os.scandir(folder_path))

# =================== UPLOAD FILE =================== 
# @app.post("/upload-audio/")
# async def upload_audio(file: UploadFile):
#     if not file or not is_audio(file.filename):
#         raise HTTPException(status_code=400, detail="Invalid audio file uploaded.")
    
#     # Ensure dataset is uploaded
#     if is_folder_empty(DATASET_FOLDER):
#         raise HTTPException(status_code=400, detail="Dataset folder is empty. Please upload a dataset first.")

#     # Ensure mapper is uploaded
#     if is_folder_empty("src/mappers/"):
#         raise HTTPException(status_code=400, detail="Mapper file is missing. Please upload a mapper first.")

#     # Reset the upload folder to clear old files
#     reset_folder(UPLOAD_FOLDER)

#     # Save query file and process...
#     query_path = os.path.join(UPLOAD_FOLDER, file.filename)
#     with open(query_path, "wb") as f:
#         f.write(await file.read())
    
#     # Process similarity
#     dataset_similarities = save_dataset_similarity(query_path, DATASET_FOLDER)
#     if not dataset_similarities:
#         return JSONResponse(content={"message": "No similar files found."}, status_code=200)
    
#     most_similar_file, cosine_similarity = get_similar_file(dataset_similarities)

#     # Reset the upload folder after processing
#     reset_folder(UPLOAD_FOLDER)

#     return JSONResponse(content={
#         "query_file": file.filename,
#         "most_similar_file": most_similar_file,
#         "cosine_similarity": cosine_similarity,
#         "all_similarities": dataset_similarities
#     })

# @app.post("/upload-image/")
# async def upload_image(file: UploadFile):
#     if not file or not is_image(file.filename):
#         raise HTTPException(status_code=400, detail="Invalid image file uploaded.")
    
#     # Ensure dataset is uploaded
#     if is_folder_empty(DATASET_FOLDER):
#         raise HTTPException(status_code=400, detail="Dataset folder is empty. Please upload a dataset first.")
    
#     # Ensure mapper is uploaded
#     if is_folder_empty("src/mappers/"):
#         raise HTTPException(status_code=400, detail="Mapper file is missing. Please upload a mapper first.")
    
#     # Reset the upload folder to clear old files
#     reset_folder(UPLOAD_FOLDER)

#     # Save query file and process...
#     query_path = os.path.join(UPLOAD_FOLDER, file.filename)
#     with open(query_path, "wb") as f:
#         f.write(await file.read())
    
#     # PCA processing and similarity logic...

#     reset_folder(UPLOAD_FOLDER)

#     return JSONResponse(content={"message": "Image query processed successfully."})



# Upload Dataset Files
@app.post("/upload-dataset/")
async def upload_dataset(files: List[UploadFile] = File(...)):
    # Reset the dataset folder before uploading new files
    reset_folder(DATASET_FOLDER)  

    # Save new dataset files
    for file in files:
        if not is_audio(file.filename):
            raise HTTPException(status_code=400, detail="Invalid audio file in dataset.")
        file_path = os.path.join(DATASET_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

    return JSONResponse(content={"message": "Dataset successfully uploaded."})

@app.get("/list-dataset/")
async def list_dataset():
    if is_folder_empty(DATASET_FOLDER):
        return JSONResponse(content={"message": "Dataset folder is empty."})

    files = os.listdir(DATASET_FOLDER)
    return JSONResponse(content={"dataset_files": files})