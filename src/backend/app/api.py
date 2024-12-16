from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import sys
import os
import zipfile
import rarfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from src.backend.app.data.database import save_image_to_database, save_audio_to_database
from src.backend.app.data.mapper import load_mapper
from src.backend.app.data.database import query_image
from src.backend.app.data.database import query_audio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
############################# UTILS #############################
def clear_directory(dir_path: str):
    if os.path.exists(dir_path):
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

def detect_dataset_type(base_dir: str) -> str:
    image_extensions = {'.jpg', '.jpeg', '.png'}
    audio_extensions = {'.wav', '.mid', '.midi'}

    for root, dirs, files in os.walk(base_dir):
        for f in files:
            ext = os.path.splitext(f.lower())[1]
            if ext in image_extensions:
                return "image"
            elif ext in audio_extensions:
                return "audio"
    raise HTTPException(status_code=400, detail="No supported image or audio files.")

############################## UPLOAD DATASET #############################
@app.post("/upload/dataset")
async def upload_dataset(file: UploadFile = File(...)):
    datasets_dir = os.path.join("src", "datasets")
    os.makedirs(datasets_dir, exist_ok=True)
    clear_directory(datasets_dir)  # Clear old files

    dataset_path = os.path.join(datasets_dir, file.filename)
    with open(dataset_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.filename.endswith(".zip"):
        with zipfile.ZipFile(dataset_path, "r") as zip_ref:
            zip_ref.extractall(datasets_dir)
    elif file.filename.endswith(".rar"):
        with rarfile.RarFile(dataset_path) as rar_ref:
            rar_ref.extractall(datasets_dir)
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file (must be .zip or .rar)."
        )
    
    # SAVE TO DATABASE
    runtime = save_image_to_database()

    dataset_type = detect_dataset_type(datasets_dir)
    if dataset_type == "image":
        runtime = save_image_to_database()
    else:  #audio
        runtime = save_audio_to_database()

    return {
        "message": f"Dataset '{file.filename}' uploaded and saved to database!",
        "filename": file.filename,
        "dataset_type": dataset_type,
        "runtime": runtime
    }        

############################## UPLOAD FILES #############################
@app.post("/upload/album")
async def upload_album(file: UploadFile = File(...)):
    albums_dir = os.path.join("src", "uploads", "album")
    os.makedirs(albums_dir, exist_ok=True)
    clear_directory(albums_dir)  # Clear old files before saving new one

    file_path = os.path.join(albums_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"Album cover '{file.filename}' uploaded successfully!", "filename": file.filename}


@app.post("/upload/audio")
async def upload_audio(file: UploadFile = File(...)):
    audio_dir = os.path.join("src", "uploads", "audio")
    os.makedirs(audio_dir, exist_ok=True)
    clear_directory(audio_dir)  # Clear old files

    file_path = os.path.join(audio_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"Audio file '{file.filename}' uploaded successfully!", "filename": file.filename}


@app.post("/upload/mapper")
async def upload_mapper(file: UploadFile = File(...)):
    datasets_dir = os.path.join("src", "datasets")
    os.makedirs(datasets_dir, exist_ok=True)
    clear_directory(datasets_dir)  # Clear old files

    mapper_path = os.path.join(datasets_dir, file.filename)
    with open(mapper_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"Mapper '{file.filename}' uploaded successfully!", "filename": file.filename}


############################## MAIN #############################
@app.post("/search/album")
async def search_album(file: UploadFile = File(...)):
    query_dir = os.path.join("src", "query", "album")
    os.makedirs(query_dir, exist_ok=True)
    clear_directory(query_dir)

    query_path = os.path.join(query_dir, file.filename)
    with open(query_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    DATADIR = "backend/app/data/"
    audio_to_pic, pic_to_audio = load_mapper(DATADIR)

    results, runtime = query_image(query_path, pic_to_audio)

    return {"results": results, "runtime": runtime}

@app.post("/search/audio")
async def search_audio(file: UploadFile = File(...)):
    query_dir = os.path.join("src", "query", "audio")
    os.makedirs(query_dir, exist_ok=True)
    clear_directory(query_dir)

    query_path = os.path.join(query_dir, file.filename)
    with open(query_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    DATADIR = "backend/app/data/"
    audio_to_pic, pic_to_audio = load_mapper(DATADIR)

    results, runtime = query_audio(query_path, audio_to_pic)

    return {"results": results, "runtime": runtime}