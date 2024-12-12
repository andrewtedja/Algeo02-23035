# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
# from typing import List
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.exceptions import HTTPException

# import os
# import shutil # delete file ato directory (reset buat tiap upload)
# import subprocess # run external python scripts/features
# import requests
# import urllib.request # Download images from URLs during scraping.


# app = FastAPI()

# origins = [
#     'https://localhost:3000',
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class Item(BaseModel):
#     url: str

# UPLOAD_FOLDER = "src/uploads/"
# UPLOAD_DATASET_FOLDER = "src/dataset/"


# # ========================================= API Endpoints ==========================================
# async def lifespan(app: FastAPI):    
#     if not os.path.exists(UPLOAD_FOLDER):
#         os.makedirs(UPLOAD_FOLDER)
#     yield 

# def is_image(filename):
#     allowed_extensions = {".jpg", ".jpeg", ".png"}
#     return any(filename.lower().endswith(ext) for ext in allowed_extensions)

# def is_audio(filename):
#     allowed_extensions = {".mid", ".midi", ".wav"}
#     return any(filename.lower().endswith(ext) for ext in allowed_extensions)

# # =================== UPLOAD FILE =================== 
# @app.post("upload")
# async def upload_file(file: UploadFile):
#     if not file:
#         raise HTTPException(status_code=400, detail="Tidak ada file yang diunggah.")

#     if not is_audio(file.filename):
#         raise HTTPException(status_code=400, detail="File yang diunggah bukan audio.")
#     if not is_image(file.filename):
#         raise HTTPException(status_code=400, detail="File yang diunggah bukan gambar.")

#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)

#     with open(file_path, "wb") as f:
#         f.write(file.file.read())
#     # subprocess.run(["python", "backend/feature/....."], check=True)
#     # subprocess.run(["python", "backend/feature/....."], check=True)

# # =================== UPLOAD DATASET =================== 
# @app.post("/upload-dataset")
# async def upload_dataset(files: List[UploadFile] = File(...)):
#     for filename in os.listdir(UPLOAD_DATASET_FOLDER):
#         file_path = os.path.join(UPLOAD_DATASET_FOLDER, filename)
#         try:
#             if os.path.isfile(file_path) or os.path.islink(file_path):
#                 os.unlink(file_path)
#             elif os.path.isdir(file_path):
#                 shutil.rmtree(file_path)
#         except Exception as e:
#             print('Failed to delete %s. Reason: %s' % (file_path, e))

#     for file in files:
#         if not is_image(file.filename):
#             raise HTTPException(status_code=400, detail="Berkas yang diunggah bukan gambar")
#         file_path = os.path.join(UPLOAD_DATASET_FOLDER, os.path.basename(file.filename))

#         with open(file_path, "wb") as f:
#             f.write(file.file.read())
    
#     # subprocess.run(["python", "backend/feature/....."], check=True)
#     return JSONResponse(content={"message" : "Dataset berhasil diunggah"})




